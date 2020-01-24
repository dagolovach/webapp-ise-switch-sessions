#!/usr/bin/env python3

"""
get into the switch
show failed access-sessions and method + mac address + IP address + name
"""

credentials = {
    'username': ['iementor3'],
    'password': ['gb4qzNdrry@f0C'],
    'secret': ['gb4qzNdrry@f0C'],
}

dict_result = {}

# Imports
import time
import re
import paramiko
import netmiko
import pprint
from mac_vendor_lookup import MacLookup


def try_to_connect_ssh(current_ip_address):
    for count in range(0, len(credentials['username'])):
        try:
            connection = netmiko.ConnectHandler(device_type='cisco_ios_ssh',
                                                ip=current_ip_address,
                                                username=credentials['username'][count],
                                                password=credentials['password'][count],
                                                secret=credentials['secret'][count],
                                                )
            connection.enable()
            return connection
        except paramiko.AuthenticationException:
            continue
        except:
            print('Failed')
            return


class Device:

    def __init__(self, current_ip_address):
        self.current_ip_address = current_ip_address

    def init_connection_ssh(self):
        self.connection = try_to_connect_ssh(self.current_ip_address)

    def close_connection(self):
        self.connection.disconnect()

    def collect_active_sessions(self):
        self.connection.send_command("term len 0")
        active_sessions = self.connection.send_command("show access-session")
        self.session_count = re.findall('Session count = (\d+)\n', active_sessions)
        self.mac_addresses = re.findall(r'[0-9a-fA-F]{4}\.[0-9a-fA-F]{4}\.[0-9a-fA-F]{4}', active_sessions)

    def collect_active_sessions_details(self):
        for each in self.mac_addresses:
            session_details = self.connection.send_command("sho access-session mac " + each + " details")
            if 'FAIL' in session_details:
                # interface = re.findall(r'Interface: (.*)', session_details)
                mac_address = re.findall(r'[0-9a-fA-F]{4}\.[0-9a-fA-F]{4}\.[0-9a-fA-F]{4}', session_details)
                # ip_address = re.findall(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}', session_details)
                # user_name = re.findall(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}', session_details)
                method = re.findall(r'(\w{3,5})\s+Authc Success', session_details)
                dict_session_details = {}
                dict_session_details['interface'] = re.findall(r'Interface: (.*)', session_details)[0]
                dict_session_details['mac_address'] = mac_address[0]
                dict_session_details['ip_address'] = re.findall(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}', session_details)[
                    0]
                dict_session_details['user_name'] = re.findall(r'User-Name:\s+(.*)', session_details)[0]
                dict_session_details['method'] = method[0]
                if method[0] == 'mab':
                    mac_string = ''.join([mac_address[0][i] for i in range(0, len(mac_address[0])) if mac_address[0][i] != '.'])
                    dict_session_details['vendor'] = MacLookup().lookup(
                        ':'.join(mac_string[i:i + 2] for i in range(0, 12, 2)))

                dict_result[each] = dict_session_details
            else:
                continue


def main(current_ip_address):
    device = Device(current_ip_address)
    device.init_connection_ssh()
    device.collect_active_sessions()
    device.collect_active_sessions_details()
    device.close_connection()
    pprint.PrettyPrinter(depth=4).pprint(dict_result)
    with open('devices-result.csv', 'w', newline='') as f:
        pprint.PrettyPrinter(depth=4, stream=f).pprint(dict_result)


if __name__ == "__main__":
    start_time = time.time()
    main('10.18.1.250')
    print(time.time() - start_time)
