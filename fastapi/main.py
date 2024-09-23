from load_data import CodeAutomate
from preprocess import Preprocess
from model_train import Modeltrain
from prediction import Prediction

from fastapi import FastAPI, Request, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # React app's origin
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods (GET, POST, etc.)
    allow_headers=["*"],  # Allow all headers (Authorization, etc.)
)

code=CodeAutomate()

@app.post("/file_upload")
async def upload_file(file: UploadFile= File(...)):
    
    # code_res=code.load_doc(file)
    # return code_res

    try:
        with open("data.csv", 'wb') as f:
            f.write(await file.read())
        
        return {"message":"success"}
    except Exception as e:
        return {"error": str(e)}

@app.get("/fetch_data")
async def main():
    code_res=code.get_data()
    return code_res
        
    
@app.post("/preprocess")
async def preprocess(col: str = Form(...), prepros: str = Form(...)):
    pros=Preprocess()
    pros_res=pros.process(col, prepros)
    return pros_res


model=Modeltrain()

@app.post("/train")
async def preprocess(col: str = Form(...), algorithm: str = Form(...), problem: str = Form(...)):
    
    model_res=model.train_model(col,algorithm, problem)
    return model_res


@app.get("/fetch_pickle")
async def fetch_picklefile():
    model_res=model.get_picklefile()
    return model_res
    

predict=Prediction()

@app.get("/json_input")
async def fetch_jsoninput():
    predict_res=predict.get_json_input()
    return predict_res


@app.post("/predictions")
async def preprocess(json_input: str= Form(...)):
    
    predict_res=predict.find(json_input)
    return predict_res


if __name__ == '__name__':
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True, debug=True)


