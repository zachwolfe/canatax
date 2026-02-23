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

    contributions = Contributions()

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

    def _get_tax_rate(self, tax_type: TaxType) -> ProvincialIncomeTaxRate:
        tax_rate = super()._get_tax_rate(tax_type)
        return tax_rate

    def _calculate(self) -> IncomeTaxEstimate:
        federal_tax_rate, provincial_tax_rate = self._tax()
        ei = self._ei()
        if self.is_quebec():
            cpp = Decimal(0)
            qpp = self._cpp()
        else:
            cpp = self._cpp()
            qpp = Decimal(0)
        qpip = self._qpip()
        total_tax = federal_tax_rate + provincial_tax_rate + ei + cpp + qpip

        net_income = self.employment_income + self.self_employment_income - total_tax
        return IncomeTaxEstimate(
            province=self.province,
            gross_income=self.income,
            federal_tax=federal_tax_rate,
            provincial_tax=provincial_tax_rate,
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

    def _cpp(self) -> Decimal:
        # CPP/QPP logic for employment vs self-employment
        if self.is_quebec():
            contrib = self.contributions.qpp
        else:
            contrib = self.contributions.cpp

        # Employment portion (regular rate, with exemption)
        emp_base_max = contrib.max_earnings - contrib.exemption
        emp_base_income = min(self.employment_income, emp_base_max)
        emp_base_contrib = emp_base_income * contrib.rate_decimal

        # Additional CPP/QPP (if applicable)
        emp_additional_contrib = Decimal(0)
        if self.employment_income >= contrib.additional_min:
            emp_cpp2_income = Decimal(min(self.employment_income, contrib.additional_max) - contrib.additional_min)
            emp_additional_contrib = emp_cpp2_income * Decimal(contrib.additional_rate_decimal)

        # Self-employment portion (2x rate, no exemption)
        se_base_max = contrib.max_earnings
        se_base_income = min(self.self_employment_income, se_base_max)
        se_base_contrib = se_base_income * contrib.rate_decimal * 2

        se_additional_contrib = Decimal(0)
        if self.self_employment_income >= contrib.additional_min:
            se_cpp2_income = Decimal(min(self.self_employment_income, contrib.additional_max) - contrib.additional_min)
            se_additional_contrib = se_cpp2_income * Decimal(contrib.additional_rate_decimal) * 2

        total = emp_base_contrib + emp_additional_contrib + se_base_contrib + se_additional_contrib
        return decimal_round(total)

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

    def _tax(self) -> tuple[Decimal, Decimal]:
        """Return federal tax and provincial tax as a tuple object."""
        federal_tax = decimal_round(self.federal_tax_rate.calculate_tax(self.income - self.federal_tax_rate.get_bpa(self.income)))
        provincial_tax = decimal_round(self.provincial_tax_rate.calculate_tax(self.income - self.provincial_tax_rate.get_bpa(self.income)))
        return federal_tax, provincial_tax
