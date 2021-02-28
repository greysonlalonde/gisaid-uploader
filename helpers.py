from itertools import islice
import json, requests, time
import pandas as pd
from Bio import SeqIO



def split_every(n, iterable):
    iterable = iter(iterable)
    yield from iter(lambda: list(islice(iterable, n)), [])


def read_files(args):
    options = [".json", ".csv", ".fasta", ".fna", ".ffn", ".faa", ".frn"]
 
    for x in args:
        if x.lower().endswith(options[0]):
            with open(x, "r") as authfile:
                authf = json.loads(authfile.read())


        elif x.lower().endswith((options[2])):
            seq = {k.id: str(k.seq) for k in SeqIO.parse(x, "fasta")}


        elif x.lower().endswith(options[1]):
            metadata = pd.read_csv(x).apply(lambda x: x.to_dict(), axis=1)
            {i.update({"covv_sequence": seq[k] for k in i.values() if k in seq}) for i in metadata}

        else:
            pass

        
    d = [split_every(500, metadata), authf]                             
    return d