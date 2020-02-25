#!/usr/bin/env python3

"""
A simple script to collect information about access-session on the switch.
- login to the switch
- collect all mac addresses from access-sessions
- check access-session for each mac address
- if there is FAIL in the dACL - collect info about this session:
    - interface
    - mac_address
    - ip_address
    - user_name
    - method (mab|dot1x)
    - vendor (for mab)
"""

# Imports
import re
import paramiko
import netmiko
import pprint
import time
from local import switch_credentials
import requests


def try_to_connect_ssh(current_ip_address):
    try:
        connection = netmiko.ConnectHandler(device_type='cisco_ios_ssh',
                                            ip=current_ip_address,
                                            username=switch_credentials['username'],
                                            password=switch_credentials['password'],
                                            secret=switch_credentials['secret'],
                                            )
        connection.enable()
        return connection
    except paramiko.AuthenticationException:
        print('Auth failed')
        return
    except:
        print('Failed')
        return



class Device:

    def __init__(self, current_ip_address):
        self.current_ip_address = current_ip_address
        self.dict_result = {}

    def init_connection_ssh(self):
        self.connection = try_to_connect_ssh(self.current_ip_address)

    def close_connection(self):
        self.connection.disconnect()

    def collect_active_sessions(self):
        """
        collect all mac addressess if active sessions and store mac address in the list
        :return:
        self.session_count - count of all sessions on the switch
        self.mac_addresses - all mac addresses of access-sessions (authentication sessions)
        """
        self.connection.send_command("term len 0")
        active_sessions = self.connection.send_command("show access-session")
        self.session_count = re.findall('Session count = (\d+)\n', active_sessions)
        self.mac_addresses = re.findall(r'[0-9a-fA-F]{4}\.[0-9a-fA-F]{4}\.[0-9a-fA-F]{4}', active_sessions)

    def collect_active_sessions_details(self):
        """
        collect details for each session. If there is FAIL in the output - collect:
        - interfcace
        - mac-address
        - method
        - status
        - user_name
        - vendor
        :return:dict_result
         '<MAC-ADDRESS>': {'interface': 'GigabitEthernetX/X',
                    'ip_address': '<IP_ADDRESS>',
                    'mac_address': '<MAC-ADDRESS>',
                    'method': '<MAB/DOT1X>',
                    'status': 'Authz Success',
                    'user_name': 'AA-AA-AA-AA-AA-AA',
                    'vendor': 'Cisco Systems, Inc'}}

        """
        dict_result = {}
        for each in self.mac_addresses:
            session_details = self.connection.send_command("show access-session mac " + each + ' details')
            if 'FAIL' in session_details or 'Unauthorized' in session_details:
                mac_address = re.findall(r'[0-9a-fA-F]{4}\.[0-9a-fA-F]{4}\.[0-9a-fA-F]{4}', session_details)
                ip_address = re.findall(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}', session_details)
                method = re.findall(r'(\w{3,5})\s+Authc\s.*', session_details)
                status = re.findall('Status:  (.*)', session_details)
                dict_session_details = {}
                dict_session_details['status'] = status[0]
                dict_session_details['interface'] = re.findall(r'Interface: (.*)', session_details)[0]
                dict_session_details['mac_address'] = mac_address[0]
                if ip_address:
                    dict_session_details['ip_address'] = ip_address[0]
                else:
                    dict_session_details['ip_address'] = 'unknown'
                dict_session_details['user_name'] = re.findall(r'User-Name:\s+(.*)', session_details)[0]
                dict_session_details['method'] = method[0]
                if method[0] == 'mab':
                    url = 'https://api.macvendors.com/' + mac_address[0]
                    response = requests.get(url)
                    dict_session_details['vendor'] = response.text
                    time.sleep(1)

                self.dict_result[each] = dict_session_details
            else:
                continue

    def get_result(self):
        return self.dict_result


def main(current_ip_address):
    start_time = time.time()
    device = Device(current_ip_address)
    device.init_connection_ssh()
    device.collect_active_sessions()
    device.collect_active_sessions_details()
    dict_result = device.get_result()
    device.close_connection()
    with open('static/result.json', 'w', newline='') as f:
        pprint.PrettyPrinter(stream=f).pprint(dict_result)
    return dict_result


if __name__ == "__main__":
    #if len(sys.argv) == 2:
    #    main(sys.argv[1])
    #else:
    #    raise SyntaxError("Insufficient arguments.")
    main('10.13.1.5')

