import pandas as pd
import numpy as np

from config import *
from data_loader import *
from cleaning import *
from analysis import *

df = load_data('src/Electric_Vehicle_Population_Data_changed.csv')
df = create_copy(df, 'Electric_Vehicle_Population_Data_CLEAN.csv')

summary = create_summary_table(df, COLUMN_DESCRIPTIONS)
print("\nData Understanding")
print(summary.to_string(index=False))

# VIN

print('\nVIN (1-10)')
#column_summary(df, 'VIN (1-10)')
df = parse_vin_long_rows(df)

# DOL Vehicle ID

print('\nDOL Vehicle ID')
df = analyze_dol_vehicle_id(df)

# Make

print('\nMake')
#column_summary(df, 'Make')
df = fix_make_replacements(df, EXACT_REPLACEMENTS)
df = to_upper(df, 'Make')

# Model

print('\nModel')
#text_column_summary(df, 'Model')
#preview_incorrect_models(df, INCORRECT_MODELS, CORRUPTED_MODELS)
df = fix_model_incorrect(df, INCORRECT_MODELS, CORRUPTED_MODELS)
print("Після змін")
print(f"Записів з 'UNKNOWN': {(df['Model'] == 'UNKNOWN').sum()}")
print(f"Унікальних моделей: {df['Model'].nunique()}")

# Electric Vehicle Type

print('\nElectric Vehicle Type')
#text_column_summary(df, 'Electric Vehicle Type')
check_ev_types(df)
print(f"Унікальні типи: {df['Electric Vehicle Type'].unique()}")

# Clean Alternative Fuel Vehicle (CAFV) Eligibility

print('\nClean Alternative Fuel Vehicle (CAFV) Eligibility')
#text_column_summary(df, 'Clean Alternative Fuel Vehicle (CAFV) Eligibility')
print(f"Унікальні статуси: {df['Clean Alternative Fuel Vehicle (CAFV) Eligibility'].unique()}")

# Vehicle Location

print('\nVehicle Location')
#text_column_summary(df, 'Vehicle Location')
df = parse_vehicle_location(df)
df = analyze_vehicle_location(df)

# Electric Utility

print('\nElectric Utility')
#text_column_summary(df, 'Electric Utility')
df = fill_unknown(df, 'Electric Utility')

# Model Year

print('\nModel Year')
df['Model Year'] = pd.to_numeric(df['Model Year'], errors='coerce')
#numeric_column_summary(df, 'Model Year')
df = analyze_model_year(df)
df = clean_model_year(df)

# County

print('\nCounty')
#text_column_summary(df, 'County')
#df = analyze_county(df)
df = clean_county(df)
print("Після очищення:")
print(f"Унікальних округів: {df['County'].nunique()}")
print(f"Пропусків: {df['County'].isna().sum()}")
print(f"Записів з 'UNKNOWN': {(df['County'].str.upper() == 'UNKNOWN').sum()}")

# City

print('\nCity')
#text_column_summary(df, 'City')
df = fill_unknown(df, 'City')

# State

print('\nState')
#text_column_summary(df, 'State')
df = clean_state(df)

# Postal Code

print('\nPostal Code')
df = clean_postal_code(df)
#text_column_summary(df, 'Postal Code')

# 2020 Census Tract

print('\n2020 Census Tract')
#column_summary(df, '2020 Census Tract')
df = clean_census_tract(df)

# Legislative District

print('\nLegislative District')
df['Legislative District'] = pd.to_numeric(df['Legislative District'], errors='coerce')
#numeric_column_summary(df, 'Legislative District')
df = clean_legislative_district(df)

# Electric Range

print('\nElectric Range')
df['Electric Range'] = pd.to_numeric(df['Electric Range'], errors='coerce')
#numeric_column_summary(df, 'Electric Range')
df = analyze_electric_range(df)
df = clean_electric_range(df)

# Base MSRP

print('\nBase MSRP')
df = analyze_base_msrp(df)

df.to_csv('Electric_Vehicle_Data_CLEANED.csv', index=False)
print(f"\nВсього записів: {len(df):,}")
print(f"Всього колонок: {len(df.columns)}")

#print(df.head(20).to_string())

