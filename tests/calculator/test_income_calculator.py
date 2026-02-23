import unittest

from canatax.calculators import IncomeTaxCalculator
from canatax.enums import ProvinceOrTerritory
from canatax.exc import InvalidDollarAmount
from canatax.tax_estimate import IncomeTaxEstimate
from canatax.rates.income.current_tax import *



class TestIncomeCalculator(unittest.TestCase):

    def test_calculate_return_type(self):
        income = 100000
        for year in (2024, 2025):
            for province in ProvinceOrTerritory:
                with self.subTest(province=province, year=year):
                    calc = IncomeTaxCalculator(employment_income=income, self_employment_income=0, province=province, year=year)
                    tax_estimate = calc._calculate()
                    self.assertIsInstance(tax_estimate, IncomeTaxEstimate)


    def test_valid_incomes(self):
        valid_incomes = [0, 1, 0.1, 0.0001, 10, 100000, 95439534942239, 2552.45, 25235.523523]
        for year in (2024, 2025):
            for income in valid_incomes:
                with self.subTest(income=income, year=year):
                    calc = IncomeTaxCalculator.calculate(employment_income=income, self_employment_income=0, province="BC", year=year)
                    self.assertIsInstance(calc, IncomeTaxEstimate)


    def test_invalid_incomes(self):
        invalid_incomes = [-23525, None, 'asdf', float('inf'), float('nan')]
        for year in (2024, 2025):
            for income in invalid_incomes:
                with self.subTest(income=income, year=year):
                    with self.assertRaises(InvalidDollarAmount):
                        calc = IncomeTaxCalculator.calculate(employment_income=income, self_employment_income=0, province="BC", year=year)


if __name__ == '__main__':
    unittest.main()