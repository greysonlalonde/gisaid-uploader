from itertools import islice
import json
import pandas as pd
from Bio import SeqIO
from main import GiSaid


def split_every(n, iterable):
    iterable = iter(iterable)
    yield from iter(lambda: list(islice(iterable, n)), [])


def read_files(auth_file, csv_file, fasta_file):
    with open(auth_file, "r") as authfile:
        auth = json.loads(authfile.read())

    seq = {k.id: str(k.seq) for k in SeqIO.parse(fasta_file, "fasta")}
    data = pd.read_csv(csv_file).apply(lambda x: x.to_dict(), axis=1)
    {i.update({"covv_sequence": seq[k] for k in i.values() if k in seq}) for i in data}
    data = split_every(500, data)


def sha512_hexdigest(inp):
    hasher = hashlib.sha512()
    hasher.update(inp)
    return hasher.hexdigest()