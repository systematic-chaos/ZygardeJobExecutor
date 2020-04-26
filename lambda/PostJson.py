'''
lambda/PostJson

Zygarde: Platform for reactive training of models in the cloud
Master in Big Data Analytics
Polytechnic University of Valencia

@author:    Javier Fernández-Bravo Peñuela
@copyright: 2020 Ka-tet Corporation. All rights reserved.
@license:   GPLv3.0
@contact:   fjfernandezbravo@iti.es
'''

import json
import sys
import urllib.error
import urllib.request

API_GATEWAY_URL = '/'.join(['https://rs4qb8njs8.execute-api.eu-west-1.amazonaws.com/dev', 'zygarde'])

def post_json_file(url, path):
    with open(path, 'r') as f:
        json_encoded = f.read().encode('utf8')
    return post_json_request(url, json_encoded)

def post_json_request(url, body):
    req = urllib.request.Request(url, data=body, headers={'Content-Type': 'application/json'})
    try:
        res = urllib.request.urlopen(req)
    except (urllib.error.URLError, urllib.error.HTTPError) as e:
        print(e)
        return None
    res = json.loads(res.read().decode('utf8'))
    return res

def main():
    url = sys.argv[1] if len(sys.argv) > 1 else API_GATEWAY_URL
    json_files = sys.argv[2:] if len(sys.argv) > 2 else ['request-body-full.json']

    print(url)
    for jf in json_files:
        print(jf)
        response = post_json_file(url, jf)
        print(response)

if __name__ == "__main__":
    main()
