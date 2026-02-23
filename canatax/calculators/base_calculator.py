from abc import ABC
from decimal import Decimal, InvalidOperation
from typing import Type

from canatax.enums import *
from canatax.exc import InvalidProvinceError, InvalidDollarAmount

from importlib import import_module
from canatax.rates.sales.base import BaseSalesTaxRate
from canatax.rates.income.current_tax import *



class BaseCalculator(ABC):

    @staticmethod
    def get_income_rate_class(province: ProvinceOrTerritory, year: int = 2025):
        """Dynamically import and return the correct income tax rate class for the province and year."""
        year = int(year)
        if year == 2024:
            mod = import_module('canatax.rates.income.tax_rates.rates_2024')
        else:
            mod = import_module('canatax.rates.income.tax_rates.rates_2025')
        class_map = {
            ProvinceOrTerritory.ALBERTA: mod.AlbertaIncomeTaxRate,
            ProvinceOrTerritory.BRITISH_COLUMBIA: mod.BritishColumbiaIncomeTaxRate,
            ProvinceOrTerritory.MANITOBA: mod.ManitobaIncomeTaxRate,
            ProvinceOrTerritory.ONTARIO: mod.OntarioIncomeTaxRate,
            ProvinceOrTerritory.NEW_BRUNSWICK: mod.NewBrunswickIncomeTaxRate,
            ProvinceOrTerritory.NEWFOUNDLAND: mod.NewfoundlandIncomeTaxRate,
            ProvinceOrTerritory.NORTHWEST_TERRITORIES: mod.NorthwestTerritoriesIncomeTaxRate,
            ProvinceOrTerritory.NOVA_SCOTIA: mod.NovaScotiaIncomeTaxRate,
            ProvinceOrTerritory.NUNAVUT: mod.NunavutIncomeTaxRate,
            ProvinceOrTerritory.PRINCE_EDWARD_ISLAND: mod.PEIIncomeTaxRate,
            ProvinceOrTerritory.QUEBEC: mod.QuebecIncomeTaxRate,
            ProvinceOrTerritory.SASKATCHEWAN: mod.SaskatchewanIncomeTaxRate,
            ProvinceOrTerritory.YUKON: mod.YukonIncomeTaxRate,
        }
        return class_map[province]

    province: ProvinceOrTerritory


    @staticmethod
    def get_sales_rate_class(province: ProvinceOrTerritory, year: int = 2025):
        """Dynamically import and return the correct sales tax rate class for the province and year."""
        year = int(year)
        if year == 2024:
            mod = import_module('canatax.rates.sales.sales_tax_rates.rates_2024')
        else:
            mod = import_module('canatax.rates.sales.sales_tax_rates.rates_2025')
        class_map = {
            ProvinceOrTerritory.ALBERTA: mod.AlbertaSalesTaxRate,
            ProvinceOrTerritory.BRITISH_COLUMBIA: mod.BritishColumbiaSalesTaxRate,
            ProvinceOrTerritory.MANITOBA: mod.ManitobaSalesTaxRate,
            ProvinceOrTerritory.ONTARIO: mod.OntarioSalesTaxRate,
            ProvinceOrTerritory.NEW_BRUNSWICK: mod.NewBrunswickSalesTaxRate,
            ProvinceOrTerritory.NEWFOUNDLAND: mod.NewfoundlandSalesTaxRate,
            ProvinceOrTerritory.NORTHWEST_TERRITORIES: mod.NorthwestTerritoriesSalesTaxRate,
            ProvinceOrTerritory.NOVA_SCOTIA: mod.NovaScotiaSalesTaxRate,
            ProvinceOrTerritory.NUNAVUT: mod.NunavutSalesTaxRate,
            ProvinceOrTerritory.PRINCE_EDWARD_ISLAND: mod.PEISalesTaxRate,
            ProvinceOrTerritory.QUEBEC: mod.QuebecSalesTaxRate,
            ProvinceOrTerritory.SASKATCHEWAN: mod.SaskatchewanSalesTaxRate,
            ProvinceOrTerritory.YUKON: mod.YukonSalesTaxRate,
        }
        return class_map[province]

    def __init__(self, province: str | ProvinceOrTerritory, year: int = 2025):
        """Initializes the calculator with a province or territory.

        Args:
            province (str | ProvinceOrTerritory): The province or territory as a string or an enum.

        Raises:
            InvalidProvinceError: If the province or territory is not valid.
        """
        self.province = self._coerce_province(province)
        self.year = int(year)


    def _coerce_province(self, province: str | ProvinceOrTerritory) -> ProvinceOrTerritory:
        if province is None:
            raise InvalidProvinceError(province)
        if not isinstance(province, ProvinceOrTerritory):
            try:
                return ProvinceOrTerritory(str(province).upper())
            except (ValueError, AttributeError) as e:
                raise InvalidProvinceError(province) from e
        return province

    def _decimalize(self, amount:int|float|Decimal) -> Decimal:
        try:
            decimal_amount = Decimal(amount)
        except (ValueError, TypeError, InvalidOperation) as e:
            raise InvalidDollarAmount(amount) from e
        else:
            if decimal_amount.is_infinite() or decimal_amount.is_nan():
                raise InvalidDollarAmount(amount)
            if decimal_amount < 0:
                raise InvalidDollarAmount(amount)
        return decimal_amount

    def is_quebec(self) -> bool:
        match self.province:
            case ProvinceOrTerritory.QUEBEC:
                return True
            case _:
                return False

    def _get_tax_rate(self, tax_type:TaxType) -> ProvincialIncomeTaxRate | BaseSalesTaxRate:
        if tax_type == TaxType.INCOME:
            klass = self.get_income_rate_class(self.province, self.year)
            return klass()
        elif tax_type == TaxType.SALES:
            klass = self.get_sales_rate_class(self.province, self.year)
            return klass()
        else:
            raise ValueError(f"Invalid param tax_type: `{tax_type}` ")

#  (AlbertaIncomeTaxRate, AlbertaSalesTaxRate),