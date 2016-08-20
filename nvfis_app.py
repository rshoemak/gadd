
import requests
import sys
# import json
import creds
# import staticvars
import events
import sparky
import acitoolkit.acitoolkit as aci
import aci_data
import nfvis_data
import message_board
# import time

# Main Program

new_bridge ="connie"

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
    s.verify = False

    # log into APIC
    a_url, a_login, a_password = creds.apic_GetArgs()
    session = aci.Session(a_url, a_login, a_password)
    session.verify_ssl = False
    a_resp = session.login()
    if not a_resp.ok:
        print "%% Could not login to APIC"
        sys.exit(0)

    # Create room if not already created.
    # Add in additional members manually. To do - add in automatically
    alert_room_id = sparky.setup_room()

    # Test NFVis login functionality
    r_imgs, r_message = nfvis_data.test_nvfis(s, url)
    do_message_(r_message)

    # Adding print statements for sanity check, delete later for production
    print ""
    print "Images result: {}".format(r_imgs)
    print ""

    # ACI metric calls
    aci_app_health = aci_data.get_overall_app_health(session)
    do_message_(aci_app_health)
    aci_egress_data = aci_data.get_egress_app_data(session)
    do_message_(aci_egress_data)
    aci_ingress_data = aci_data.get_ingress_app_data(session)
    do_message_(aci_ingress_data)

    # Need ability to wait for response 'ack' from NFVis deployment. Add sleep for now.
    aci_post_health = aci_data.get_post_app_health(session)
    # time.sleep(3)
    do_message_(aci_post_health)

    # Creating generic functions for NFVIS
    print " verify vm image"
    nfvis_data.verify_vmimage_nvfis(s, url)
    print "image config"
    nfvis_data.get_image_config(s, url)
    print "verify port lan bridge"
    nfvis_data.verify_port_lan_bridge(s, url)
    print "networks"
    nfvis_data.verify_networks(s, url)
    print "asa deployment"
    nfvis_data.verify_asa_deployment(s, url)

    #Create NFVIS stuff
    # nfvis_data.reg_vmimage_nvfis(s, url)
    nfvis_data.create_new_bridge(s, url, new_bridge)
