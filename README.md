# Outremer Projet: Entrepreneurship Analysis in Martinique

## Overview
This project analyzes entrepreneurship activity in Martinique using enterprise data from 2011-2025. The analysis focuses on enterprise creation trends, category distributions, sector breakdowns, and geographic concentrations to evaluate entrepreneurial dynamics in the region.

## Data Source
The data is sourced from CapFinancials, providing comprehensive financial and organizational information on enterprises in Martinique. The dataset includes over 867,000 enterprises with variables such as creation dates, categories (PME, ETI, GE), sectors, locations, and financial metrics.

## Files
- `analyze_entrepreneurship.py`: Python script that loads the data and generates analysis and graphs.
- `data_martinique.dta`: Main dataset (Stata format).
- `data_description_martinique.tex`: Detailed description of the dataset variables and statistics.
- Generated graphs:
  - `enterprises_created_per_year.png`: Bar chart of enterprise creations by year.
  - `enterprise_categories.png`: Pie chart of enterprise distribution by category.
  - `top_sectors.png`: Top 10 sectors by enterprise count.
  - `top_communes.png`: Top 10 communes by enterprise count.

## Key Findings
- Enterprise creations peaked in 2021 (88,106 new enterprises).
- 98.35% of enterprises are PME (small and medium enterprises).
- Top sectors include equipment leasing, real estate, healthcare, and consulting.
- Fort-de-France concentrates the majority of enterprises.

## Requirements
- Python 3.x
- pandas
- matplotlib

## How to Run
1. Ensure `data_martinique.dta` is in the project directory.
2. Run `python analyze_entrepreneurship.py` to generate the analysis and graphs.

## Limitations
The dataset has missing values for many financial variables, limiting quantitative analyses like productivity estimation. It is best suited for qualitative insights into enterprise structures and distributions.