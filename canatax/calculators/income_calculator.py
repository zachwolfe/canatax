from decimal import Decimal
from canatax.calculators.base_calculator import BaseCalculator
from canatax.enums import ProvinceOrTerritory, TaxType
from canatax.tax_estimate import IncomeTaxEstimate
from canatax.rates.income.current_tax import *
from canatax.utils import decimal_round
from canatax.rates.income.current_contributions import Contributions


class IncomeTaxCalculator(BaseCalculator):

    contributions = Contributions()

    def __init__(self, income: int | float | Decimal, province: ProvinceOrTerritory):

        income = self._decimalize(income)
        super().__init__(province=province)
        self.income = decimal_round(income)
        self.federal_tax_rate = FederalIncomeTaxRate()
        self.provincial_tax_rate:ProvincialIncomeTaxRate = self._get_tax_rate(TaxType.INCOME)

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
        net_income = self.income - total_tax
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
    def calculate(cls, income: float | int | Decimal, province: str | ProvinceOrTerritory) -> IncomeTaxEstimate:
        calculator = cls(income=income, province=province)
        return calculator._calculate()

    def _cpp(self) -> Decimal:
        
        if self.is_quebec():
            cpp = self.contributions.qpp
        else:
            cpp = self.contributions.cpp

        base_max = cpp.max_earnings - cpp.exemption
        base_contrib = min(self.income, base_max) * cpp.rate_decimal

        if self.income < cpp.additional_min:
            additional_contrib = Decimal(0)
        else:
            cpp2_income = min(self.income, cpp.additional_max) - cpp.additional_min
            additional_contrib = Decimal(cpp2_income * cpp.additional_rate_decimal)

        total = base_contrib + additional_contrib
        return decimal_round(total)

    def _ei(self) -> Decimal:
        if self.is_quebec():
            ei = self.contributions.ei_quebec
        else:
            ei = self.contributions.ei
        ei_float = min(self.income, ei.max_earnings) * ei.rate_decimal
        return decimal_round(ei_float)
        
    def _qpip(self) -> Decimal:
        qpip = self.contributions.qpip
        if not self.is_quebec():
            return Decimal(0)
        
        return decimal_round(min(self.income, qpip.max_earnings) * qpip.rate_decimal)
        
    def _tax(self) -> tuple[Decimal, Decimal]:
        """Return federal tax and provincial tax as a tuple object."""
        federal_tax = decimal_round(self.federal_tax_rate.calculate_tax(self.income))
        provincial_tax = decimal_round(self.provincial_tax_rate.calculate_tax(self.income))
        return federal_tax, provincial_tax