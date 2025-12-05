import pandas as pd
import matplotlib.pyplot as plt

# Load the data using pandas (more memory efficient for large files)
df = pd.read_stata('data_martinique.dta')

print("Data loaded successfully. Shape:", df.shape)
print("Columns:", df.columns.tolist())

print("\nFirst 5 rows:")
print(df.head())

# Convert creation date to datetime
df['Datedecréation'] = pd.to_datetime(df['Datedecréation'], errors='coerce')
df['creation_year'] = df['Datedecréation'].dt.year

# Entrepreneurship activity: Number of new enterprises per year
creation_counts = df.groupby('creation_year').size().sort_index()
print("\nNumber of enterprises created per year:")
print(creation_counts)

# Distribution by enterprise category
print("\nDistribution by enterprise category:")
print(df['Catégoriedentreprise'].value_counts())

# Average number of employees by category
print("\nAverage number of employees by category:")
avg_employees = df.groupby('Catégoriedentreprise')['employes'].mean()
print(avg_employees)

# Average turnover by category
print("\nAverage turnover (Chiffredaffaires) by category:")
avg_turnover = df.groupby('Catégoriedentreprise')['Chiffredaffaires'].mean()
print(avg_turnover)

# Top 10 sectors by frequency
print("\nTop 10 sectors by frequency:")
sector_counts = df['LibelléAPE'].value_counts().head(10)
print(sector_counts)

# Top 10 communes by number of enterprises
print("\nTop 10 communes by number of enterprises:")
commune_counts = df['Ville'].value_counts().head(10)
print(commune_counts)

# Generate graphs

# Graph 1: Enterprises created per year (2011-2025)
recent_years = creation_counts[creation_counts.index >= 2011]
plt.figure(figsize=(10,6))
recent_years.plot(kind='bar')
plt.title('Number of Enterprises Created per Year (2011-2025)')
plt.xlabel('Year')
plt.ylabel('Number of Enterprises')
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig('enterprises_created_per_year.png')
print("Saved: enterprises_created_per_year.png")

# Graph 2: Distribution by category
category_counts = df['Catégoriedentreprise'].value_counts()
plt.figure(figsize=(8,6))
category_counts.plot(kind='pie', autopct='%1.1f%%')
plt.title('Distribution of Enterprises by Category')
plt.ylabel('')
plt.savefig('enterprise_categories.png')
print("Saved: enterprise_categories.png")

# Graph 3: Top 10 sectors
plt.figure(figsize=(12,8))
sector_counts.plot(kind='barh')
plt.title('Top 10 Sectors by Number of Enterprises')
plt.xlabel('Number of Enterprises')
plt.tight_layout()
plt.savefig('top_sectors.png')
print("Saved: top_sectors.png")

# Graph 4: Top 10 communes
plt.figure(figsize=(12,8))
commune_counts.plot(kind='barh')
plt.title('Top 10 Communes by Number of Enterprises')
plt.xlabel('Number of Enterprises')
plt.tight_layout()
plt.savefig('top_communes.png')
print("Saved: top_communes.png")