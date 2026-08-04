electric-vehicles-analysis/
│
├── README.md                          # Опис проекту
├── requirements.txt                   # Залежності
├── .gitignore                         # Щоб не публікувати дані
│
├── data/
│   └── .gitkeep                       # Папка для даних (порожня)
│
├── notebooks/
│   └── 01_data_understanding.ipynb    # Jupyter Notebook (основний аналіз)
│
├── src/                               # Модулі Python
│   ├── __init__.py
│   ├── config.py                      # Конфігурація (шляхи, словники)
│   ├── data_loader.py                 # Завантаження даних
│   ├── cleaning.py                    # Функції очищення
│   ├── analysis.py                    # Функції аналізу
│   └── main.py                        # Головний скрипт
│
├── reports/
│   └── data_understanding_report.md   # Звіт
│
└── visualizations/                    # Збережені графіки
    └── .gitkeep
