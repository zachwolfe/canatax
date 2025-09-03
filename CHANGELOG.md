## [2.0.1] - 2025-09-03

### Fixed
- Implemented Basic Personal Amount (BPA) calculations for federal and provincial taxes
- Federal BPA now includes proper phase-out calculation for high income earners ($173,205 - $246,752 range)
- Added BPA deduction from taxable income before applying tax brackets

### Note
This was a critical bug fix - previous versions calculated taxes without accounting for basic personal amounts, resulting in overstated tax liabilities.


## [2.0.0] – 2025-06-08

- Refactored `IncomeTaxCalculator` and `SalesTaxCalculator` to use `.calculate()` classmethods
- Added QPIP, QPP support, and Quebec EI rate for 2025
- Added QST support for sales tax
- Added CPP2 and QPP2 support
- Improved readme and public API clarity