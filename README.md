# 🇨🇦 Canatax – The Canadian Tax Calculator

[![PyPI - Version](https://img.shields.io/pypi/v/typed-api-response.svg)](https://pypi.org/project/canatax/)
[![PyPI - Downloads](https://img.shields.io/pypi/dm/canatax.svg)](https://pypi.org/project/canatax/)

**Canatax** is a dependency-free Python package for estimating **Canadian income** and **sales taxes**, including all federal and provincial deductions. It supports **CPP, EI, QPIP, QPP**, and automatically applies **GST, PST, HST, or QST** based on the province or territory.

📦 Zero dependencies.  
🧮 This package uses **2025** tax rates and brackets


## 🚀 Features

### Income Tax Calculation
- Calculates:
  - **Federal tax**
  - **Provincial/territorial tax**
  - **CPP or QPP** (based on province)
  - **EI or EI (Quebec)**
  - **QPIP** (Quebec parental leave)
- Returns a structured `IncomeTaxEstimate` with:
  - Individual line items
  - Total deductions
  - Net after-tax income

### Sales Tax Estimation
- Calculates:
  - **GST**, **PST**, **HST**, and **QST**
- Returns a `SalesTaxEstimate` with:
  - Breakdown by tax type
  - Total tax
  - After-tax amount


## 📦 Installation

```bash
pip install canatax
```


## 💼 Usage

### Income Tax

```python
from canatax import IncomeTaxCalculator

estimate = IncomeTaxCalculator.calculate(income=80000, province="BC")

print(estimate.province)
print(estimate.federal_tax)
print(estimate.provincial_tax)
print(estimate.cpp)
print(estimate.qpp)
print(estimate.qpip)
print(estimate.ei)
print(estimate.total_tax)
print(estimate.net_income)
```

### Sales Tax

```python
from canatax import SalesTaxCalculator

estimate = SalesTaxCalculator.calculate(amount=100.00, province="QC")

print(estimate.province)
print(estimate.gst)
print(estimate.qst)
print(estimate.pst)
print(estimate.hst)
print(estimate.tax_total)
print(estimate.after_tax)
print(estimate.before_tax)
```


## 📘 API Overview

- `IncomeTaxCalculator.calculate(income, province)`  
  → returns `IncomeTaxEstimate`
- `SalesTaxCalculator.calculate(amount, province)`  
  → returns `SalesTaxEstimate`

Both calculators also support manual instantiation with `._calculate()` as an instance method if preferred.


## 🤝 Contributing

Bug fixes and suggestions are welcome! Open an issue or submit a pull request.


## 🔒 License

MIT – Free for personal or commercial use. Go nuts.


## ☕ Support

If you found this useful and want to support future development,  
you can [buy me a coffee](https://www.buymeacoffee.com/FirstFlush). It helps keep the lights on and the tax brackets fresh.