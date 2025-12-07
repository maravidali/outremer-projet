import pandas as pd
import matplotlib.pyplot as plt
import folium
import requests
import geopandas as gpd
import zipfile
import urllib.request

# Load the data using pandas (more memory efficient for large files)
df = pd.read_stata('data_martinique.dta')

print("Data loaded successfully. Shape:", df.shape)
print("Columns:", df.columns.tolist())

print("\nFirst 5 rows:")
print(df.head())

# Convert creation date to datetime
df['Datedecréation'] = pd.to_datetime(df['Datedecréation'], errors='coerce')
df['creation_year'] = df['Datedecréation'].dt.year

# Get unique firms by SIREN (first occurrence for creation year)
df_unique = df.drop_duplicates(subset='SIREN', keep='first')

# Aggregate commune data for map
commune_agg = df_unique.groupby('CodecommuneINSEE').agg({'SIREN':'count'}).rename(columns={'SIREN':'count'})
commune_agg.index = commune_agg.index.astype(int).astype(str)

# Calculate total unique enterprises
total_unique = df_unique.shape[0]

# Entrepreneurship activity: Number of enterprises by age (2025 - creation_year)
df_unique['firm_age'] = 2025 - df_unique['creation_year']
age_counts = df_unique.groupby('firm_age').size().sort_index()
print("\nNumber of enterprises by age (unique SIREN):")
print(age_counts)

# Distribution by enterprise category (unique firms)
print("\nDistribution by enterprise category (unique firms, %):")
category_percent = df_unique['Catégoriedentreprise'].value_counts(normalize=True) * 100
category_percent.index = category_percent.index.map({'PME': 'SME', 'ETI': 'Intermediate', 'GE': 'Large'})
category_percent = category_percent[category_percent.index.notna()]
print(category_percent)


# Percentage of unique enterprises by 2-digit sector
print("\nPercentage of unique enterprises by 2-digit sector:")
df_unique['sector_2digit'] = df_unique['CodeAPE'].astype(str).str[:2]
sector_2digit_counts = df_unique.groupby('sector_2digit').size()
sector_2digit_percent = (sector_2digit_counts / total_unique) * 100

# Map to sector names
sector_names = {
    '01': 'Agriculture, hunting, forestry',
    '02': 'Forestry, logging and related service activities',
    '05': 'Fishing, fish farming',
    '10': 'Mining of coal and lignite; peat',
    '11': 'Extraction of crude petroleum and natural gas; service activities',
    '13': 'Mining of metal ores',
    '14': 'Other mining and quarrying',
    '15': 'Manufacture of food products and beverages',
    '16': 'Manufacture of tobacco products',
    '17': 'Manufacture of textiles',
    '18': 'Manufacture of wearing apparel; dressing and dyeing of fur',
    '19': 'Tanning and dressing of leather; manufacture of luggage',
    '20': 'Manufacture of wood and of products of wood and cork',
    '21': 'Manufacture of pulp, paper and paper products',
    '22': 'Publishing, printing and reproduction of recorded media',
    '23': 'Manufacture of coke, refined petroleum products and nuclear fuel',
    '24': 'Manufacture of chemicals and chemical products',
    '25': 'Manufacture of rubber and plastic products',
    '26': 'Manufacture of other non-metallic mineral products',
    '27': 'Manufacture of basic metals',
    '28': 'Manufacture of fabricated metal products',
    '29': 'Manufacture of machinery and equipment n.e.c.',
    '30': 'Manufacture of office machinery and computers',
    '31': 'Manufacture of electrical machinery and apparatus n.e.c.',
    '32': 'Manufacture of radio, television and communication equipment',
    '33': 'Manufacture of medical, precision and optical instruments',
    '34': 'Manufacture of motor vehicles, trailers and semi-trailers',
    '35': 'Manufacture of other transport equipment',
    '36': 'Manufacture of furniture; manufacturing n.e.c.',
    '37': 'Recycling',
    '40': 'Electricity, gas, steam and hot water supply',
    '41': 'Collection, purification and distribution of water',
    '45': 'Construction',
    '50': 'Sale, maintenance and repair of motor vehicles',
    '51': 'Wholesale trade and commission trade',
    '52': 'Retail trade, except of motor vehicles',
    '55': 'Hotels and restaurants',
    '60': 'Land transport; transport via pipelines',
    '61': 'Water transport',
    '62': 'Air transport',
    '63': 'Supporting and auxiliary transport activities',
    '64': 'Post and telecommunications',
    '65': 'Financial intermediation',
    '66': 'Insurance and pension funding',
    '67': 'Activities auxiliary to financial intermediation',
    '70': 'Real estate activities',
    '71': 'Renting of machinery and equipment',
    '72': 'Computer and related activities',
    '73': 'Research and development',
    '74': 'Other business activities',
    '75': 'Public administration and defence',
    '80': 'Education',
    '85': 'Health and social work',
    '90': 'Sewage and refuse disposal, sanitation and similar activities',
    '91': 'Activities of membership organizations n.e.c.',
    '92': 'Recreational, cultural and sporting activities',
    '93': 'Other service activities',
    '95': 'Private households with employed persons',
    '96': 'Undifferentiated goods-producing activities of private households',
    '97': 'Undifferentiated service-producing activities of private households',
    '99': 'Extra-territorial organizations and bodies'
}
sector_2digit_percent.index = sector_2digit_percent.index.map(sector_names)
sector_2digit_percent = sector_2digit_percent[sector_2digit_percent.index.notna()]
print(sector_2digit_percent)

