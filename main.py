import requests, secrets, json
from helpers import *


class GiSaid:
    def __init__(self, auth, csv, fasta):
        self.data = read_files(auth, csv, fasta)

    def upload(self):
        s = requests.Session()
        urls = "https://gpsapi.epicov.org/epi3/gps_api"
        resp1 = (
            s.post(
                url=urls,
                data=json.dumps(
                    {
                        "cmd": "state/session/logon",
                        "api": {"version": 1},
                        "ctx": "CoV",
                        "client_id": self.data[1]["client_id"],
                        "auth_token": self.data[1]["auth_token"],
                    }
                ),
            )
        ).json()

        time.sleep(0.5)
        resp2 = [
            s.post(
                url=urls,
                data=json.dumps(
                    {
                        "cmd": "data/hcov-19/upload",
                        "sid": resp1["sid"],
                        "data": x[0],
                        "submitter": x[0]["submitter"],
                    }
                ),
            ).json()
            for x in [i for i in self.data[0]]
        ]
        resp3 = s.post(url=urls, data=json.dumps({"cmd": "state/session/logoff"}))
        print(resp3)