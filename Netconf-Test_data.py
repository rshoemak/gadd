#!/usr/bin/env python
from ncclient import manager
import sys

HOST = '10.91.13.157'
PORT = 830
USER = 'admin'
PASS = 'Chicagoland_123'

def main():
    """
    Main method that prints NetConf capabilities of remote device.
    :return:
    """
    with manager.connect(host=HOST, port=PORT, username=USER, password=PASS, hostkey_verify=False,
                         device_params={'name': 'default'},
                         look_for_keys=False, allow_agent=False) as m:

        #print all NETCONF capabilities
        print('***Here are the remote capabilities***')
        for capability in m.server_capabilities:
            print(capability)

if __name__ == '__main__':
    sys.exit(main())


