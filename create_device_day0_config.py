#!/usr/bin/env python

# wonder if this makes sense?
'''
device_values = {
    '$hostname': 'overlaid-router',
    '$ip': '169.254.66.6',
    '$answer': 'yes'
}
'''


# Creata static content for Phase 1 - Ryan TBD?

ASAv_IMAGE_INPUT = "Chet-asa-image"
ASAv10_FLAVOR_INPUT = "Chet-asav10-flavor"
WAN_NET_INPUT = "10.100.3.3"
LAN_NET_INPUT = "10.100.40.2"
DEV_NAME_DERV_CSR_INPUT = "Chet-CSR-ASA"
DOM_NAME_INPUT = "chet.com"
MGT_IP_ADDRESS_INPUT = "20.20.20.1"
MGT_IP_MASK_INPUT = "255.255.255.128"
ASA_OUT_INT_IP_INPUT = "10.100.40.10"
ASA_OUT_INT_MASK_INPUT = "255.255.255.0"

# CREATING ENVS TO REPLACE
device = dict()

device["$ASAv_IMAGE"] = ASAv_IMAGE_INPUT
device["$ASAv10_FLAVOR"] = ASAv10_FLAVOR_INPUT
device["$WAN_NET"] = WAN_NET_INPUT
device["$LAN_NET"] = LAN_NET_INPUT
device["$DEV_NAME_DERV_CSR"] = DEV_NAME_DERV_CSR_INPUT
device["$DOM_NAME"] = DOM_NAME_INPUT
device["$MGT_IP_ADDRESS"] = MGT_IP_ADDRESS_INPUT
device["$MGT_IP_MASK"] = MGT_IP_MASK_INPUT
device["$ASA_OUT_INT_IP"] =ASA_OUT_INT_IP_INPUT
device["$ASA_OUT_INT_MASK"] = ASA_OUT_INT_MASK_INPUT


'''
# create  example:
device["$hostname"] = os.getenv('HOSTNAME_INPUT')
device["$hostname"] = raw_input("\nHostname: ")
'''


def replace_words(base_text, device_values):
    for key, val in device_values.items():
        base_text = base_text.replace(key, val)
    return base_text


# Open your desired file as 't' and read the lines into string 'tempstr'
def create_device_cfg(create_asa_name):
    t = open('device_data_template.txt', 'r')
    tempstr = t.read()
    t.close()

    day_zero_cfg = "%s-day0cfg.json" % create_asa_name

    output = replace_words(tempstr, device)

    fout = open(day_zero_cfg, 'w')
    fout.write(output)
    fout.close()
    return

