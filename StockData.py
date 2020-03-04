import pandas as pd
import numpy as np

def save(df,location):
    df.to_csv(location)

def read(csv_file):
    df = pd.read_csv(csv_file, index_col=0)
    return df