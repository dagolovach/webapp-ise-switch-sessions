import requests
import json
from requests.auth import HTTPBasicAuth

# Disable warnings(InsecureRequestWarning) because of the certificate
from requests.packages.urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


def get_group_id():
    url = "https://3.45.48.12:9060/ers/config/endpointgroup"

    payload = {}
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'Authorization': 'Basic YWRtaW46VjByMHRuMWs='
    }
    ise_groups = {}
    while True:
        response = requests.request("GET", url, headers=headers, data=payload, verify=False)
        data = response.json()
        for each in data['SearchResult']['resources']:
            ise_groups[each['name']] = each['id']
        if data['SearchResult']['nextPage']['href']:
            url = data['SearchResult']['nextPage']['href']
            continue
        else:
            break

    return ise_groups


def update_endpoint_group(mac, ise_group_id):
    url = "https://3.45.48.12:9060/ers/config/endpoint/name/" + mac

    payload = {}
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'Authorization': 'Basic YWRtaW46VjByMHRuMWs='
    }
    response = requests.request("GET", url, headers=headers, data=payload, verify=False)
    data = response.json()
    endpoint_id = data['ERSEndPoint']['id']

    url = "https://3.45.48.12:9060/ers/config/endpoint/" + endpoint_id
    print(url)
    str_ise_group_id = '"' + ise_group_id + '"'
    print(str_ise_group_id)
    payload = "{\r\n\t\"ERSEndPoint\": {\r\n\t\t\"groupId\": \"" + ise_group_id + "\",\r\n\t\t\"staticGroupAssignment\": \"true\"\r\n        }\r\n}"

    response = requests.request("PUT", url, headers=headers, data=payload, verify=False)
    return response


if __name__ == "__main__":
    update_endpoint_group()
