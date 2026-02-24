from decimal import Decimal
from canatax.rates.income.base import BaseIncomeTaxRate, ProvincialIncomeTaxRate

# 2025 Provincial and federal tax rates:
# ----
# https://www.canada.ca/en/revenue-agency/services/tax/individuals/frequently-asked-questions-individuals/canadian-income-tax-rates-individuals-current-previous-years.html
# https://www.revenuquebec.ca/en/citizens/income-tax-return/completing-your-income-tax-return/income-tax-rates/


class FederalIncomeTaxRate(BaseIncomeTaxRate):
    """
    14.5% 	on the portion of taxable income that is $57,375 or less, plus
    20.5% 	on the portion of taxable income over $57,375 up to $114,750, plus
    26% 	on the portion of taxable income over $114,750 up to $177,882, plus
    29% 	on the portion of taxable income over $177,882 up to $253,414, plus
    33% 	on the portion of taxable income over $253,414
    """

    _BPA_MIN = Decimal(14538) # https://www.canada.ca/en/revenue-agency/services/forms-publications/payroll/t4032-payroll-deductions-tables/t4032on-jan/t4032on-january-general-information.html
    _BPA_MAX = Decimal(16129)
    _BPA_PHASE_OUT_START = Decimal("177882")
    _BPA_PHASE_OUT_END = Decimal("253414")

    brackets = [
        (14.5, 57375),
        (20.5, 114750),
        (26, 177882),
        (29, 253414),
        (33, float('inf')),
    ]

    @classmethod
    def get_bpa(cls, income: Decimal) -> Decimal:
        if income <= cls._BPA_PHASE_OUT_START:
            bpa = cls._BPA_MAX
        elif income >= cls._BPA_PHASE_OUT_END:
            bpa = cls._BPA_MIN
        else:
            reduction_ratio = ((income - cls._BPA_PHASE_OUT_START) / (cls._BPA_PHASE_OUT_END - cls._BPA_PHASE_OUT_START))
            bpa = cls._BPA_MAX - (reduction_ratio * (cls._BPA_MAX - cls._BPA_MIN))
        return bpa


class AlbertaIncomeTaxRate(ProvincialIncomeTaxRate):
    """
    10% 	on the portion of taxable income that is $151,234 or less, plus
    12% 	on the portion of taxable income over $151,234 up to $181,481, plus
    13% 	on the portion of taxable income over $181,481 up to $241,974, plus
    14% 	on the portion of taxable income over $241,974 up to $362,961, plus
    15% 	on the portion of taxable income over $362,961
    """

    @classmethod
    def get_bpa(cls, income):
        return Decimal("22323")

    brackets = [
        (10, 151234),
        (12, 181481),
        (13, 241974),
        (14, 362961),
        (15, float('inf')),
    ]


class BritishColumbiaIncomeTaxRate(ProvincialIncomeTaxRate):
    """
    5.06% 	on the portion of taxable income that is $49,279 or less, plus
    7.7% 	on the portion of taxable income over $49,279 up to $98,560, plus
    10.5% 	on the portion of taxable income over $98,560 up to $113,158, plus
    12.29% 	on the portion of taxable income over $113,158 up to $137,407, plus
    14.7% 	on the portion of taxable income over $137,407 up to $186,306, plus
    16.8% 	on the portion of taxable income over $186,306 up to $259,829, plus
    20.5% 	on the portion of taxable income over $259,829
    """

    @classmethod
    def get_bpa(cls, income):
        return Decimal("12932")

    brackets = [
        (5.06, 49279),
        (7.7, 98560),
        (10.5, 113158),
        (12.29, 137407),
        (14.7, 186306),
        (16.8, 259829),
        (20.5, float('inf')),
    ]


