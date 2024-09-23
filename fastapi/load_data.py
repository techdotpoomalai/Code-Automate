import pandas as pd

class CodeAutomate:
    def __init__(self):
        pass

    async def load_doc(self,file):
        print("hjdfgjghksdfghdkjghkdsfhgjkhfdgkhfdkghkdfhgkhdfgkjhdkfghfdhgkhdfgkjhdfkghkdsfghkdfhgkhjdfkghdskfghkdshgkhdfkghjkdsfhgkdhgkjhdfkgjjh")
        try:
            with open("data.csv", 'wb') as f:
                f.write(await file.read())
            
            return {"message":"success"}
        except Exception as e:
            return {"error": str(e)}

    def get_data(self,):
        try:
            df = pd.read_csv("data.csv")
            df.to_csv('preprocess.csv')
            records = df.to_dict(orient='records')
            return records
        except:
            return []