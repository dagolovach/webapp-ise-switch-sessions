import requests
from requests.auth import HTTPBasicAuth
from local import ise_credentials

# Disable warnings(InsecureRequestWarning) because of the certificate
from requests.packages.urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

headers = {
    'Content-Type': 'application/json',
    'Accept': 'application/json',
}
user = ise_credentials['username']
password = ise_credentials['password']
base_url = ise_credentials['base_url']


def get_group_id():
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


def get_endpoint_group_id(mac):
    url = base_url + "endpoint/name/" + mac
    payload = {}

    response = requests.request("GET", url, auth=HTTPBasicAuth(user, password), headers=headers, data=payload,
                                verify=False)
    data = response.json()
    endpoint_group_id = data['ERSEndPoint']['groupId']
    return endpoint_group_id


def update_endpoint_group(mac, ise_group_id):
    url = base_url + "endpoint/name/" + mac

    payload = {}

    response = requests.request("GET", url, auth=HTTPBasicAuth(user, password), headers=headers, data=payload,
                                verify=False)
    data = response.json()
    endpoint_id = data['ERSEndPoint']['id']

    url = base_url + "endpoint/" + endpoint_id
    print(url)
    str_ise_group_id = '"' + ise_group_id + '"'
    print(str_ise_group_id)
    payload = "{\r\n\t\"ERSEndPoint\": {\r\n\t\t\"groupId\": \"" + ise_group_id + "\",\r\n\t\t\"staticGroupAssignment" \
                                                                                  "\": \"true\"\r\n        }\r\n} "

    response = requests.request("PUT", url, auth=HTTPBasicAuth(user, password), headers=headers, data=payload,
                                verify=False)
    print(response.text)
    return response


if __name__ == "__main__":
    get_group_id()
