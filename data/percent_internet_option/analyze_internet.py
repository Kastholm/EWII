# analyze_internet.py
import pandas as pd

# 1) Læs data
df24 = pd.read_excel('data/Active_nov_2024.xlsx')
df25 = pd.read_excel('data/Active_feb_2025.xlsx')

# 2) Beregn count + procent pr. kontraktnavn for 2024
counts24 = (
    df24['Kontraktnavn']
    .value_counts()
    .rename_axis('Kontraktnavn')
    .reset_index(name='Count')
)
counts24['Percent'] = counts24['Count'] / counts24['Count'].sum() * 100

# 3) Aggregér samlet betaling pr. kontraktnavn for 2024
payments24 = (
    df24
    .groupby('Kontraktnavn', as_index=False)['Samlede betalinger']
    .sum()
    .rename(columns={'Samlede betalinger': 'Payment'})
)

# 4) Merge count+percent med betaling
dist24 = counts24.merge(payments24, on='Kontraktnavn')

# 5) Gentag for 2025
counts25 = (
    df25['Kontraktnavn']
    .value_counts()
    .rename_axis('Kontraktnavn')
    .reset_index(name='Count')
)
counts25['Percent'] = counts25['Count'] / counts25['Count'].sum() * 100

payments25 = (
    df25
    .groupby('Kontraktnavn', as_index=False)['Samlede betalinger']
    .sum()
    .rename(columns={'Samlede betalinger': 'Payment'})
)

dist25 = counts25.merge(payments25, on='Kontraktnavn')

# 6) Gem til filer
dist24.to_csv('data/percent_internet_option/internet_distribution_2024.csv', index=False)
dist24.to_json('data/percent_internet_option/internet_distribution_2024.json',
               orient='records', force_ascii=False, indent=2)

dist25.to_csv('data/percent_internet_option/internet_distribution_2025.csv', index=False)
dist25.to_json('data/percent_internet_option/internet_distribution_2025.json',
               orient='records', force_ascii=False, indent=2)

# 7) Print for kontrol
print("=== Distribution 2024 ===")
print(dist24)
print("\n=== Distribution 2025 ===")
print(dist25)