# All communes by number of enterprises (unique firms)
commune_counts = df_unique['Ville'].value_counts()

# Generate graphs

# Graph 1: Enterprises by age
plt.figure(figsize=(10,6))
age_counts.plot(kind='line')
plt.title('Number of Enterprises by Age')
plt.xlabel('Firm Age (Years)')
plt.ylabel('Number of Enterprises')
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.savefig('enterprises_by_age.png')
print("Saved: enterprises_by_age.png")

# Graph 2: Distribution by category
plt.figure(figsize=(8,6))
category_percent.plot(kind='bar')
plt.title('Distribution of Enterprises by Category (Unique Firms, %)')
plt.xlabel('Category')
plt.ylabel('Percentage')
plt.xticks(rotation=90)
plt.savefig('enterprise_categories.png')
print("Saved: enterprise_categories.png")

# Graph 3: Percentage by 2-digit sector
plt.figure(figsize=(16,10))
sector_2digit_percent.plot(kind='bar')
plt.title('Percentage of Unique Enterprises by NACE 2-Digit Sector')
plt.xlabel('Sector')
plt.ylabel('Percentage')
plt.xticks(rotation=90)
plt.tight_layout()
plt.savefig('sectors_2digit.png')
print("Saved: sectors_2digit.png")

# Graph 5: Percentage by 1-digit sector
df_unique['sector_1digit'] = df_unique['CodeAPE'].astype(str).str[0]
sector_1digit_counts = df_unique.groupby('sector_1digit').size()
sector_1digit_percent = (sector_1digit_counts / total_unique) * 100

sector_1digit_names = {
    '0': 'Agriculture, hunting and forestry',
    '1': 'Fishing',
    '2': 'Mining and quarrying',
    '3': 'Manufacturing',
    '4': 'Electricity, gas and water supply',
    '5': 'Construction',
    '6': 'Wholesale and retail trade; repair',
    '7': 'Hotels and restaurants',
    '8': 'Transport, storage and communication',
    '9': 'Financial intermediation; real estate; other services'
}
sector_1digit_percent.index = sector_1digit_percent.index.map(sector_1digit_names)
sector_1digit_percent = sector_1digit_percent[sector_1digit_percent.index.notna()]

plt.figure(figsize=(16,8))
sector_1digit_percent.plot(kind='bar')
plt.title('Percentage of Unique Enterprises by NACE 1-Digit Sector')
plt.xlabel('Sector')
plt.ylabel('Percentage')
plt.xticks(rotation=0)
plt.tight_layout()
plt.savefig('sectors_1digit.png')
print("Saved: sectors_1digit.png")

# Graph 6: Median turnover by category over years (2011-2025)
df_years = df_unique[(df_unique['year'] >= 2011) & (df_unique['year'] <= 2022)]
turnover_by_year_cat = df_years.groupby(['year', 'Catégoriedentreprise'])['Chiffredaffaires'].median().unstack()
turnover_by_year_cat.columns = turnover_by_year_cat.columns.map({'PME': 'SME', 'ETI': 'Intermediate', 'GE': 'Large'})
turnover_by_year_cat = turnover_by_year_cat.dropna(axis=1, how='all')
turnover_by_year_cat = turnover_by_year_cat.fillna(method='ffill')

fig, ax1 = plt.subplots(figsize=(12,8))
turnover_by_year_cat[['SME', 'Intermediate']].plot(ax=ax1, kind='line', marker='o')
ax1.set_ylabel('Median Turnover (SME & Intermediate)')

ax2 = ax1.twinx()
turnover_by_year_cat['Large'].plot(ax=ax2, kind='line', marker='o', color='red')
ax2.set_ylabel('Median Turnover (Large)', color='red')
ax2.tick_params(axis='y', labelcolor='red')

# Combined legend
lines = ax1.get_lines() + ax2.get_lines()
labels = [l.get_label() for l in lines]
ax1.legend(lines, labels, title='Category', loc='upper left')
ax2.legend().set_visible(False)

plt.title('Median Turnover by Enterprise Category (2011-2022)')
plt.xlabel('Year')
plt.grid(True)
plt.tight_layout()
plt.savefig('turnover_by_category_year.png')
print("Saved: turnover_by_category_year.png")
