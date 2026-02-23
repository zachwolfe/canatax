import unittest

from canatax.enums import TaxType, ProvinceOrTerritory
from canatax.calculators.base_calculator import BaseCalculator
from canatax.rates.income.current_tax import ProvincialIncomeTaxRate
from canatax.rates.sales.current_sales_tax import BaseSalesTaxRate


class TestBaseCalculator(unittest.TestCase):

    def test_tax_rate(self):
        for tax_type in TaxType:
            for province in ProvinceOrTerritory:
                for year in (2024, 2025):
                    with self.subTest(tax_type=tax_type, province=province, year=year):
                        calculator = BaseCalculator(province=province, year=year)
                        match tax_type:
                            case TaxType.INCOME:
                                self.assertIsNotNone(calculator._get_tax_rate(tax_type))
                            case TaxType.SALES:
                                self.assertIsInstance(calculator._get_tax_rate(tax_type), BaseSalesTaxRate)
                            case _:
                                self.fail(f"Unexpected tax type `{tax_type}` or province `{province}`")


if __name__ == '__main__':
    unittest.main()
