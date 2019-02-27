import itertools
import pandas as pd

df = pd.read_csv('test_files/countries.csv')

print(list(itertools.combinations(df, 2)))