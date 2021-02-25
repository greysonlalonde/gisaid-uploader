from itertools import islice
import json, hashlib, requests, time
import pandas as pd
from Bio import SeqIO


def request_authentication_token(client_id, user, pswd, file):

    password = pswd.encode("utf8")

    salt = secrets.token_urlsafe(64)
    hashed = (
        salt + "/" + sha512_hexdigest((salt + sha512_hexdigest(pswd)).encode("ascii"))
    )

    resp = requests.post(
        urls="https://gpsapi.epicov.org/epi3/gps_api",
        data={
            "cmd": "state/auth/get_token",
            "api": {"version": 1},
            "ctx": "CoV",
            "client_id": client_id,
            "login": user,
            "hash": hashed,
        },
    )
    if resp["rc"] == "ok":
        with open(file, "w") as f:
            json.dump(
                {
                    "api": {"version": 1},
                    "ctx": "CoV",
                    "client_id": client_id,
                    "client_token": resp["auth_token"],
                }
            )
        print("Auth file written")
    else:
        print(f'Auth failed: {resp["rc"]}')
    return resp["rc"]


def sha512_hexdigest(inp):
    hasher = hashlib.sha512()
    hasher.update(inp)
    return hasher.hexdigest()


def split_every(n, iterable):
    iterable = iter(iterable)
    yield from iter(lambda: list(islice(iterable, n)), [])


def read_files(*args):
    files = [".json", ".csv", ".fasta", ".fna", ".ffn", ".faa", ".frn"]
    for i, x in enumerate(args):
        if x.lower().endswith(files[0]):
            with open(x, "r") as authfile:
                auth = json.loads(authfile.read())
        elif x.lower().endswith((files[2])):
            seq = {k.id: str(k.seq) for k in SeqIO.parse(x, "fasta")}
        elif x.lower().endswith(files[1]):
            metadata = pd.read_csv(x).apply(lambda x: x.to_dict(), axis=1)
            {
                i.update({"covv_sequence": seq[k] for k in i.values() if k in seq})
                for i in metadata
            }
        else:
            print("Invalid file")
    return [split_every(500, metadata), auth]


