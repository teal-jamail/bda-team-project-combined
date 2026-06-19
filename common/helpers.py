import pandas as pd
import os

def load_csv(filepath):

    # Time: O(n) - reads n rows from disk
    # Space: O(n) - stores n rows in memory

    return pd.read_csv(filepath)

def save_csv(df, filepath):
    os.makedirs(os.path.dirname(filepath), exist_ok=True)


    df.to_csv(filepath, index=False)
   
    print(f"Saved: {filepath}")
