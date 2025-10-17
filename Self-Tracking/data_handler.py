import pandas as pd
import os

DATA_PATH = "data/user_logs.csv"

def save_activity(date, text):
    os.makedirs("data", exist_ok=True)
    df = pd.DataFrame([[date, text]], columns=["Tarih", "Aktivite"])
    if os.path.exists(DATA_PATH):
        df.to_csv(DATA_PATH, mode='a', header=False, index=False)
    else:
        df.to_csv(DATA_PATH, index=False)

def load_data():
    if os.path.exists(DATA_PATH):
        return pd.read_csv(DATA_PATH)
    return pd.DataFrame(columns=["Tarih", "Aktivite"])
