
from dataclasses import dataclass
from decimal import Decimal
from ..base import BaseContribution

@dataclass(frozen=True)
class EI(BaseContribution):
    rate = 1.66
    max_earnings = 63600

@dataclass(frozen=True)
class EIQuebec(EI):
    rate = 1.32

@dataclass(frozen=True)
class QPIP(BaseContribution):
    max_earnings = Decimal('94000')
    rate = Decimal('0.494')

@dataclass(frozen=True)
class CPP(BaseContribution):
    base_rate = Decimal('4.95')
    base_rate_se = Decimal('9.9')
    first_additional_rate = Decimal('1.0')
    first_additional_rate_se = Decimal('2.0')
    second_additional_rate = Decimal('4.0')
    second_additional_rate_se = Decimal('8.0')

    max_earnings = Decimal('68500')
    exemption = Decimal('3500')
    additional_min = Decimal('68500')
    additional_max = Decimal('73200')

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


# QPP 2024
@dataclass(frozen=True)
class QPP(CPP):
    base_rate = Decimal('5.4')
    base_rate_se = Decimal('10.8')
    first_additional_rate = Decimal('1.0')
    first_additional_rate_se = Decimal('2.0')
    second_additional_rate = Decimal('4.0')
    second_additional_rate_se = Decimal('8.0')

    max_earnings = Decimal('68500')
    exemption = Decimal('3500')
    additional_min = Decimal('68500')
    additional_max = Decimal('73200')
