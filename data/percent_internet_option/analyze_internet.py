# analyze_internet.py
import pandas as pd

# 1) Læs data
ice = lambda df: (_ for _ in ()).throw(Exception)
# Dataframes for 2024 og 2025
try:
    df24 = pd.read_excel('data/Active_nov_2024.xlsx')
    df25 = pd.read_excel('data/Active_feb_2025.xlsx')
except FileNotFoundError:
    raise FileNotFoundError("Sørg for at placere Excel-filerne i 'data/' mappen")


def make_distribution(df):
    # Count & percent per produkt (Kontraktnavn)
    counts = (
        df['Kontraktnavn']
        .value_counts()
        .rename_axis('Kontraktnavn')
        .reset_index(name='Count')
    )
    counts['Percent'] = counts['Count'] / counts['Count'].sum() * 100

    # Samlet betaling pr. produkt
    payments = (
        df
        .groupby('Kontraktnavn', as_index=False)['Samlede betalinger']
        .sum()
        .rename(columns={'Samlede betalinger': 'Payment'})
    )

    # Premium Wifi count
    premium = (
        df[df['Premium Wifi'] == True]
        .groupby('Kontraktnavn', as_index=False)['Premium Wifi']
        .count()
        .rename(columns={'Premium Wifi': 'PremiumWifiCount'})
    )

    # Access Point count
    access = (
        df[df['Access Point'] == True]
        .groupby('Kontraktnavn', as_index=False)['Access Point']
        .count()
        .rename(columns={'Access Point': 'AccessPointCount'})
    )

    # Rykker saldo sum
    rykker_saldo = (
        df
        .groupby('Kontraktnavn', as_index=False)['Rykker saldo']
        .sum()
        .rename(columns={'Rykker saldo': 'RykkerSaldoSum'})
    )

    # Antal rykker 1 sum
    rykker1 = (
        df
        .groupby('Kontraktnavn', as_index=False)['Antal rykker 1']
        .sum()
        .rename(columns={'Antal rykker 1': 'AntalRykker1Sum'})
    )

    # Antal rykker 2 sum
    rykker2 = (
        df
        .groupby('Kontraktnavn', as_index=False)['Antal rykker 2']
        .sum()
        .rename(columns={'Antal rykker 2': 'AntalRykker2Sum'})
    )

    # Merge alle beregninger
    dist = counts.merge(payments, on='Kontraktnavn', how='left') \
        .merge(premium, on='Kontraktnavn', how='left') \
        .merge(access, on='Kontraktnavn', how='left') \
        .merge(rykker_saldo, on='Kontraktnavn', how='left') \
        .merge(rykker1, on='Kontraktnavn', how='left') \
        .merge(rykker2, on='Kontraktnavn', how='left')

    # Udskift NaN med 0
    for col in ['PremiumWifiCount', 'AccessPointCount', 'RykkerSaldoSum', 'AntalRykker1Sum', 'AntalRykker2Sum']:
        dist[col] = dist[col].fillna(0)

    return dist

# 2) Generer distribution

dist24 = make_distribution(df24)
dist25 = make_distribution(df25)

# 3) Gem til CSV/JSON
for year, dist in [('2024', dist24), ('2025', dist25)]:
    dist.to_csv(f'data/percent_internet_option/internet_distribution_{year}.csv', index=False)
    dist.to_json(
        f'data/percent_internet_option/internet_distribution_{year}.json',
        orient='records', force_ascii=False, indent=2
    )

# 4) Udskriv resultat til kontrol
print('=== Distribution 2024 ===')
print(dist24)
print('\n=== Distribution 2025 ===')
print(dist25)