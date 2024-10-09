import pandas as pd # works like tidydata
import numpy as np # works with matrices
import requests # conducts web transactions
import json # works with json style data
import dotenv # works with .env files
import os # allows for operating system level commands
import re # regular expressions
import io
from PyPDF2 import PdfReader

class legiscanscraper:
    def __init__(self):
        dotenv.load_dotenv() # finds and loads (silently) the .env file
        self.legiscan_key = os.getenv('legiscan_key')
        self.root = 'https://api.legiscan.com'

    def get_useragent(self):
            url = 'https://httpbin.org/user-agent'
            r = requests.get(url)
            useragent = json.loads(r.text)['user-agent']
            return useragent
        
    def make_headers(self,  email='jkropko@virginia.edu'):
            useragent=self.get_useragent()
            headers = {
                    'User-Agent': useragent,
                    'From': email
            }
            return headers

    def get_sessions(self):
        params = {'key': self.legiscan_key,
                 'op': 'getSessionList'}
        r = requests.get(self.root, params=params, headers=self.make_headers())
        myjson = json.loads(r.text)
        session_df = pd.json_normalize(myjson, record_path = ['sessions'])
        return session_df

    def get_bill_list(self, sessionid):
        params = {'key': self.legiscan_key,
                  'op': 'getMasterList',
                  'id': sessionid}
        r = requests.get(self.root, params=params, headers=self.make_headers())
        myjson = json.loads(r.text)['masterlist']
        del myjson['session']
        bill_df = pd.DataFrame(myjson).T
        return bill_df

    def get_onebill_info(self, billid):
        params = {'key': self.legiscan_key,
                  'op': 'getBill',
                  'id': billid}
        r = requests.get(self.root, params=params, headers=self.make_headers())
        myjson = json.loads(r.text)
        toreturn = {}
        toreturn['bill_id'] = myjson['bill']['bill_id']
        toreturn['session_id'] = myjson['bill']['session_id']
        toreturn['title'] = myjson['bill']['title']
        toreturn['description'] = myjson['bill']['description']
        toreturn['textlink'] = myjson['bill']['texts'][0]['state_link']
        return toreturn

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
        response = requests.get(url=textlink, headers=self.make_headers(), timeout=120)
        on_fly_mem_obj = io.BytesIO(response.content)
        pdf_file = PdfReader(on_fly_mem_obj)
        textlist = [x.extract_text() for x in pdf_file.pages]
        fulltext = ' '.join(textlist)
        clean_text = self.clean_text(fulltext)
        return clean_text
        
                