import pandas as pd # works like tidydata
import numpy as np # works with matrices
import requests # conducts web transactions
import json # works with json style data
import dotenv # works with .env files
import os # allows for operating system level commands
import re # regular expressions
import io
from PyPDF2 import PdfReader
import pymongo
from bson.json_util import dumps, loads
import time

class legiscanscraper:
    def __init__(self):
        dotenv.load_dotenv() # finds and loads (silently) the .env file
        self.legiscan_key = os.getenv('legiscan_key')
        self.root = 'https://api.legiscan.com'
        self.MONGO_INITDB_ROOT_USERNAME=os.getenv('MONGO_INITDB_ROOT_USERNAME') 
        self.MONGO_INITDB_ROOT_PASSWORD=os.getenv('MONGO_INITDB_ROOT_PASSWORD') 
        url = 'https://httpbin.org/user-agent'
        r = requests.get(url)
        if r.status_code==200:
            useragent = json.loads(r.text)['user-agent']
            self.headers = {
                'User-Agent': useragent,
                'From': 'jkropko@virginia.edu'
            }
        else:
            useragent = json.loads(r.text)['user-agent']
            self.headers = {
                'User-Agent': 'python-requests/2.32.3',
                'From': 'jkropko@virginia.edu'
            }

    def get_sessions(self, make_csv=False):
        params = {'key': self.legiscan_key,
                 'op': 'getSessionList'}
        r = requests.get(self.root, params=params, headers=self.headers)
        myjson = json.loads(r.text)
        session_df = pd.json_normalize(myjson, record_path = ['sessions'])
        if make_csv:
            sessions_df.query("sine_die==1")['session_id'].to_csv('concluded_session_ids.csv', index=False)
        return session_df

    def get_bill_list(self, sessionid, make_file=False):
        params = {'key': self.legiscan_key,
                  'op': 'getMasterList',
                  'id': sessionid}
        r = requests.get(self.root, params=params, headers=self.headers)
        myjson = json.loads(r.text)['masterlist']
        session_json = myjson['session']
        del myjson['session']
        bill_df = pd.DataFrame(myjson).T
        bill_json_list = [self.get_onebill_info(x) for x in bill_df['bill_id']]
        if make_file:
            state = myjson['0']['url'][21:23] 
            session_name = session_json['session_name'].lower().replace(' ', '_')
            filename = f'Data/bills_{state}_{session_name}.json'
            with open(filename, 'w') as fp:
                json.dump(bill_json_list, fp)
        return bill_df, bill_json_list

    def clean_text(self, text):
        # Remove page headers/footers and line numbers
        cleaned_text = re.sub(r'HB\d+ INTRODUCED|Page \d+|K\d+[A-Z]+-\d+|PFD:\s?\d{2}-[A-Za-z]{3}-\d{2,4}|RFD:.*|First Read:.*|ZAK.*\d{4}-\d{4}', '', text)
        
        # Remove multiple line breaks and redundant spaces
        cleaned_text = re.sub(r'\n+', '\n', cleaned_text)
        cleaned_text = re.sub(r'\s+', ' ', cleaned_text)
        
        # Remove line numbers and extra spaces around punctuation
        cleaned_text = re.sub(r'\d+', '', cleaned_text)
        cleaned_text = re.sub(r'\s([.,;])', r'\1', cleaned_text)
    
        # Strip any leading or trailing spaces
        cleaned_text = cleaned_text.strip()
    
        # Remove section numbering like (a) and (b)
        cleaned_text = re.sub(r'\s*\([a-zA-Z]\)\s*', ' ', cleaned_text)
    
        # Remove dollar signs, legal sign, empty paranetheses
        cleaned_text = cleaned_text.replace('($)', '')
        cleaned_text = cleaned_text.replace('($,)', '')
        cleaned_text = cleaned_text.replace('§', '')
        cleaned_text = cleaned_text.replace('()', '')

        return cleaned_text
    
    def get_bill_text(self, textlink):
        response = requests.get(url=textlink, headers=self.headers, timeout=120)
        response = requests.get(url=textlink, headers=self.headers, timeout=120)
        on_fly_mem_obj = io.BytesIO(response.content)
        pdf_file = PdfReader(on_fly_mem_obj)
        textlist = [x.extract_text() for x in pdf_file.pages]
        fulltext = ' '.join(textlist)
        clean_text = self.clean_text(fulltext)
        return clean_text

    def get_onebill_info(self, billid):
        print(billid)
        :
        params = {'key': self.legiscan_key,
                  'op': 'getBill',
                  'id': billid}
        r = requests.get(self.root, params=params, headers=self.headers)
        myjson = json.loads(r.text)
        try:
            myjson['text'] = self.get_bill_text(myjson['bill']['texts'][0]['state_link'])
        except:
            myjson['text'] = ''
        return myjson

    def mongo_read_query(self, col, q):
        qtext = dumps(col.find(q))
        qrec = loads(qtext)
        qdf = pd.DataFrame.from_records(qrec)
        return qdf

    def mongo_connect(self, billtext_from_scratch=False):
        myclient = pymongo.MongoClient(f"mongodb://{MONGO_INITDB_ROOT_USERNAME}:{MONGO_INITDB_ROOT_PASSWORD}@mongo:27017/")
        legiscan_mongo = myclient['legiscan']
        billtext_mongo = legiscan_mongo['billtext']
        if billtext_from_scratch:
            collist = legiscan_mongo.list_collection_names()
            if "billtext" in collist:
              legiscan_mongo.billtext.drop()
            billtext_mongo = legiscan_mongo['billtext']
        return billtext_mongo

    #insert all bills from one session
    def insert_list_of_bills(self, col, bill_list):
        col.insert_many(bills_list)
        

    #loop over sessions/states and insert all bills into legiscan mongo DB

    


        