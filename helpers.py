from itertools import islice
import json, requests, time
import pandas as pd
from Bio import SeqIO
import re


def split_every(n, iterable):
    iterable = iter(iterable)
    yield from iter(lambda: list(islice(iterable, n)), [])


def check_file(fname):
    d = {}
    for i in fname[0]:
        if re.search("\.csv$", i, flags=re.IGNORECASE):
            d["csv"] = i
        elif re.search("\.json$", i, flags=re.IGNORECASE):
            d["cred"] = i
        elif re.search("\.fa$", i, flags=re.IGNORECASE):
            d["fa"] = i
        else:
            d['error'] = i
    return d


def read_files(args):
    data = check_file(args)
    try:
        with open(data["cred"], "r") as authfile:
            authf = json.loads(authfile.read())
        seq = {k.id: str(k.seq) for k in SeqIO.parse(data["fa"], "fasta")}

        metadata = pd.read_csv(data["csv"]).apply(lambda x: x.to_dict(), axis=1)
        {
            i.update({"covv_sequence": seq[k] for k in i.values() if k in seq})
            for i in metadata
        }
        
        d = [split_every(500, metadata), authf]
    except KeyError:
        d = print(f'{data["error"]} not found')
    

    
    return d
