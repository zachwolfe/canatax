from decimal import Decimal
from canatax.calculators.base_calculator import BaseCalculator
from canatax.enums import ProvinceOrTerritory, TaxType
from canatax.exc import CanataxError
from canatax.rates.income.current_tax import ProvincialIncomeTaxRate
from canatax.tax_estimate import IncomeTaxEstimate
from canatax.rates.income.current_tax import *
from canatax.utils import decimal_round
from canatax.rates.income.current_contributions import Contributions


class IncomeTaxCalculator(BaseCalculator):

    def __init__(self, employment_income: int | float | Decimal, self_employment_income: int | float | Decimal, province: ProvinceOrTerritory | str, year: int = 2025):
        employment_income = self._decimalize(employment_income)
        self_employment_income = self._decimalize(self_employment_income)
        super().__init__(province=province, year=year)
        self.employment_income = decimal_round(employment_income)
        self.self_employment_income = decimal_round(self_employment_income)
        self.income = self.employment_income + self.self_employment_income
        # Dynamically import correct FederalIncomeTaxRate for year
        if int(year) == 2024:
            from canatax.rates.income.tax_rates.rates_2024 import FederalIncomeTaxRate as FedRate
        else:
            from canatax.rates.income.tax_rates.rates_2025 import FederalIncomeTaxRate as FedRate
        self.federal_tax_rate = FedRate()
        self.provincial_tax_rate = self._get_tax_rate(TaxType.INCOME)
        self.contributions = Contributions(year)

    def _get_tax_rate(self, tax_type: TaxType) -> ProvincialIncomeTaxRate:
        tax_rate = super()._get_tax_rate(tax_type)
        return tax_rate

    def _calculate(self) -> IncomeTaxEstimate:
        ei = self._ei()
        # Calculate CPP/QPP and track employment/self-employment portions
        if self.is_quebec():
            qpp, qpp_emp, qpp_se = self._cpp()
            cpp = Decimal(0)
            cpp_se = qpp_se
        else:
            cpp, cpp_emp, cpp_se = self._cpp()
            qpp = Decimal(0)
        qpip = self._qpip()

        # Deduct half of CPP/QPP paid on self-employment income from taxable income
        half_cpp_se_deduction = cpp_se * Decimal('0.5') if self.self_employment_income > 0 else Decimal(0)
        taxable_income = self.income - half_cpp_se_deduction
        federal_tax_base = Decimal(self.federal_tax_rate.calculate_tax(taxable_income) - self.federal_tax_rate.calculate_tax(self.federal_tax_rate.get_bpa(taxable_income)))
        provincial_tax_base = Decimal(self.provincial_tax_rate.calculate_tax(taxable_income) - self.provincial_tax_rate.calculate_tax(self.provincial_tax_rate.get_bpa(taxable_income)))

        # Non-refundable tax credit for "employee" portion of self-employed CPP/QPP
        cpp_nrtc = self.federal_tax_rate.calculate_tax(cpp_se * Decimal('0.5'))
        prov_cpp_nrtc = self.provincial_tax_rate.calculate_tax(cpp_se * Decimal('0.5'))

        # Province-specific tax credits
        prov_tax_credits = self.provincial_tax_rate.province_specific_tax_credits(taxable_income)

        federal_tax = decimal_round(federal_tax_base - cpp_nrtc)
        provincial_tax = decimal_round(provincial_tax_base - prov_cpp_nrtc - prov_tax_credits)
        total_tax = federal_tax + provincial_tax + ei + cpp + qpip
        net_income = self.income - total_tax
        return IncomeTaxEstimate(
            province=self.province,
            gross_income=self.income,
            federal_tax=federal_tax,
            provincial_tax=provincial_tax,
            ei=ei,
            cpp=cpp,
            qpp=qpp,
            qpip=qpip,
            total_tax=total_tax,
            net_income=net_income,
        )

    @classmethod
    def calculate(cls, employment_income: float | int | Decimal, self_employment_income: float | int | Decimal, province: str | ProvinceOrTerritory, year: int = 2025) -> IncomeTaxEstimate:
        calculator = cls(employment_income=employment_income, self_employment_income=self_employment_income, province=province, year=year)
        return calculator._calculate()

    def _cpp(self):
        """
        Year-specific CPP calculation for employment and self-employment income.
        Returns: (total_cpp, employment_cpp, self_employment_cpp)
        """
        if self.is_quebec():
            qpp = self.contributions.qpp
            emp_income = Decimal(self.employment_income)
            se_income = Decimal(self.self_employment_income)

            # --- Employment QPP ---
            emp_base_first_income = max(Decimal(0), min(emp_income, qpp.max_earnings) - qpp.exemption)
            emp_base_contrib = emp_base_first_income * qpp.base_rate_decimal
            emp_first_addl_contrib = emp_base_first_income * qpp.first_additional_rate_decimal
            emp_second_addl_income = max(Decimal(0), min(emp_income, qpp.additional_max) - qpp.additional_min)
            emp_second_addl_contrib = emp_second_addl_income * qpp.second_additional_rate_decimal
            emp_total = decimal_round(emp_base_contrib + emp_first_addl_contrib + emp_second_addl_contrib)

            # --- Self-Employment QPP ---
            total_income = emp_income + se_income
            se_base_first_income = max(Decimal(0), min(total_income, qpp.max_earnings) - qpp.exemption)
            se_base_first_income -= max(Decimal(0), min(emp_income, qpp.max_earnings) - qpp.exemption)
            se_base_contrib = se_base_first_income * qpp.base_rate_se_decimal
            se_first_addl_contrib = se_base_first_income * qpp.first_additional_rate_se_decimal
            se_second_addl_income = max(Decimal(0), min(total_income, qpp.additional_max) - qpp.additional_min)
            se_second_addl_income -= max(Decimal(0), min(emp_income, qpp.additional_max) - qpp.additional_min)
            se_second_addl_contrib = se_second_addl_income * qpp.second_additional_rate_se_decimal
            se_total = decimal_round(se_base_contrib + se_first_addl_contrib + se_second_addl_contrib)

            total = emp_total + se_total
            return total, emp_total, se_total

        cpp = self.contributions.cpp
        emp_income = Decimal(self.employment_income)
        se_income = Decimal(self.self_employment_income)

        # --- Employment CPP ---
        emp_base_first_income = max(Decimal(0), min(emp_income, cpp.max_earnings) - cpp.exemption)
        emp_base_contrib = emp_base_first_income * cpp.base_rate_decimal
        emp_first_addl_contrib = emp_base_first_income * cpp.first_additional_rate_decimal
        emp_second_addl_income = max(Decimal(0), min(emp_income, cpp.additional_max) - cpp.additional_min)
        emp_second_addl_contrib = emp_second_addl_income * cpp.second_additional_rate_decimal
        emp_total = decimal_round(emp_base_contrib + emp_first_addl_contrib + emp_second_addl_contrib)

        # --- Self-Employment CPP ---
        total_income = emp_income + se_income
        se_base_first_income = max(Decimal(0), min(total_income, cpp.max_earnings) - cpp.exemption)
        se_base_first_income -= max(Decimal(0), min(emp_income, cpp.max_earnings) - cpp.exemption)
        se_base_contrib = se_base_first_income * cpp.base_rate_se_decimal
        se_first_addl_contrib = se_base_first_income * cpp.first_additional_rate_se_decimal
        se_second_addl_income = max(Decimal(0), min(total_income, cpp.additional_max) - cpp.additional_min)
        se_second_addl_income -= max(Decimal(0), min(emp_income, cpp.additional_max) - cpp.additional_min)
        se_second_addl_contrib = se_second_addl_income * cpp.second_additional_rate_se_decimal
        se_total = decimal_round(se_base_contrib + se_first_addl_contrib + se_second_addl_contrib)

        total = emp_total + se_total
        return total, emp_total, se_total

    def _ei(self) -> Decimal:
        # EI only applies to employment income, not self-employment
        if self.is_quebec():
            ei = self.contributions.ei_quebec
        else:
            ei = self.contributions.ei
        ei_float = min(self.employment_income, ei.max_earnings) * ei.rate_decimal
        return decimal_round(ei_float)

    def _qpip(self) -> Decimal:
        qpip = self.contributions.qpip
        if not self.is_quebec():
            return Decimal(0)

        return decimal_round(min(self.income, qpip.max_earnings) * qpip.rate_decimal)
