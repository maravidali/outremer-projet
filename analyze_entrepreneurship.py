import pandas as pd
import matplotlib.pyplot as plt
import folium
import requests
import geopandas as gpd
import zipfile
import urllib.request
import gender_guesser.detector as gender

# Expanded French name lists for better gender detection
french_male = [
    'Jean', 'Pierre', 'Michel', 'Philippe', 'Louis', 'Jacques', 'François', 'Alain', 'Nicolas', 'Patrick', 'Christophe', 'Eric', 'Stéphane', 'David', 'Thomas', 'Daniel', 'Antoine', 'Olivier', 'Sébastien', 'Emmanuel', 'Vincent', 'Laurent', 'Romain', 'Guillaume', 'Julien', 'Benoît', 'Sylvain', 'Fabrice', 'Marc', 'Gilles', 'Bruno', 'Thierry', 'Denis', 'Pascal', 'Christian', 'Bernard', 'André', 'Robert', 'Paul', 'Henri', 'Georges', 'Charles', 'Joseph', 'René', 'Marcel', 'Albert', 'Claude', 'Roger', 'Maurice', 'Raymond', 'Lucien', 'Eugène', 'Léon', 'Victor', 'Edouard', 'Alfred', 'Gustave', 'Jules', 'Emile', 'Auguste', 'Ferdinand', 'Achille', 'Adolphe', 'Alexandre', 'Amédée', 'Anatole', 'Aristide', 'Armand', 'Arthur', 'Augustin', 'Baptiste', 'Basile', 'Baudouin', 'Benjamin', 'Bertrand', 'Boniface', 'Célestin', 'César', 'Clément', 'Constant', 'Cyrille', 'Damien', 'Didier', 'Edmond', 'Elie', 'Ernest', 'Etienne', 'Evariste', 'Félix', 'Fernand', 'Florent', 'Francis', 'Frédéric', 'Gabriel', 'Gaston', 'Gérard', 'Gilbert', 'Godefroy', 'Grégoire', 'Guy', 'Hector', 'Hervé', 'Hilaire', 'Honoré', 'Hubert', 'Hugues', 'Ignace', 'Irénée', 'Isidore', 'Jérémie', 'Jérôme', 'Joachim', 'Justin', 'Lazare', 'Léandre', 'Léonce', 'Léopold', 'Lévi', 'Lionel', 'Loïc', 'Lothaire', 'Luc', 'Ludovic', 'Marin', 'Martin', 'Mathieu', 'Matthieu', 'Maxime', 'Maximilien', 'Médéric', 'Modeste', 'Napoléon', 'Nathan', 'Nestor', 'Noël', 'Octave', 'Onésime', 'Oscar', 'Patrice', 'Prosper', 'Quentin', 'Raoul', 'Raphaël', 'Rémi', 'Richard', 'Roch', 'Rodolphe', 'Roland', 'Roméo', 'Samuel', 'Sauveur', 'Serge', 'Simon', 'Stanislas', 'Théodore', 'Théophile', 'Thibault', 'Timothée', 'Toussaint', 'Urbain', 'Valentin', 'Valère', 'Vivien', 'Xavier', 'Yves', 'Zacharie', 'Adrien', 'Alexis', 'Arnaud', 'Benoit', 'Cedric', 'Clement', 'Damien', 'Dominique', 'Emile', 'Felix', 'Florian', 'Francois', 'Frederic', 'Gregory', 'Henri', 'Hugo', 'Jerome', 'Kevin', 'Laurent', 'Leo', 'Lucas', 'Manuel', 'Matteo', 'Maxence', 'Nathan', 'Nicolas', 'Noah', 'Pierre', 'Remy', 'Romain', 'Ruben', 'Samuel', 'Sebastien', 'Simon', 'Theo', 'Thibaut', 'Timothee', 'Tom', 'Valentin', 'Victor', 'William', 'Yann', 'Yannick'
]

