from fastapi import FastAPI,Form
import fastapi
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse,FileResponse

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import r2_score,accuracy_score
import matplotlib.pyplot as plt
from PIL import Image
import pandas as pd
import requests
import shutil
import pickle
import base64
import json
import os
import io
from PIL import Image

from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.svm import SVC
import uvicorn

from code_automate import Codeautomate
from preprocess import Preprocess


app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # React app's origin
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods (GET, POST, etc.)
    allow_headers=["*"],  # Allow all headers (Authorization, etc.)
)

label_encoder = LabelEncoder()

data_file=Codeautomate()

@app.post("/file_upload")
async def upload_file(file: UploadFile= File(...)):
    
    file_res=data_file.upload_file(file)
    return file_res

@app.get("/fetch_data")
async def main():
    data_file=Codeautomate()
    data_res=data_file.get_data()
    return data_res
    
@app.post("/preprocess")
async def preprocess(col: str = Form(...), prepros: str = Form(...)):
    data_file=Codeautomate()
    pros=Preprocess()
    process_data=pros.process(col,prepros)

    # col_dict=json.loads(col)
    # cols=[key for key, value in col_dict.items() if value]
    # df=[]
    # print(cols,prepros)
    # try:
    #     # file=os.listdir("Preprocess")
    #     df = pd.read_csv(f"preprocess.csv")
    #     if prepros == 'onehot_encode':
    #         df = pd.get_dummies(df, columns=cols)
    #     elif prepros == 'label_encode':
    #         for col in cols:
    #             if col in df.columns:
    #                 df[col] = label_encoder.fit_transform(df[col])
    #     elif prepros == 'drop_col':
    #         df.drop(columns=cols, errors='ignore', inplace=True)
    #     bool_col=[col for col in df.columns if df[col].dtype == 'bool']
    #     for col_ in bool_col:
    #         df[col_] = df[col_].astype(int)
    #     df.to_csv(f"preprocess.csv",index=False)  
    #     records = df.to_dict("records")
    #     return records
    # except:
    #     return []
    
@app.post("/analysis")
async def preprocess(cols: str = Form(...), analysis: str = Form(...)):
    print(cols)
    col_dict=json.loads(cols)
    col=[key for key, value in col_dict.items() if value]
    print(col, analysis)
    try:
        # file=os.listdir(f"Preprocess")
        df = pd.read_csv(f"preprocess.csv")
        plt.figure(figsize=(6, 4))
        if analysis == 'scatter_chart':       
            plt.scatter(df[col[0]], df[col[1]])  
            plt.title('Scatter Plot')
        if analysis == 'line_chart':
            plt.plot(df[col[0]], df[col[1]])  
            plt.title('Line Plot')
        fig = plt.gcf()
        buf = io.BytesIO() 
        fig.savefig(buf) 
        buf.seek(0) 
        img = Image.open(buf) 
        img.save(f'analysis.png')
        img.save(f'/Users/poomalai/Desktop/CODE AUTOMATE/react_frontend/src/Component/analysis.png')
        plt.show()
        return {"message":"image created success"}
    except:
        return {"message":"image created fail"}
    
@app.post("/train")
async def preprocess(col: str = Form(...), algorithm: str = Form(...), problem: str = Form(...)):
    col_dict=json.loads(col)
    col=[key for key, value in col_dict.items() if value]
    print(col, algorithm, problem)
    try:
        # file=os.listdir('Preprocess')
        df = pd.read_csv('preprocess.csv')
        # df.drop("Unnamed: 0",axis=1,inplace=True)
        y=df.pop(col[0])
        X=df
        print(X.shape)
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        models = {
            'logistic_regression': LogisticRegression(max_iter=200),
            'random_forest': RandomForestClassifier(),
            'Support Vector Classifier': SVC(),
            'decision_tree': DecisionTreeClassifier(criterion='entropy', random_state=9)
        }
        r2=''
        for name, model in models.items():
            if name==algorithm:
                model.fit(X_train,y_train)
                y_pred = model.predict(X_test)
                with open('model.pkl', 'wb') as file:
                    pickle.dump(model, file)
        if problem == "regression":
            r2 = r2_score(y_test, y_pred)
            return {"r2_score":r2}
        else:
            accuracy = accuracy_score(y_test, y_pred)
            return {"accuracy":accuracy}
    except:
        return {"message":"model error"}
    

@app.get("/fetch_pickle")
async def fetch_picklefile():
    try:
        file_path = os.path.join("model", "model.pkl")
        # return FileResponse("model\model.pkl", media_type='application/octet-stream', filename="model.pkl")
        return {"message":"success"}
    except:
        return {"message":"fail"}

@app.get("/json_input")
async def fetch_jsoninput():
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

@app.post("/predictions")
async def preprocess(json_input: str= Form(...)):
    json_string=json_input.replace("'", '"')
    data = json.loads(json_string)
    print(data)
    df1=pd.DataFrame(list([data.values() ]),columns=list(data.keys()))
    for col in df1.columns.to_list():
        df1[col] = label_encoder.fit_transform(df1[col])   
        print(df1)
    try:
        with open(f"model.pkl", 'rb') as file:
            loaded_object = pickle.load(file)
        print(df1.values)
        predict=loaded_object.predict(df1.values)
        return {"prediction":str(predict[0])}
    except:
        return {"message":"error"}
    

if __name__ == '__name__':
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True, debug=True)


