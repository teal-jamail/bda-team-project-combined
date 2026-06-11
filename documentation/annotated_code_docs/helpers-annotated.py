import pandas as pd
import os

def load_csv(filepath):
    # Time: O(n) - reads n rows from disk
    # Space: O(n) - stores n rows in memory
    return pd.read_csv(filepath)

def save_csv(df, filepath):
    # Time: O(n) - writes n rows to disk
    # Space: O(1) - no extra memory beyond the dataframe
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    # creates filepath, extracts folder data
    # os.makerdirs creates that folder if doesnt exist
    # if exists don't give error: FileNotFound 
    # would crash 'df.to_csv' if data/ folder doesn't exist

    df.to_csv(filepath, index=False)
    # don't write pd's row nums (o,1,2,3...) as col. in csv
   
    print(f"Saved: {filepath}")
