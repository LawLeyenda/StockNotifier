import csv
import pandas as pd
import numpy as np

dict = {'name': 'krunal', 'age': 26, 'education': 'Engineering'}


def save(dict):
    with open('data.csv', 'w') as f:
        for key in dict.keys():
            f.write("%s, %s\n" % (key, dict[key]))


def read(csv_file):
    stock_list = {}
    df = pd.read_csv("data.csv")

    for index, row in df.iterrows():
        stock_list[row['ticker']] = row['info']
    return stock_list

