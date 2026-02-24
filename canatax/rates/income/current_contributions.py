
class Contributions:
    def __init__(self, year: int = 2025):
        if int(year) == 2025:
            from .contribution_rates.rates_2025 import CPP, EI, QPP, QPIP, EIQuebec
            self.cpp = CPP()
            self.ei = EI()
            self.ei_quebec = EIQuebec()
            self.qpp = QPP()
            self.qpip = QPIP()
        elif int(year) == 2024:
            from .contribution_rates.rates_2024 import CPP, EI, QPP, QPIP, EIQuebec
            self.cpp = CPP()
            self.ei = EI()
            self.ei_quebec = EIQuebec()
            self.qpp = QPP()
            self.qpip = QPIP()
        else:
            raise NotImplementedError(f"Contribution rates for year {year} not implemented.")
