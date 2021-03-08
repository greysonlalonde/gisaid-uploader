import hashlib
import json
import requests
import secrets
from configparser import ConfigParser, NoSectionError


def authfile():
    try:
        config = ConfigParser()
        config.read('config.py')
        auth_path = config.get('FILES', 'AUTH_FILE')
    except NoSectionError:
        print("config.py not found")
    with open(auth_path, "r") as f:
        authf = json.loads(f.read())
    return authf


def authenticate(kwargs):
    """
    kwargs = 'authenticate=True,password=password,
    client_id=client_id, user=user,file=file'
    """

    password = kwargs['password'].encode("utf8")

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
            "client_id": kwargs['client_id'],
            "login": kwargs['user'],
            "hash": hashed,
        },
    )
    if resp.json()["rc"] == "ok":
        with open(kwargs['file'], "w") as f:
            json.dump(
                {
                    "api": {"version": 1},
                    "ctx": "CoV",
                    "client_id": kwargs['client_id'],
                    "client_token": resp["auth_token"],
                }
            )
        config.read('config.py')
        config.add_section('FILES')
        config.set('FILES', 'AUTH_FILE', kwargs['file'])

        with open('../config.py', 'w') as f:
            config.write(f)

    else:
        resp = f'Authentication failed: {resp.json()["rc"]}'
    return print(resp)


def sha512_hexdigest(inp):
    hasher = hashlib.sha512()
    hasher.update(inp)
    return hasher.hexdigest()
