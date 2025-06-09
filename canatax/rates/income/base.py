from decimal import Decimal, ROUND_HALF_UP
from canatax.utils import percent_to_decimal


class BaseIncomeTaxRate:
    
    brackets:None | list[tuple[float|int, int]] = None

    def calculate_tax(self, income:Decimal) -> Decimal:
        """Returns the tax owed (estimate) on a given income amount."""
        tax_owed = 0
        previous_threshold = 0
        for rate, threshold in self.brackets:
            if income > threshold:
                tax_owed += (threshold - previous_threshold) * percent_to_decimal(rate)
                previous_threshold = threshold
            else:
                tax_owed += (income - previous_threshold) * percent_to_decimal(rate)
                break
        return tax_owed.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)


class ProvincialIncomeTaxRate(BaseIncomeTaxRate):
    ...


class BaseContribution:

    rate = 0
    max_earnings = 0
    
    @property
    def rate_decimal(self) -> Decimal:
        return Decimal(self.rate / 100)
