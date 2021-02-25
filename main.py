import requests, secrets, json
from helpers import *


class GiSaid:
    """
    Class for uploading & downloading to GISAID.
    Provides a route for automation or back-end integration.

    Parameters
    ----------
    args:
        csv_path, fasta_path, jsoncred_path or authentication info


    Returns
    ----------
    response:
        output from request


    Examples
    ----------
    >>> gs = GiSaid('authenticate', client_id, username, pswd, filename)
    Authentication successful
    """

    def __init__(self, *args):
        if args[0] == "authenticate":
            self.data = read_files(args)
        else:
            self.data = read_files(args[0], args[1], args[2])

    def upload(self):
        """
        Uploading method

        Parameters
        ----------
        args:
            csv_path, fasta_path, jsoncred_path


        Returns
        ----------
        response:
            output from request


        Examples
        ----------
        >>> gs = GiSaid(csv_file, fasta_file, jsoncred_file)
        >>> gs.upload()
        Upload successful
        """
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
        print(resp3.json())
