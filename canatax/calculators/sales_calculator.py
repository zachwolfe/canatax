from decimal import Decimal, ROUND_HALF_UP, InvalidOperation
from canatax.calculators.base_calculator import BaseCalculator
from canatax.enums import ProvinceOrTerritory, TaxType
from canatax.exc import InvalidDollarAmount
from canatax.tax_estimate import SalesTaxEstimate
from canatax.utils import percent_to_decimal


class SalesTaxCalculator(BaseCalculator):

    def __init__(self, province: ProvinceOrTerritory | str):
        super().__init__(province=province)
        self.tax_rate = self._get_tax_rate(TaxType.SALES)

    def calculate(self, amount: float | int | Decimal) -> SalesTaxEstimate:
        """Calculate sales tax for a given amount based on the tax rates for the initialized province or territory.

        This method calculates the GST, PST, and HST based on the provided amount and the applicable tax rates
        for the current province or territory. It raises an `InvalidDollarAmount` exception if the input amount is invalid.

        Args:
            amount (float): The amount to calculate sales tax on.

        Returns:
            SalesTaxEstimate: An object containing detailed information about the calculated sales tax, including
                            GST, PST, HST, total tax, and the after-tax total.

        Raises:
            InvalidDollarAmount: If the provided amount is negative, `None`, or cannot be converted to a valid decimal.
        """
        amount = self._decimalize(amount)
        gst_total = (amount * percent_to_decimal(self.tax_rate.GST)).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP) if self.tax_rate.GST else Decimal('0.00')
        pst_total = (amount * percent_to_decimal(self.tax_rate.PST)).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP) if self.tax_rate.PST else Decimal('0.00')
        hst_total = (amount * percent_to_decimal(self.tax_rate.HST)).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP) if self.tax_rate.HST else Decimal('0.00')
        qst_total = (amount * percent_to_decimal(self.tax_rate.QST)).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP) if self.tax_rate.HST else Decimal('0.00')
        tax_total = (gst_total + pst_total + hst_total + qst_total).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
        after_tax_total = (amount + tax_total).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
        return SalesTaxEstimate(
            province=self.province,
            before_tax_total=amount,
            tax_total=tax_total,
            after_tax_total=after_tax_total,
            gst_total=gst_total,
            pst_total=pst_total,
            hst_total=hst_total,
            qst_total=qst_total,
        )