#!/usr/bin/env python


# Creata static content for Phase 1 - Ryan TBD?

ASAv_IMAGE_INPUT = "asav951-201-GADD.ova"   # ok
DEV_NAME_DERV_CSR_INPUT = "GADD-ASA"    # ok
MGMT_IP_INPUT = "20.20.20.10"       # ok
MGMT_MASK_INPUT = "255.255.255.0"   # ok
BVI_MASK_INPUT = "255.255.255.0"    # ok
SSH_USERNAME_INPUT = "cisco"        # ok
SSH_PASSWORD_INPUT = "cisco"        # ok
VNF_MGMT_GW_INPUT = "20.20.20.1"    # ok


# CREATING ENVS TO REPLACE
device = dict()

device["$ASAv_IMAGE"] = ASAv_IMAGE_INPUT    # ok
device["$DEV_NAME_DERV_CSR"] = DEV_NAME_DERV_CSR_INPUT  # ok
device["$MGMT_IP"] = MGMT_IP_INPUT  # ok
device["$MGMT_MASK"] = MGMT_MASK_INPUT  # ok
device["$BVI_MASK"] = BVI_MASK_INPUT    # ok
device["$SSH_USERNAME"] = SSH_USERNAME_INPUT    # ok
device["$SSH_PASSWORD"] = SSH_PASSWORD_INPUT    # ok
device["$VNF_MGMT_GW"] = VNF_MGMT_GW_INPUT      # ok

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
def create_device_cfg(r_asa_flavor, new_network, r_bvi_gw, r_bvi_ip):
    device["$ASA_FLAVOR"] = r_asa_flavor     # dreived from CSR flavor (values are: ASAv5, ASAv10, ASAv30)
    device["$NEW_NETWORK"] = new_network     # drived from ryans function
    device["$BVI_IP"] = r_bvi_ip             # derived from Lan ip of CSR
    device["$BVI_GW"] = r_bvi_gw             # equals lan IP of CSR

    t = open('device_data_template.txt', 'r')
    tempstr = t.read()
    t.close()

    day_zero_cfg = "%s_input_cfg.json" % DEV_NAME_DERV_CSR_INPUT

    output = replace_words(tempstr, device)

    fout = open(day_zero_cfg, 'w')
    fout.write(output)
    fout.close()
    if len(day_zero_cfg) > 0:
        return True
    else:
        return False
