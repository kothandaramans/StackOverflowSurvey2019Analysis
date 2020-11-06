import pandas as pd

def load(filename):
    df = pd.read_csv(filename).set_index('Respondent')
    return df
