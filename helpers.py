from itertools import islice
import json, hashlib, requests, time, secrets
import pandas as pd
from Bio import SeqIO


def auth(li):
    """
    args = 'client_id, user, password, file'
    """
    password = li[2].encode("utf8")

    salt = secrets.token_urlsafe(64)
    hashed = (
        salt + "/" + sha512_hexdigest((salt + sha512_hexdigest(password)).encode("ascii"))
    )

    resp = requests.post(
        url="https://gpsapi.epicov.org/epi3/gps_api",
        data={
            "cmd": "state/auth/get_token",
            "api": {"version": 1},
            "ctx": "CoV",
            "client_id": li[0],
            "login": li[1],
            "hash": hashed,
        },
    )
    if resp.json()["rc"] == "ok":
        with open(li[3], "w") as f:
            json.dump(
                {
                    "api": {"version": 1},
                    "ctx": "CoV",
                    "client_id": li[1],
                    "client_token": resp["auth_token"],
                }
            )

    else:
        pass
    return resp

def sha512_hexdigest(inp):
    hasher = hashlib.sha512()
    hasher.update(inp)
    return hasher.hexdigest()


def split_every(n, iterable):
    iterable = iter(iterable)
    yield from iter(lambda: list(islice(iterable, n)), [])


def read_files(*args):
    options = [".json", ".csv", ".fasta", ".fna", ".ffn", ".faa", ".frn"]
    try:
        for i,x in enumerate(args):
            if x.lower().endswith(options[0]):
                with open(x, "r") as authfile:
                    authf = json.loads(authfile.read())


            elif x.lower().endswith((options[2])):
                seq = {k.id: str(k.seq) for k in SeqIO.parse(x, "fasta")}


            elif x.lower().endswith(options[1]):
                metadata = pd.read_csv(x).apply(lambda x: x.to_dict(), axis=1)

            elif x.lower() == 'authenticate':
                li = list(args)
                r = auth(li)
                if r.json()['rc'] == 'ok':
                    print('Authentication successful')
                else:
                    print(f'Authentication failed: {r.json()["rc"]}')
                
        {i.update({"covv_sequence": seq[k] for k in i.values() if k in seq}) for i in metadata}
        d = [split_every(500, metadata), authf]                   
    except IndexError as e:
        d = e
                         
    return d


