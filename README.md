# Outremer Projet: Firm Analysis and Entrepreneurial Dynamics in Martinique

## Overview
This project analyzes firm characteristics and entrepreneurial dynamics in Martinique using comprehensive enterprise data from 2011-2025. The analysis examines firm age distributions, category compositions, sector breakdowns (NACE 1-digit and 2-digit classifications), geographic concentrations, and turnover trends by firm category to understand entrepreneurial patterns and firm evolution in the region.

## Data Source
The data is sourced from CapFinancials, providing comprehensive financial and organizational information on firms in Martinique. The dataset includes over 867,000 firms with variables such as creation dates, categories (SME, Intermediate, Large), sectors (NACE codes), locations, and financial metrics.

## Files
- `analyze_entrepreneurship.py`: Python script that loads the data and generates analysis and graphs.
- `data_martinique.dta`: Main dataset (Stata format) - not included in repository.
- `data_description_martinique.tex`: Detailed description of the dataset variables and statistics.
- Generated graphs:
  - `enterprises_by_age.png`: Line chart of enterprise distribution by firm age (2025 - creation year).
  - `enterprise_categories.png`: Bar chart of enterprise distribution by category (%).
  - `sectors_2digit.png`: Bar chart of enterprise distribution by NACE 2-digit sectors (%).
  - `sectors_1digit.png`: Bar chart of enterprise distribution by NACE 1-digit sectors (%).
  - `turnover_by_category_year.png`: Line chart of median turnover by category (2011-2022).
  - `gender_distribution.png`: Pie chart of gender distribution of firm leaders.
  - `martinique_choropleth.png`: Choropleth map of firm concentrations by municipality.

## Key Findings
- Firm age distribution shows most firms are young, with peaks at 4-5 years old.
- Firm composition: 98.25% PME (small and medium firms), 1.43% Intermediate, 0.26% Large.
- Sector distribution highlights construction, health/social work, water supply, and real estate as dominant.
- Geographic concentration is highest in Fort-de-France.
- Gender distribution of firm leaders: 55.8% unknown (missing or unrecognized names); among identified: 75.4% male, 24.6% female.
- Turnover dynamics show significant variation by firm category.

## Requirements
- Python 3.x
- pandas
- matplotlib
- geopandas
- folium
- requests
- gender-guesser

## How to Run
1. Ensure `data_martinique.dta` is in the project directory.
2. Run `python analyze_entrepreneurship.py` to generate the analysis and graphs.

## Limitations
Many firms are individual entrepreneurs with incomplete financial data. Analysis focuses on unique firms identified by SIREN for accurate representation.