import pandas as pd
import json
from Bio import SeqIO
import requests, secrets, hashlib, json
from itertools import islice


class GiSaid(object):
    def __init__(self):
        self = None
    
    def split_every(self,n, iterable):
        iterable = iter(iterable)
        yield from iter(lambda: list(islice(iterable,n)), [])
    
    def login(self, auth_file, csv_file, fasta_file):
        with open(auth_file, "r") as authfile:
            self.auth = json.loads(authfile.read())
       
            
        self.seq = {k.id:str(k.seq) for k in SeqIO.parse(fasta_file, 'fasta')}    
        data = pd.read_csv(csv_file).apply(lambda x: x.to_dict(), axis=1)
        {i.update({'covv_sequence':self.seq[k] for k in i.values() if k in self.seq}) for i in data}
        self.data = self.split_every(500, data)
        
        
        
    def upload(self):
        count = 0
        s = requests.Session()
        urls = "https://gpsapi.epicov.org/epi3/gps_api"
        resp1 = (s.post(url=urls,
                data=json.dumps({"cmd": "state/session/logon",
                 "api": {"version": 1},
                 "ctx": 'CoV',
                 "client_id":self.auth["client_id"],
                 "auth_token":self.auth["auth_token"]}))).json()
        
        time.sleep(0.5) 
        resp2 = [s.post(url=urls, data=json.dumps({"cmd": "data/hcov-19/upload",
         "sid": resp1["sid"],
         "data": x[0],
         "submitter": x[0]["submitter"]})).json() for x in [i for i in self.data]]
        resp3 = s.post(url=urls, data=json.dumps({"cmd": "state/session/logoff"}))
        print(resp3)