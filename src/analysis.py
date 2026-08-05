import pandas as pd

def column_summary(df, column_name):
    total = len(df)
    unique = df[column_name].nunique()
    nulls = df[column_name].isna().sum()
    duplicate_rows = df.duplicated().sum()
    
    print(f"\nКолонка: {column_name}")
    print(f"Всього записів: {total:,}")
    print(f"Унікальних значень: {unique:,}")
    print(f"Пропусків (NaN): {nulls} ({nulls/total*100:.4f}%)")
    print(f"Повторюваних значень: {total - unique} ({ (total - unique)/total*100:.2f}%)")
    print(f"Дублікатів рядків: {duplicate_rows} ({duplicate_rows/total*100:.4f}%)")
    
    return {'total': total, 'unique': unique, 'nulls': nulls, 'duplicates': duplicate_rows}

def text_column_summary(df, column_name):
    stats = column_summary(df, column_name)
    
    print(f"\nТекстовий аналіз:")
    sample = df[column_name].dropna().unique()[:5]
    print(f"Приклади: {sample}")
    
    lengths = df[column_name].dropna().astype(str).str.len()
    print(f"Мін. довжина: {lengths.min()}")
    print(f"Макс. довжина: {lengths.max()}")
    
    return stats

def numeric_column_summary(df, column_name):
    stats = column_summary(df, column_name)
    print(f"\nЧисловий аналіз:")
    print(f"Мінімум: {df[column_name].min():.0f}")
    print(f"Максимум: {df[column_name].max():.0f}")
    print(f"Середнє: {df[column_name].mean():.2f}")
    print(f"Медіана: {df[column_name].median():.2f}")
    
    return stats

def create_summary_table(df, descriptions):
    total_rows = len(df)
    summary = pd.DataFrame({
        'Колонка': df.columns,
        'Опис': [descriptions.get(col, '') for col in df.columns],
        'Тип даних': df.dtypes.values,
        'Унікальних': [df[col].nunique() for col in df.columns],
        'Непорожніх': df.count().values,
        'Пропуски (NaN)': df.isnull().sum().values,
        '% NaN': (df.isnull().sum().values / total_rows * 100).round(2),
        'Нульові (0)': [(df[col] == 0).sum() for col in df.columns],
        '% Нулів': [((df[col] == 0).sum() / total_rows * 100).round(2) for col in df.columns]
    })
    
    return summary

def analyze_vehicle_location(df):
    from cleaning import parse_vehicle_location
    df = parse_vehicle_location(df)
    print("\nПеревірка координат:")
    
    invalid_lat = df[(df['Latitude'] < -90) | (df['Latitude'] > 90)]
    print(f"Широта (Latitude):")
    print(f"Мін: {df['Latitude'].min():.4f}")
    print(f"Макс: {df['Latitude'].max():.4f}")
    print(f"Некоректних: {len(invalid_lat)}")
    
    invalid_lon = df[(df['Longitude'] < -180) | (df['Longitude'] > 180)]
    print(f"Довгота (Longitude):")
    print(f"Мін: {df['Longitude'].min():.4f}")
    print(f"Макс: {df['Longitude'].max():.4f}")
    print(f"Некоректних: {len(invalid_lon)}")
    
    if len(invalid_lat) == 0 and len(invalid_lon) == 0:
        print("Координати в межах норми")
    
    return df

def analyze_model_year(df):
    future_cars = df[df['Model Year'] > 2026]
    if len(future_cars) > 0:
        print(f"\nЗнайдено {len(future_cars)} записів з роком > 2026")
        print(future_cars[['Model Year', 'Make', 'Model']].head())
    else:
        print("\nНемає аномальних років (>2026)")
    
    return df

def analyze_county(df):
    print("\nОкруги по штатах:")
    wa_counties = df[df['State'] == 'WA']['County'].nunique()
    other_counties = df[df['State'] != 'WA']['County'].nunique()
    print(f"У WA: {wa_counties}")
    print(f"В інших штатах: {other_counties}")
    
    return df

# analysis.py

def analyze_base_msrp(df):
    #column_summary(df, 'Base MSRP')
    zero_count = (df['Base MSRP'] == 0).sum()
    total = len(df)
    real_count = total - zero_count
    
    print(f"Розподіл даних:")
    print(f"Нульових значень: {zero_count:,} ({zero_count/total*100:.2f}%)")
    print(f"Реальних даних:   {real_count:,} ({real_count/total*100:.2f}%)")
    
    print("\nКолонка не придатна до аналізу:")
    print("98.71% даних = 0")
    print("Тільки 1.29% записів мають реальні ціни")
    
    return df