class ManitobaIncomeTaxRate(ProvincialIncomeTaxRate):
    """
    10.8% 	on the portion of taxable income that is $47,564 or less, plus
    12.75% 	on the portion of taxable income over $47,564 up to $101,200, plus
    17.4% 	on the portion of taxable income over $101,200
    """

    _BPA_MIN = Decimal(0)
    _BPA_MAX = Decimal(15780)
    _BPA_PHASE_OUT_START = Decimal("200000")
    _BPA_PHASE_OUT_END = Decimal("400000")

    brackets = [
        (10.8, 47564),
        (12.75, 101200),
        (17.4, float('inf')),
    ]

    @classmethod
    def get_bpa(cls, income: Decimal) -> Decimal:
        if income <= cls._BPA_PHASE_OUT_START:
            bpa = cls._BPA_MAX
        elif income >= cls._BPA_PHASE_OUT_END:
            bpa = cls._BPA_MIN
        else:
            reduction_ratio = ((income - cls._BPA_PHASE_OUT_START) / (cls._BPA_PHASE_OUT_END - cls._BPA_PHASE_OUT_START))
            bpa = cls._BPA_MAX - (reduction_ratio * (cls._BPA_MAX - cls._BPA_MIN))
        return bpa

    @classmethod
    def get_bpa(cls, income):
        income = Decimal(income)
        if income <= cls._BPA_PHASE_OUT_START:
            return cls._BPA_MAX
        elif income >= cls._BPA_PHASE_OUT_END:
            return cls._BPA_MIN
        else:
            reduction_ratio = ((income - cls._BPA_PHASE_OUT_START) / (cls._BPA_PHASE_OUT_END - cls._BPA_PHASE_OUT_START))
            bpa = cls._BPA_MAX - (reduction_ratio * (cls._BPA_MAX - cls._BPA_MIN))
            return bpa

class NewBrunswickIncomeTaxRate(ProvincialIncomeTaxRate):
    """
    9.4% 	on the portion of taxable income that is $51,306 or less, plus
    14% 	on the portion of taxable income over $51,306 up to $102,614, plus
    16% 	on the portion of taxable income over $102,614 up to $190,060, plus
    19.5% 	on the portion of taxable income over $190,060
    """

    @classmethod
    def get_bpa(cls, income):
        return Decimal("13396")

    brackets = [
        (9.4, 51306),
        (14, 102614),
        (16, 190060),
        (19.5, float('inf')),
    ]


class NewfoundlandIncomeTaxRate(ProvincialIncomeTaxRate):
    """
    8.7% 	on the portion of taxable income that is $44,192 or less, plus
    14.5% 	on the portion of taxable income over $44,192 up to $88,382, plus
    15.8% 	on the portion of taxable income over $88,382 up to $157,792, plus
    17.8% 	on the portion of taxable income over $157,792 up to $220,910, plus
    19.8% 	on the portion of taxable income over $220,910 up to $282,214, plus
    20.8% 	on the portion of taxable income over $282,214 up to $564,429, plus
    21.3% 	on the portion of taxable income over $564,429 up to $1,128,858, plus
    21.8% 	on the portion of taxable income over $1,128,858
    """

    @classmethod
    def get_bpa(cls, income):
        return Decimal("10808")

    brackets = [
        (8.7, 44192),
        (14.5, 88382),
        (15.8, 157792),
        (17.8, 220910),
        (19.8, 282214),
        (20.8, 564429),
        (21.3, 1128858),
        (21.8, float('inf')),
    ]


class NorthwestTerritoriesIncomeTaxRate(ProvincialIncomeTaxRate):
    """
    5.9% 	on the portion of taxable income that is $51,964 or less, plus
    8.6% 	on the portion of taxable income over $51,964 up to $103,930, plus
    12.2% 	on the portion of taxable income over $103,930 up to $168,967, plus
    14.05% 	on the portion of taxable income over $168,967
    """

    @classmethod
    def get_bpa(cls, income):
        return Decimal("15705")

    brackets = [
        (5.9, 51964),
        (8.6, 103930),
        (12.2, 168967),
        (14.05, float('inf')),
    ]


class NovaScotiaIncomeTaxRate(ProvincialIncomeTaxRate):
    """
    8.79% 	on the portion of taxable income that is $30,507 or less, plus
    14.95% 	on the portion of taxable income over $30,507 up to $61,015, plus
    16.67% 	on the portion of taxable income over $61,015 up to $95,883, plus
    17.5% 	on the portion of taxable income over $95,883 up to $154,650, plus
    21% 	on the portion of taxable income over $154,650
    """

    @classmethod
    def get_bpa(cls, income):
        return Decimal("14744")

    brackets = [
        (8.79, 30507),
        (14.95, 61015),
        (16.67, 95883),
        (17.5, 154650),
        (21, float('inf')),
    ]