french_female = [
    'Marie', 'Jeanne', 'Françoise', 'Monique', 'Nicole', 'Nathalie', 'Isabelle', 'Delphine', 'Catherine', 'Sylvie', 'Martine', 'Jacqueline', 'Anne', 'Christine', 'Valérie', 'Sandrine', 'Véronique', 'Stéphanie', 'Patricia', 'Christiane', 'Brigitte', 'Dominique', 'Michèle', 'Danielle', 'Cécile', 'Florence', 'Annie', 'Agnès', 'Alice', 'Amélie', 'Annette', 'Antoinette', 'Ariane', 'Aurore', 'Béatrice', 'Bernadette', 'Blanche', 'Camille', 'Caroline', 'Céline', 'Chantal', 'Charlotte', 'Claire', 'Claudine', 'Colette', 'Corinne', 'Denise', 'Diane', 'Edith', 'Elisabeth', 'Elodie', 'Emilie', 'Emma', 'Evelyne', 'Fabienne', 'Florence', 'Frédérique', 'Gabrielle', 'Geneviève', 'Georgette', 'Germaine', 'Ghislaine', 'Ginette', 'Hélène', 'Henriette', 'Inès', 'Irène', 'Josiane', 'Josette', 'Julie', 'Juliette', 'Laurence', 'Léa', 'Léonie', 'Liliane', 'Line', 'Louise', 'Lucie', 'Madeleine', 'Magali', 'Marcelle', 'Marguerite', 'Marthe', 'Mathilde', 'Mireille', 'Nadine', 'Natalie', 'Noémie', 'Odette', 'Olivie', 'Paulette', 'Pénélope', 'Philomène', 'Pierrette', 'Rachel', 'Raymonde', 'Renée', 'Rita', 'Rosalie', 'Rose', 'Roseline', 'Sabine', 'Simone', 'Solange', 'Sophie', 'Suzanne', 'Sylvaine', 'Thérèse', 'Valentine', 'Violette', 'Viviane', 'Yvette', 'Yvonne', 'Zoé', 'Adeline', 'Alexandra', 'Alice', 'Ambre', 'Anais', 'Anna', 'Apolline', 'Aurelie', 'Axelle', 'Capucine', 'Carla', 'Cassandre', 'Cecile', 'Chloe', 'Clarisse', 'Clementine', 'Coline', 'Constance', 'Delphine', 'Elise', 'Emeline', 'Estelle', 'Eva', 'Fanny', 'Garance', 'Helene', 'Ines', 'Iris', 'Jade', 'Julia', 'Justine', 'Laura', 'Lea', 'Lena', 'Lilou', 'Lola', 'Lou', 'Louane', 'Lucie', 'Luna', 'Maelle', 'Manon', 'Margaux', 'Marine', 'Mathilde', 'Melanie', 'Mila', 'Nina', 'Noemie', 'Océane', 'Olivia', 'Pauline', 'Romane', 'Rose', 'Sarah', 'Sasha', 'Solene', 'Soline', 'Sonia', 'Tessa', 'Valentine', 'Victoire', 'Zoe'
]

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

# Gender analysis of firm leaders
d = gender.Detector()
df_unique['first_name'] = df_unique['DirigeantprincipalNom'].str.split().str[0]
def get_gender_improved(name):
    if pd.isna(name):
        return 'unknown'
    gender = d.get_gender(name)
    if gender in ['unknown', 'andy']:
        # Check hyphenated names
        parts = name.lower().replace('-', ' ').split()
        for part in parts:
            if part in [m.lower() for m in french_male]:
                return 'male'
            elif part in [f.lower() for f in french_female]:
                return 'female'
        # Check full name lower
        if name.lower() in [m.lower() for m in french_male]:
            return 'male'
        elif name.lower() in [f.lower() for f in french_female]:
            return 'female'
        return 'unknown'
    return gender

df_unique['gender'] = df_unique['first_name'].apply(get_gender_improved)

# Simplify gender
gender_map = {'male': 'Male', 'female': 'Female', 'mostly_male': 'Male', 'mostly_female': 'Female', 'unknown': 'Unknown', 'andy': 'Unknown'}
df_unique['gender_simple'] = df_unique['gender'].map(gender_map)

gender_counts = df_unique['gender_simple'].value_counts()
gender_percent = (gender_counts / gender_counts.sum()) * 100

print("\nGender distribution of firm leaders (%):")
print(gender_percent)

# Percentage among identified genders
identified_counts = gender_counts[gender_counts.index != 'Unknown']
identified_percent = (identified_counts / identified_counts.sum()) * 100

print("\nGender distribution among identified firm leaders (%):")
print(identified_percent)

# Save unknown names for manual classification
unknown_names = df_unique[df_unique['gender'].isin(['unknown', 'andy'])]['first_name'].dropna().unique()
pd.DataFrame({'unknown_names': unknown_names}).to_csv('unknown_names.csv', index=False)
print("Saved unknown names to unknown_names.csv for manual gender classification")
print("Top 10 unknown names:", unknown_names[:10])

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

# Graph 4: Gender distribution (identified only)
plt.figure(figsize=(8,6))
identified_percent.plot(kind='pie', autopct='%1.1f%%')
plt.title('Gender Distribution of Identified Firm Leaders')
plt.ylabel('')
plt.figtext(0.5, 0.02, '50.0% of firms have unknown gender due to missing or unrecognized names', ha='center', fontsize=10)
plt.savefig('gender_distribution.png')
print("Saved: gender_distribution.png")

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

# Static Choropleth Map: Municipalities by number of enterprises
# Download shapefile
zip_url = 'https://www.data.gouv.fr/fr/datasets/r/8f251e1d-5a6b-4e4e-8e61-9b05b82b4e/download/communes-martinique.zip'
response = requests.get(zip_url)
with open('communes_martinique.zip', 'wb') as f:
    f.write(response.content)

# Extract zip
with zipfile.ZipFile('communes_martinique.zip', 'r') as zip_ref:
    zip_ref.extractall('shapefiles')

# Read shapefile
gdf = gpd.read_file('shapefiles/communes-martinique.shp')
gdf['insee'] = gdf['insee'].astype(str)

# Merge with commune_agg
commune_agg.index.name = 'insee'
gdf = gdf.merge(commune_agg, on='insee', how='left')

# Plot
fig, ax = plt.subplots(1, 1, figsize=(10, 10))
gdf.plot(column='count', ax=ax, cmap='YlOrRd', legend=True)
ax.axis('off')
plt.savefig('martinique_choropleth.png', bbox_inches='tight')
print("Saved: martinique_choropleth.png")
