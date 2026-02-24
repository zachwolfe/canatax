from dataclasses import dataclass
from decimal import Decimal
from ..base import BaseContribution

# CPP:
# https://www.canada.ca/en/revenue-agency/news/newsroom/tax-tips/tax-tips-2024/canada-revenue-agency-announces-maximum-pensionable-earnings-contributions-2025.html
#
# EI & EIQuebec:
# https://www.canada.ca/en/revenue-agency/services/tax/businesses/topics/payroll/payroll-deductions-contributions/employment-insurance-ei/ei-premium-rates-maximums.html
#
# QPP:
# https://www.revenuquebec.ca/en/businesses/source-deductions-and-employer-contributions/calculating-source-deductions-and-employer-contributions/quebec-pension-plan-contributions/maximum-pensionable-salary-or-wages-and-contribution-rate/
#
# QPIP:
# https://www.quebec.ca/nouvelles/actualites/details/maintien-des-taux-de-cotisation-au-regime-quebecois-dassurance-parentale-en-2025-56294



@dataclass(frozen=True)
class EI(BaseContribution):

    rate = 1.64
    max_earnings = 65700


@dataclass(frozen=True)
class EIQuebec(EI):

    rate = 1.31


@dataclass(frozen=True)
class CPP(BaseContribution):

    base_rate = Decimal('4.95')
    base_rate_se = Decimal('9.9')
    first_additional_rate = Decimal('1.0')
    first_additional_rate_se = Decimal('2.0')
    second_additional_rate = Decimal('4.0')
    second_additional_rate_se = Decimal('8.0')

    max_earnings = Decimal('71300')
    exemption = Decimal('3500')
    additional_min = Decimal('71300')
    additional_max = Decimal('81200')

    @property
    def base_rate_decimal(self) -> Decimal:
        return self.base_rate / Decimal('100')

    @property
    def base_rate_se_decimal(self) -> Decimal:
        return self.base_rate_se / Decimal('100')

    @property
    def first_additional_rate_decimal(self) -> Decimal:
        return self.first_additional_rate / Decimal('100')

    @property
    def first_additional_rate_se_decimal(self) -> Decimal:
        return self.first_additional_rate_se / Decimal('100')

    @property
    def second_additional_rate_decimal(self) -> Decimal:
        return self.second_additional_rate / Decimal('100')

    @property
    def second_additional_rate_se_decimal(self) -> Decimal:
        return self.second_additional_rate_se / Decimal('100')



@dataclass(frozen=True)
class QPP(CPP):
    # 2025 QPP rates (from Quebec Schedule 8)
    base_rate = Decimal('5.4')  # employee
    base_rate_se = Decimal('10.8')  # self-employed
    first_additional_rate = Decimal('1.0')  # employee
    first_additional_rate_se = Decimal('2.0')  # self-employed
    second_additional_rate = Decimal('4.0')  # employee
    second_additional_rate_se = Decimal('8.0')  # self-employed

    max_earnings = Decimal('71300')
    exemption = Decimal('3500')
    additional_min = Decimal('71300')
    additional_max = Decimal('81200')

    @property
    def base_rate_decimal(self) -> Decimal:
        return self.base_rate / Decimal('100')

    @property
    def base_rate_se_decimal(self) -> Decimal:
        return self.base_rate_se / Decimal('100')

    @property
    def first_additional_rate_decimal(self) -> Decimal:
        return self.first_additional_rate / Decimal('100')

    @property
    def first_additional_rate_se_decimal(self) -> Decimal:
        return self.first_additional_rate_se / Decimal('100')

    @property
    def second_additional_rate_decimal(self) -> Decimal:
        return self.second_additional_rate / Decimal('100')

    @property
    def second_additional_rate_se_decimal(self) -> Decimal:
        return self.second_additional_rate_se / Decimal('100')


@dataclass(frozen=True)
class QPIP(BaseContribution):

    max_earnings = Decimal('98000')
    rate = Decimal('0.494')
