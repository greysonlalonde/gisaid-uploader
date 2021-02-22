import pandas as pd
import json
import requests


def handles(filename, csv_file, params):
    global proxy
    
    data = (pd.read_csv(csv_file).query("Final_Decision == 'yes' \
             & sequence == sequence").apply(lambda x: x.to_json(), axis=1))
    try:
        with open(filename, "r") as file:
            d_auth = json.loads(file.read())
    except FileNotFoundError:
        print('File not found')
    
    params = {"cmd": "state/session/logon", "api":{"version": 1},
              "ctx":"CoV", "client_id":d_auth["client_id"],
              "auth_token":d_auth["auth_token"]}
    
    
    
   
    body = json.dumps(params)
    try:
        r = requests.post(get_service_url(), data=body, proxies=proxy)
        time.sleep(0.1)
    except requests.exceptions.ProxyError:
        if debug:
            raise
        else:
            return {"rc": "proxy_error"}
    except KeyboardInterrupt:
        raise
    except:
        if debug:
            raise
        else:
            return {"rc": "connection_error"}
    count = 0    
    for i in data:
        body2 = {"cmd": "data/hcov-19/upload",
                         "api": {"version": 1},
                         "sid": r.json()['sid'],
                         "ctx": "CoV",
                         "data": i,
                         "submitter": json.dumps(json.loads(i)['analyst'])}
        
        r = requests.post(get_service_url(), data=body2, proxies=proxy)
        
    body3 =  {"cmd": "state/session/logoff",
                "api": {"version": 1},
                "ctx": 'CoV',
                "sid": r.json()['sid']}
    r = request.post(get_service_url(),data=body3, proxies=proxy)
    return count