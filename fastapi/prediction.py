import json
from sklearn.preprocessing import LabelEncoder
from preprocess import Preprocess
import pickle
import pandas as pd

label_encoder = LabelEncoder()

class Prediction(Preprocess):
    def __init__(self):
        pass

    def find(self,json_input):
        json_string=json_input.replace("'", '"')
        data = json.loads(json_string)
        print(data)
        df1=pd.DataFrame(list([data.values()]),columns=list(data.keys()))
        for col in df1.columns.to_list():
            df1[col] = label_encoder.fit_transform(df1[col])   
        try:
            with open(f"model.pkl", 'rb') as file:
                loaded_object = pickle.load(file)
            print(df1.values)
            predict=loaded_object.predict(df1.values)
            return {"prediction":str(predict[0])}
        except:
            return {"message":"error"}
        
    def get_json_input(self,):
        try:
            df = pd.read_csv(f"data.csv")
            cols=df.columns.to_list()
            vals=["" for val in cols]
            print(vals)
            string= str(dict(zip(cols, vals)))
            string=string.replace(",",",\n")
            string=string.replace("{","{\n")
            string=string.replace("}","\n}")
            return string
        except:
            return {"message":"fail"}