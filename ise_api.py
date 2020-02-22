import requests
import response as response
from requests.auth import HTTPBasicAuth
from local import ise_credentials
from typing import List, Set, Dict, Tuple, Optional

# Disable warnings(InsecureRequestWarning) because of the certificate
from requests.packages.urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

headers = {
    'Content-Type': 'application/json',
    'Accept': 'application/json',
}
user = ise_credentials['username']
password = ise_credentials['password']
#base_url = ise_credentials['base_url']
base_url = 'https://3.45.48.12:9060/ers/config/'

def get_group_id() -> dict:
    """
    Collect all group IDs from Cisco ISE
    return: dict{'group_id': group_name}
    """
    url = base_url + "endpointgroup"
    payload = {}
    ise_groups = {}
    while True:
        response = requests.request("GET", url, auth=HTTPBasicAuth(user, password), headers=headers, data=payload,
                                    verify=False)
        data = response.json()
        for each in data['SearchResult']['resources']:
            ise_groups[each['id']] = each['name']
        if data['SearchResult']['nextPage']['href']:
            url = data['SearchResult']['nextPage']['href']
            continue
        else:
            break

    return ise_groups


def get_endpoint_group_id(mac: str) -> str:
    """
    Get endpoint id from MAC address
    :param mac: MAC address
    :return: endpoint_group_id string
    """
    url = base_url + "endpoint/name/" + mac
    payload = {}

    response = requests.request("GET", url, auth=HTTPBasicAuth(user, password), headers=headers, data=payload,
                                verify=False)
    data = response.json()
    endpoint_group_id = data['ERSEndPoint']['groupId']
    return endpoint_group_id


def update_endpoint_group(mac: str, ise_group_id: str):
    """
    Update endpoint group in ISE for MAC address
    :param mac: MAC address
    :param mac: ise_group_id - the ID of new ISE group
    :return: response for API request
    """
    url = base_url + "endpoint/name/" + mac
    payload = {}
    response = requests.request("GET", url, auth=HTTPBasicAuth(user, password), headers=headers, data=payload,
                                verify=False)
    data = response.json()
    endpoint_id = data['ERSEndPoint']['id']

    url = base_url + "endpoint/" + endpoint_id
    payload = "{\r\n\t\"ERSEndPoint\": {\r\n\t\t\"groupId\": \"" + ise_group_id + "\",\r\n\t\t\"staticGroupAssignment" \
                                                                                  "\": \"true\"\r\n        }\r\n} "

    response = requests.request("PUT", url, auth=HTTPBasicAuth(user, password), headers=headers, data=payload,
                                verify=False)
    return response


if __name__ == "__main__":
    get_group_id()
