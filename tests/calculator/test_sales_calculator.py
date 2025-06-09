from decimal import Decimal
import unittest
from unittest.mock import patch, PropertyMock
from canatax import InvalidDollarAmount
from canatax.enums import ProvinceOrTerritory
from canatax.calculators import SalesTaxCalculator
from canatax.tax_estimate import SalesTaxEstimate


class TestSalesTaxRates(unittest.TestCase):
    ...


class TestSalesTaxCalculator(unittest.TestCase):
    

    def test_calculate_return_type(self):

        for province in ProvinceOrTerritory:
            with self.subTest(province=province):
                calculator = SalesTaxCalculator(province)
                tax_estimate = calculator._calculate(1000)
                self.assertIsInstance(tax_estimate, SalesTaxEstimate)

    def test_valid_amounts(self):

        amounts = [0, 100, 1000000, 95385923235223, 25.54, 25.54385753, 0.01]
        for amount in amounts:
            with self.subTest(amount=amount):
                tax_estimate = SalesTaxCalculator.calculate(amount, "BC")
                self.assertIsInstance(tax_estimate, SalesTaxEstimate)

    def test_invalid_amounts(self):
        amounts = [-100, None, 'fifty_bucks', float('inf')]
        for amount in amounts:
            with self.subTest(amount=amount):
                with self.assertRaises(expected_exception=InvalidDollarAmount):
                    SalesTaxCalculator.calculate(amount, "BC")

    # def test_calculate_return_values(self):
    #     """Test that the SalesTaxCalculator correctly calculates sales 
    #     tax and returns the expected SalesTaxEstimate values.
    #     """
 
 
    from canatax.rates.sales.base import BaseSalesTaxRate

    @patch('canatax.rates.sales.base.BaseSalesTaxRate.GST', new_callable=PropertyMock)
    @patch('canatax.rates.sales.base.BaseSalesTaxRate.PST', new_callable=PropertyMock)
    @patch('canatax.rates.sales.base.BaseSalesTaxRate.HST', new_callable=PropertyMock)
    def test_calculate_with_mocked_tax_rates(self, mock_hst, mock_pst, mock_gst):
        """Test the SalesTaxCalculator with mocked GST, PST, and HST values."""
        mock_gst.return_value = Decimal('5')
        mock_pst.return_value = Decimal('7')
        mock_hst.return_value = Decimal('0')

        province = ProvinceOrTerritory.BRITISH_COLUMBIA
        input_amount = 100
        expected = {
            'before_tax_total': Decimal('100.00'),
            'gst_total': Decimal('5.00'),
            'pst_total': Decimal('7.00'),
            'hst_total': Decimal('0.00'),
            'tax_total': Decimal('12.00'),
            'after_tax_total': Decimal('112.00'),
        }

        tax_estimate = SalesTaxCalculator.calculate(input_amount, province)

        self.assertEqual(tax_estimate.before_tax_total, expected['before_tax_total'])
        self.assertEqual(tax_estimate.gst_total, expected['gst_total'])
        self.assertEqual(tax_estimate.pst_total, expected['pst_total'])
        self.assertEqual(tax_estimate.hst_total, expected['hst_total'])
        self.assertEqual(tax_estimate.tax_total, expected['tax_total'])
        self.assertEqual(tax_estimate.after_tax_total, expected['after_tax_total'])





if __name__ == '__main__':
    unittest.main()