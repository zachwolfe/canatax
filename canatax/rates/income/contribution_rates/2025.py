from ..base import BaseContribution

# 2025
#
# CPP:
# https://www.canada.ca/en/revenue-agency/news/newsroom/tax-tips/tax-tips-2024/canada-revenue-agency-announces-maximum-pensionable-earnings-contributions-2025.html
#
# EI:
# https://www.canada.ca/en/revenue-agency/services/tax/businesses/topics/payroll/payroll-deductions-contributions/employment-insurance-ei/ei-premium-rates-maximums.html
#
# QPP:
#

class EI(BaseContribution):

    rate = 1.64
    max_earnings = 65700


class CPP(BaseContribution):

    rate = 5.95
    max_earnings = 71300
    exemption = 3500

    cpp2_rate = 4.00
    cpp2_min = 73200
    cpp_max = 81200


class QPP(BaseContribution):
    
    rate = 5.40
    max_earnings = 73200
    exemption = 3500
    
    qpp2_rate = 4.00
    qpp2_min = 73200
    qpp2_max = 82700