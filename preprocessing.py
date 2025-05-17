import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler

def load_and_preprocess_data(csv_path, column_name):
    df = pd.read_csv(csv_path)
    try:
        df['Date'] = pd.to_datetime(df['Date'], format='%m/%d/%Y')
    except:
        df['Date'] = pd.to_datetime(df['Date'], format='%Y-%m-%d')
    df = df.sort_values('Date')
    df = df.set_index('Date')
    df[column_name] = df[column_name].str.replace('$', '').astype(float)
    data = df[column_name].values.reshape(-1, 1)
    return data, df


def create_sequences(data, seq_length):
    X, y = [], []
    for i in range(len(data) - seq_length):
        X.append(data[i:(i + seq_length)])
        y.append(data[i + seq_length])
    return np.array(X), np.array(y)

def scale_data(data):
    scaler = MinMaxScaler()
    scaled_data = scaler.fit_transform(data)
    return scaled_data, scaler
