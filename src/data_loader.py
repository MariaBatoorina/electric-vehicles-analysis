import pandas as pd

def load_data(file_path, encoding='latin-1'):
    df = pd.read_csv(file_path, encoding=encoding)
    return df

def create_copy(df, save_path=None):
    df_copy = df.copy()
    if save_path:
        df_copy.to_csv(save_path, index=False)
    return df_copy