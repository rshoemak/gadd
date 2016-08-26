
import requests
import sys
import creds
import events
import sparky
import acitoolkit.acitoolkit as aci
import aci_data
import nfvis_data
import message_board
import create_device_input_config

# Main Program

new_bridge = "svc-gadd-br"      # Statically assigned for Phase 1 or will we make dynamic?
new_network = "svc-gadd-net"    # Statically assigned for Phase 1 or will we make dynamic?
deep_key = False
r_bvi_ip = ""
r_bvi_gw = ""
device_name = ""
dev_id = ""
r_asa_flavor = ""


def do_message_(mess):
    sparky.send_alert(alert_room_id, mess)
    return


if __name__ == '__main__':

    trigger = events.trigger_event()

    # test for trigger event
    if not trigger:
        print "no trigger"
        sys.exit(0)

    # basic credential setup for NFVis device
    url, login, password = creds.nvfis_getgcred()
    s = requests.Session()
    s.auth = (login, password)
    s.headers = ({'Content-type': 'application/vnd.yang.data+json', 'Accept': 'application/vnd.yang.data+json'})
    s.verify = False    # I don't know if this is needed

    # log into APIC
    a_url, a_login, a_password = creds.apic_GetArgs()
    session = aci.Session(a_url, a_login, a_password)
    session.verify_ssl = False  # I don't know if this is needed
    a_resp = session.login()
    if not a_resp.ok:
        print "%% Could not login to APIC"
        sys.exit(0)

    # Create room if not already created.
    # Add in additional members manually. To do: make automatic
    alert_room_id = sparky.setup_room()


# ####################  -- APIC SECTION --  ####################

    # ACI metric calls
    do_message_(message_board.liner)
    aci_app_health = aci_data.get_overall_app_health(session)
    do_message_(aci_app_health)
    aci_egress_data = aci_data.get_egress_app_data(session)
    do_message_(aci_egress_data)
    aci_ingress_data = aci_data.get_ingress_app_data(session)
    do_message_(aci_ingress_data)
    do_message_(message_board.liner)


# ####################  -- NFV SECTION --   ####################

    # Step 1: Get CSR device name and device_name_id
    dev_name, dev_id = nfvis_data.nfv_prune_name(s, url)

    # Step 2: Get LAN IP of CSR
    r_bvi_ip, r_bvi_gw = nfvis_data.nfv_prune_bvi_ip(s, url, dev_id)

    # Step 3: Get image flavor
    r_flavor = nfvis_data.nfv_prune_flavor(s, url, dev_id)
    if r_flavor:
        do_message_(message_board.nfv_gather_basics)
    else:
        print "Could NOT gather data on NFVIS device"
        sys.exit(0)

    # Step 3: Get ASA Flavor
    r_asa_flavor = nfvis_data.nfv_get_asa_flavor(r_flavor)
    if r_asa_flavor:
        print "CSR FLAVOR: %s    BVI_IP: %s    DEV_NAME: %s    DEV_ID: %s    ASA_FLAVOR: %s" \
              % (r_flavor, r_bvi_ip, dev_name, dev_id, r_asa_flavor)
        print "NEW_NETWORK: %s    NEW_BRIDGE: %s    BVI_GW: %s" % (new_network, new_bridge, r_bvi_gw)
    else:
        print "%% Could NOT get ASA flavor"
        sys.exit(0)

    '''
    # Step 5:  Create LAN Bridge
    r_create_lanbridge = nfvis_data.nfv_create_newbridge(s, url, new_bridge)
    if r_create_lanbridge:  # What will be the code or do we need to do a verify functions?
        do_message_(message_board.nfv_created_lanbridge)
    else:
        print "%% Could NOT create lan bridge"
        do_message_(message_board.nfv_lanbridge_failed)
        sys.exit(0)

    # Step 6:  Create new network and map to lan bridge
    r_create_net = nfvis_data.nfv_create_new_network(s, url, new_network, new_bridge)
    if r_create_net:    # What will be the code or do we need to do a verify functions?
        do_message_(message_board.nfv_created_net_and_mapped)
    else:
        print "%% Could NOT create network and map to lan bridge"
        do_message_(message_board.nfv_net_map_failed)
        sys.exit(0)
    '''

    # Step 7:  Create json payload to instantiate device
    r_created_input_cfg = create_device_input_config.create_device_cfg(r_asa_flavor, new_network, r_bvi_gw, r_bvi_ip)
    if r_created_input_cfg:
        do_message_(message_board.nfv_creating_cfg)
    if not r_created_input_cfg:
        print "%% Could NOT create INPUT config"
        do_message_(message_board.nfv_input_cfg_failed)
        sys.exit(0)

    # Step 8:  Deployment
    # Do something...

    # Need ability to wait for response 'ack' from NFVis deployment. Add sleep timer?.
    aci_post_health = aci_data.get_post_app_health(session)
    do_message_(message_board.liner)
    do_message_(aci_post_health)
