from gisaid.helpers import *
from gisaid.auth import *
import time


class GiSaid(object):
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
    >>> gs = GiSaid(authenticate=True, client_id=client_id,
    >>>              username=username, password=password, filename=filename)
    Authentication successful
    """

    def __init__(self, *args, **kwargs):
        if not kwargs:
            self.kwargs = None
            self.args = args
            self.data = read_files(self.args)
            self.authf = authfile()

        elif kwargs["authenticate"]:
            self.kwargs = kwargs
            self.args = None
            self.data = authenticate(self.kwargs)

        elif kwargs['collate_fasta']:
            self.kwargs = kwargs
            self.args = args
            self.data = collate_fa(self)
        else:
            if kwargs["authenticate"]:
                self.kwargs = kwargs
                self.args = None
                self.data = authenticate(self.kwargs)
            else:
                print('Invalid parameter')

    def upload(self):
        """
        Uploading method

        Parameters
        ----------
        self:
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
                        "client_id": self.authf["client_id"],
                        "auth_token": self.authf["client_token"],
                    }
                ),
            )
        )

        time.sleep(0.1)
        resp2 = [logfile(x['covv_virus_name'],
                         s.post(
                             url=urls,
                             data=json.dumps(
                                 {
                                     "cmd": "data/hcov-19/upload",
                                     "sid": resp1.json()["sid"],
                                     "data": x,
                                     "submitter": x["submitter"],
                                 }
                             ),
                         ).json())
                 for x in self.data]

        resp3 = s.post(url=urls, data=json.dumps({"cmd": "state/session/logoff"}))
        count = 0
        bad = 0
        with open('../logfile.csv') as f:
            for line in f:
                if 'success' in line:
                    count += 1
                else:
                    bad += 1
        print([i for i in resp2])
        print(resp3.json())
        print(f'{bad} failed uploads')
        print(f'{count} successful uploads')
