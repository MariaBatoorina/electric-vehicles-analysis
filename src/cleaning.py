import pandas as pd
import numpy as np

def parse_vin_long_rows(df):
    import csv
    import io
    
    long_vin = df[df['VIN (1-10)'].astype(str).str.len() > 10].copy()
    print(f"Знайдено {len(long_vin)} 'злиплих' рядків")
    
    parsed_rows = []
    for row in long_vin['VIN (1-10)']:
        reader = csv.reader(io.StringIO(row))
        parsed = next(reader)
        parsed_rows.append(parsed)
    
    split_data = pd.DataFrame(parsed_rows)
    
    if split_data.shape[1] > 17:
        split_data[16] = split_data.iloc[:, 16:].apply(lambda x: ','.join(x.astype(str)), axis=1)
        split_data = split_data.iloc[:, :17]
    
    column_names = ['VIN (1-10)', 'County', 'City', 'State', 'Postal Code', 
                    'Model Year', 'Make', 'Model', 'Electric Vehicle Type', 
                    'Clean Alternative Fuel Vehicle (CAFV) Eligibility', 
                    'Electric Range', 'Base MSRP', 'Legislative District', 
                    'DOL Vehicle ID', 'Vehicle Location', 'Electric Utility', 
                    '2020 Census Tract']
    
    split_data.columns = column_names
    
    long_vin_indices = df[df['VIN (1-10)'].astype(str).str.len() > 10].index
    df = df.drop(long_vin_indices)
    df = pd.concat([df, split_data], ignore_index=True)
    
    print(f"Відновлено {len(split_data)} рядків")
    return df

def to_upper(df, column_name):
    if column_name in df.columns:
        df[column_name] = df[column_name].str.upper()
        print(f"{column_name}: приведено до верхнього регістру")
    return df

def fix_make_replacements(df, replacements):
    for wrong, correct in replacements.items():
        if wrong in df['Make'].values:
            count = (df['Make'] == wrong).sum()
            df['Make'] = df['Make'].replace(wrong, correct)
            print(f"'{wrong}' - '{correct}' ({count} записів)")
    return df

def fix_model_incorrect(df, incorrect_models, corrupted_models=None):
    for wrong, correct in incorrect_models.items():
        count = (df['Model'] == wrong).sum()
        if count > 0:
            df['Model'] = df['Model'].replace(wrong, correct)
            print(f"'{wrong}' - '{correct}' ({count} записів)")
    
    if corrupted_models:
        for model in corrupted_models:
            count = (df['Model'] == model).sum()
            if count > 0:
                df = df[df['Model'] != model]
                print(f"Видалено '{model}' ({count} записів)")
    
    return df

def parse_vehicle_location(df):
    null_count = df['Vehicle Location'].isna().sum()
    if null_count > 0:
        df['Vehicle Location'] = df['Vehicle Location'].fillna('UNKNOWN')
    
    df['Longitude'] = df['Vehicle Location'].str.extract(r'POINT \(([^ ]+) ')[0].astype(float)
    df['Latitude'] = df['Vehicle Location'].str.extract(r'POINT \([^ ]+ ([^)]+)\)')[0].astype(float)
    
    return df

def fill_unknown(df, column_name, verbose=True):
    null_count = df[column_name].isna().sum()
    if null_count > 0:
        df[column_name] = df[column_name].fillna('UNKNOWN')
        if verbose:
            print(f"Заповнено {null_count} пропусків на 'UNKNOWN'")
    return df

def clean_model_year(df):
    df['Model Year'] = pd.to_numeric(df['Model Year'], errors='coerce')
    print(" Конвертовано в числовий тип")
    
    future_cars = df[df['Model Year'] > 2026]
    if len(future_cars) > 0:
        df.loc[df['Model Year'] > 2026, 'Model Year'] = np.nan
        print(f"Замінено {len(future_cars)} записів з роком > 2026 на NaN")
    else:
        print("Немає аномальних років (>2026)")
    
    return df

def clean_county(df):
    null_count = df['County'].isna().sum()
    if null_count > 0:
        df['County'] = df['County'].fillna('UNKNOWN')
        print(f"Заповнено {null_count} пропусків на 'UNKNOWN'")
    else:
        print("Пропусків немає")

    df['County'] = df['County'].str.strip()
    df['County'] = df['County'].str.title()
    
    return df

def clean_state(df):
    canadian_states = ['BC', 'NS']
    military_states = ['AP', 'AE', 'AA']

    canada_rows = df[df['State'].isin(canadian_states)]
    if len(canada_rows) > 0:
        print(f"Знайдено {len(canada_rows)} записів з Канади (BC, NS):")
        #print(canada_rows[['State', 'City', 'Postal Code', 'Make', 'Model']].head())
        print("Потребують уточнення — залишено без змін")
    
    military_rows = df[df['State'].isin(military_states)]
    if len(military_rows) > 0:
        print(f"Знайдено {len(military_rows)} записів з військовими кодами (AP, AE, AA):")
        #print(military_rows[['State', 'City', 'Postal Code', 'Make', 'Model']].head())
        print("Потребують уточнення — залишено без змін")
    
    unknown_state = df[df['State'] == 'UNKNOWN']
    if len(unknown_state) > 0:
        print(f"Знайдено {len(unknown_state)} записів з UNKNOWN State")
    
    return df

def clean_postal_code(df):
    df['Postal Code'] = (
        df['Postal Code']
        .astype(float)             # спочатку в float
        .astype('Int64')           # потім в ціле число
        .astype('string')          # потім у текст
        .str.zfill(5)              # додаємо нулі зліва до 5 символів
    )

    null_count = df['Postal Code'].isna().sum()
    if null_count > 0:
        df['Postal Code'] = df['Postal Code'].fillna('UNKNOWN')
        print(f"Заповнено {null_count} пропусків на 'UNKNOWN'")
    else:
        print("Пропусків немає")
    
    return df

def clean_census_tract(df):
    null_count = df['2020 Census Tract'].isna().sum()
    if null_count > 0:
        print(f"Знайдено {null_count} пропусків у '2020 Census Tract', залишено як NaN (відсутність даних)")
    else:
        print("Пропусків немає")
    
    df['2020 Census Tract'] = pd.to_numeric(df['2020 Census Tract'], errors='coerce').astype('Int64')
    print("'2020 Census Tract' конвертовано в цілі числа")
    
    return df

def clean_legislative_district(df):
    null_count = df['Legislative District'].isna().sum()
    if null_count > 0:
        median_val = df['Legislative District'].median()
        df['Legislative District'] = df['Legislative District'].fillna(median_val)
        print(f"Заповнено {null_count} пропусків медіаною ({median_val:.0f})")
    else:
        print("Пропусків немає")
    
    df['Legislative District'] = df['Legislative District'].astype('Int64')
    
    return df

def clean_electric_range(df):
    df['Electric Range Clean'] = df['Electric Range']
    print("Створено копію 'Electric Range Clean'")
    
    zero_count = (df['Electric Range Clean'] == 0).sum()
    df['Electric Range Clean'] = df['Electric Range Clean'].replace(0, np.nan)
    
    print(f"Замінено {zero_count:,} нулів на NaN")
    print(f"Реальних даних: {df['Electric Range Clean'].notna().sum():,}")
    
    print("Порівняння:")
    print(f"Оригінал (Electric Range):      {df['Electric Range'].notna().sum():,} записів")
    print(f"Копія (Electric Range Clean):   {df['Electric Range Clean'].notna().sum():,} записів (без нулів)")
    
    return df























