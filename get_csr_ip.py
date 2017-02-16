#!/usr/bin/env python

from ncclient import manager
import sys
try:
    from lxml import etree as ET
except ImportError:
    import xml.etree.ElementTree as ET
import xml.dom.minidom

# the variables below assume the user is leveraging the
# GADD lab environment and accessing csr1000v
# use the user credentials for your CSR1000V device
USER = 'admin'
PASS = 'Chicagoland_123'
# XML file to open
FILTER = 'get_interfaces_filter.xml'

def get_configured_interfaces(xml_filter, nip, isrv_netconf_port):
    """
    Main method that retrieves the interfaces from config via NETCONF.
    """
    with manager.connect(host=nip, port=isrv_netconf_port, username=USER,
                         password=PASS, hostkey_verify=False,
                         device_params={'name': 'default'},
                         allow_agent=False, look_for_keys=False) as m:
        with open(xml_filter) as f:
            return(m.get_config('running', f.read()))


def get_lan_ip(nip, isrv_netconf_port):
    """
    Simple main method calling our function.
    """
    interfaces = get_configured_interfaces(FILTER, nip, isrv_netconf_port)

 #   if you want to see the XML parsed output, you can uncomment the line below.
 #   print(xml.dom.minidom.parseString(interfaces.xml).toprettyxml())

    root = ET.fromstring(interfaces.xml)

    for interface in root.iter('{urn:ietf:params:xml:ns:yang:ietf-interfaces}interface'):
        for description in interface.findall('{urn:ietf:params:xml:ns:yang:ietf-interfaces}description'):
            if description.text == 'LAN':
            #    print "Found LAN"
                for ip in description.findall("..//{urn:ietf:params:xml:ns:yang:ietf-ip}ip"):
                    ISRv_LAN_IP = ip.text
                    return ISRv_LAN_IP
