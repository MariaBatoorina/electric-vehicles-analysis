COLUMN_DESCRIPTIONS = {
    'VIN (1-10)': 'Частковий VIN-код (перші 10 символів)',
    'County': 'Округ, де зареєстровано авто',
    'City': 'Місто реєстрації',
    'State': 'Штат',
    'Postal Code': 'Поштовий індекс (Zip Code)',
    'Model Year': 'Рік випуску автомобіля',
    'Make': 'Виробник автомобіля',
    'Model': 'Модель автомобіля',
    'Electric Vehicle Type': 'Тип електромобіля',
    'Clean Alternative Fuel Vehicle (CAFV) Eligibility': 'Статус пільгового допуску',
    'Electric Range': 'Запас ходу на одному заряді (милі)',
    'Base MSRP': 'Базова рекомендована ціна ($)',
    'Legislative District': 'Законодавчий округ',
    'DOL Vehicle ID': 'Унікальний ID автомобіля',
    'Vehicle Location': 'Географічні координати (POINT)',
    'Electric Utility': 'Постачальник електроенергії',
    '2020 Census Tract': 'ID переписної ділянки'
}

EXACT_REPLACEMENTS = {
    'TES??\x8bLA': 'TESLA',
    'TH!NK': 'THINK',
    'F-150': 'FORD',
    'GLC-CLASS': 'MERCEDES-BENZ'
}

INCORRECT_MODELS = {
    'FORD': 'UNKNOWN',
    'BRIGHTDROP': 'UNKNOWN'
}

CORRUPTED_MODELS = ['Plug-in Hybrid Electric Vehicle (PHEV)']  