class NunavutIncomeTaxRate(ProvincialIncomeTaxRate):
    """
    4% 	on the portion of taxable income that is $54,707 or less, plus
    7% 	on the portion of taxable income over $54,707 up to $109,413, plus
    9% 	on the portion of taxable income over $109,413 up to $177,881, plus
    11.5% 	on the portion of taxable income over $177,881
    """

    @classmethod
    def get_bpa(cls, income):
        return Decimal("18767")

    brackets = [
        (4, 54707),
        (7, 109413),
        (9, 177881),
        (11.5, float('inf')),
    ]


class OntarioIncomeTaxRate(ProvincialIncomeTaxRate):
    """
    5.05% 	on the portion of taxable income that is $52,886 or less, plus
    9.15% 	on the portion of taxable income over $52,886 up to $105,775, plus
    11.16% 	on the portion of taxable income over $105,775 up to $150,000, plus
    12.16% 	on the portion of taxable income over $150,000 up to $220,000, plus
    13.16% 	on the portion of taxable income over $220,000
    """

    @classmethod
    def get_bpa(cls, income):
        return Decimal("12399")

    brackets = [
        (5.05, 52886),
        (9.15, 105775),
        (11.16, 150000),
        (12.16, 220000),
        (13.16, float('inf')),
    ]


class PEIIncomeTaxRate(ProvincialIncomeTaxRate):
    """
    9.5% 	on the portion of taxable income that is $33,328 or less, plus
    13.47% 	on the portion of taxable income over $33,328 up to $64,656, plus
    16.6% 	on the portion of taxable income over $64,656 up to $105,000, plus
    17.62% 	on the portion of taxable income over $105,000 up to $140,000, plus
    19% 	on the portion of taxable income over $140,000
    """

    @classmethod
    def get_bpa(cls, income):
        return Decimal("15050")

    brackets = [
        (9.5, 33328),
        (13.47, 64656),
        (16.6, 105000),
        (17.62, 140000),
        (19, float('inf')),
    ]


class QuebecIncomeTaxRate(ProvincialIncomeTaxRate):
    """
    $53,255 or less	14%
    More than $53,255 but not more than $106,495	19%
    More than $106,495 but not more than $129,590	24%
    More than $129,590	25.75%
    """

    @classmethod
    def get_bpa(cls, income):
        return Decimal("18056")

    brackets = [
        (14, 53255),
        (19, 106495),
        (24, 129590),
        (25.75, float('inf')),
    ]


class SaskatchewanIncomeTaxRate(ProvincialIncomeTaxRate):
    """
    10.5% 	on the portion of taxable income that is $53,463 or less, plus
    12.5% 	on the portion of taxable income over $53,463 up to $152,750, plus
    14.5% 	on the portion of taxable income over $152,750
    """

    BPA = 18491 # https://turbotax.intuit.ca/tips/saskatchewan-provincial-taxes-and-credits-5062

    brackets = [
        (10.5, 53463),
        (12.5, 152750),
        (14.5, float('inf')),
    ]


class YukonIncomeTaxRate(ProvincialIncomeTaxRate):
    """
    6.4% 	on the portion of taxable income that is $57,375 or less, plus
    9% 	on the portion of taxable income over $57,375 up to $114,750, plus
    10.9% 	on the portion of taxable income over $114,750 up to $177,882, plus
    12.8% 	on the portion of taxable income over $177,882 up to $500,000, plus
    15% 	on the portion of taxable income over $500,000
    """

    BPA = 15705 # Yes, same as the fed. Not a typo. https://turbotax.intuit.ca/tips/yukon-territorial-taxes-and-credits-5066

    brackets = [
        (6.4, 57375),
        (9, 114750),
        (10.9, 177882),
        (12.8, 500000),
        (15, float('inf')),
    ]