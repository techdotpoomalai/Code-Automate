import shutil
import pandas as pd

class Codeautomate:
    def __init__(self,):
        pass

    def upload_file(self,file):
        print(file)
        # try:
        #     with open(f"data.csv", 'wb') as f:
        #         f.write(file.read())
        #     # shutil.copyfile("data.csv", "preprocess.csv")
        #     return {"message":"success"}
        # except Exception as e:
        #     return {"error": str(e)}
    

    def get_data(self,):
        try:
            df = pd.read_csv("preprocess.csv")
            records = df.to_dict(orient='records')
            return records
        except:
            return []
        