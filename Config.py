import os
import json5 as json


class Config:
    def __init__(self):
        self.DIR = os.path.dirname(os.path.realpath(__file__))
        self.file = os.path.join(self.DIR, 'config.json')
        # ^if this file doesn't exist... you need to create it 
        # should look like this... with your api key
        # {"X-RapidAPI-Key": "<API-KEY>"}
        self.data = self.get_data(self.file)

    def get_data(self,file):
        try:
            with open(file,'r',encoding='utf-8') as f:
                return json.load(f)
        except:
            return {}

    def set_data(self,data,file):
        # self.sort()
        with open(file,'w',encoding='utf-8') as f:
            json.dump(data,f,indent=4)


            