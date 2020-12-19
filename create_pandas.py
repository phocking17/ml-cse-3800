import pickle
from excel_reading import Patient
import pandas as pd
y = pickle.load(open("save.txt", "rb"))

def frame(obj_lst):
    name_lst = [str(key) for key in vars(y[0])]
    df = pd.DataFrame(columns=name_lst)
    for patient in obj_lst:
        data_dict = vars(patient)
        data_row = [data_dict[key] for key in data_dict]
        df_length = len(df)
        df.loc[df_length] = data_row
    return df
y = frame(y)
y.to_csv('pandas_data.csv', index=False, header=True)