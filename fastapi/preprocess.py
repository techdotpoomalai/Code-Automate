import json
import pandas as pd
from sklearn.preprocessing import LabelEncoder


label_encoder = LabelEncoder()

class Preprocess():
    def __init__(self):
        pass

    def process(self,col,prepros):
        col_dict=json.loads(col)
        cols=[key for key, value in col_dict.items() if value]
        df=[]
        try:
            df = pd.read_csv(f"preprocess.csv")
            if prepros == 'onehot_encode':
                df = pd.get_dummies(df, columns=cols)
            elif prepros == 'label_encode':
                for col in cols:
                    if col in df.columns:
                        df[col] = label_encoder.fit_transform(df[col])
            elif prepros == 'drop_col':
                df.drop(columns=cols, errors='ignore', inplace=True)
            bool_col=[col for col in df.columns if df[col].dtype == 'bool']
            for col_ in bool_col:
                df[col_] = df[col_].astype(int)
            df.to_csv(f"preprocess.csv",index=False)  
            records = df.to_dict("records")
            return records
        except:
            return []
        
    