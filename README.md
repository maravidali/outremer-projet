# Outremer Projet: Entrepreneurship Analysis in Martinique

## Overview
This project analyzes entrepreneurship activity in Martinique using enterprise data from 2011-2025. The analysis focuses on enterprise age distribution, category distributions, sector breakdowns (NACE 1-digit and 2-digit), geographic concentrations, and turnover trends by category to evaluate entrepreneurial dynamics in the region.

## Data Source
The data is sourced from CapFinancials, providing comprehensive financial and organizational information on enterprises in Martinique. The dataset includes over 867,000 enterprises with variables such as creation dates, categories (PME, ETI, GE), sectors (NACE codes), locations, and financial metrics.

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
  - `martinique_choropleth.png`: Choropleth map of enterprise concentrations by commune.

## Key Findings
- Most enterprises are young, with peaks at ages 4-5 years.
- 98.25% of enterprises are PME (small and medium enterprises), 1.43% Intermediate, 0.26% Large.
- Top sectors include construction, health/social work, water supply, and real estate.
- Fort-de-France has the highest concentration of enterprises.
- Turnover varies significantly by category, with Large enterprises exhibiting greater variation over the years.

## Requirements
- Python 3.x
- pandas
- matplotlib
- geopandas
- folium
- requests

## How to Run
1. Ensure `data_martinique.dta` is in the project directory.
2. Run `python analyze_entrepreneurship.py` to generate the analysis and graphs.

## Limitations
Most enterprises are individuals with missing financial data. Analysis uses unique firms by SIREN.