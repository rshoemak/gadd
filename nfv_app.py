
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
import argparse

# Main Program

new_bridge = "svc-gadd-br"      # Statically assigned for Phase 1 or will we make dynamic?
new_network = "svc-gadd-net"    # Statically assigned for Phase 1 or will we make dynamic?
deep_key = False
r_bvi_ip = ""
r_bvi_gw = ""
# device_name = ""
# dev_id = ""
r_asa_flavor = ""
r_csr_flavor = ""
r_csr_id = ""
r_csr_vm_name_id = ""
# default is on, turn off if you'd like to not send messages to spark


def do_message_(mess):
    if spark_flag == "on":
        sparky.send_alert(alert_room_id, mess)
        return
    else:
        pass


def get_args():
    parser = argparse.ArgumentParser(description='Enable or Disable Spark Messaging')
    # Add arguments
    parser.add_argument('--spark', help='Disable Spark by typing "--spark off", default is on', type=str, default="on")
    return parser.parse_args()


args = get_args()
spark_flag = args.spark

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

    # Step 1a:  Find out how many VM's have been deployed
    r_vm_deployed_count = nfvis_data.nfv_get_count_of_vm_deployments(s, url)

    # Step 1b: Get CSR flavor, dev_name and vm_name
    r_csr_flavor, r_csr_id, r_csr_vm_name_id = nfvis_data.nfv_get_csr_cfg(s, url, r_vm_deployed_count)
    # print r_csr_flavor, r_csr_id, r_csr_vm_name_id

    # Step 2: Get LAN IP of CSR
    r_bvi_ip, r_bvi_gw = nfvis_data.nfv_prune_bvi_ip(s, url, r_csr_id)
    # print r_bvi_ip, r_bvi_gw

    # Step 3: Get ASA Flavor
    r_asa_flavor = nfvis_data.nfv_get_asa_flavor(r_csr_flavor)
    if r_asa_flavor:
        do_message_(message_board.nfv_gather_basics)
        print "CSR FLAVOR: %s    BVI_IP: %s    DEV_NAME: %s    DEV_ID: %s    ASA_FLAVOR: %s" \
              % (r_csr_flavor, r_bvi_ip, r_csr_vm_name_id, r_csr_id, r_asa_flavor)
        print "NEW_NETWORK: %s    NEW_BRIDGE: %s    BVI_GW: %s" % (new_network, new_bridge, r_bvi_gw)
    else:
        print "%% Could NOT get ASA flavor"
        sys.exit(0)

    # Step 5:  Create LAN Bridge
    r_create_lanbridge = nfvis_data.nfv_create_newbridge(s, url, new_bridge)
    if r_create_lanbridge:
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

    # Step 7a:  assign vnf network
    r_asgn_net = nfvis_data.nfv_assign_vnf_network(s, url, r_csr_id, new_network)
    if r_asgn_net:
        do_message_(message_board.nfv_mapped_vnf_network)
    if not r_asgn_net:
        print "%% Count NOT map VNF network"
        do_message_(message_board.nfv_mapped_vnf_network_failed)
        sys.exit(0)

    # Step 7b:  Create json payload to instantiate device
    r_created_input_cfg = create_device_input_config.create_device_cfg(r_asa_flavor, new_network, r_bvi_gw, r_bvi_ip)
    if r_created_input_cfg:
        do_message_(message_board.nfv_creating_cfg)
    if not r_created_input_cfg:
        print "%% Could NOT create INPUT config"
        do_message_(message_board.nfv_input_cfg_failed)
        sys.exit(0)

    # Step 8:  Deployment
    r_status_resp = nfvis_data.nfv_deploy_asa(s, url, r_created_input_cfg)
    if r_status_resp:
        do_message_(message_board.nfv_asa_deployment_success)
    else:
        do_message_(message_board.nfv_asa_deployment_failed)
        sys.exit(0)

    # Step 9:  Update ACI/GADD Health checks
    # Need ability to wait for response 'ack' from NFVis deployment. Add sleep timer?.
    aci_post_health = aci_data.get_post_app_health(session)
    do_message_(message_board.liner)
    do_message_(aci_post_health)
