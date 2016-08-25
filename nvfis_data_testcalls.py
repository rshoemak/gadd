
import requests
import sys
# import json
import creds
# import staticvars
import events
import sparky
import acitoolkit.acitoolkit as aci
import aci_data
#import nfvis_data
# import time
import nfvis_data_testfunctions
import message_board





# Main Program

# Message Board
#nfv_created_lanbridge = "\nNFV created Lan Bridge"
#nfv_assigned_port_lanbrdige = "\nNFV assigned port to Lan Bridge"


new_bridge = "svc-gadd-br"
img = "asav941-203"
device = "1471415647"

def do_message_(mess):
    sparky.send_alert(alert_room_id, mess)
    return


if __name__ == '__main__':
    trigger = events.trigger_event()

    # basic credential setup for NFVis device
    url, login, password = creds.nvfis_getgcred()
    s = requests.Session()
    s.auth = (login, password)
    s.headers = ({'Content-type': 'application/vnd.yang.data+json', 'Accept': 'application/vnd.yang.data+json'})
    s.verify = False

    # Create room if not already created.
    # Add in additional members manually. To do - add in automatically
    #alert_room_id = sparky.setup_room()

    # Test NFVis login functionality
    #r_imgs, r_message = nfvis_data.test_nvfis(s, url)
    #do_message_(r_message)

    # Adding print statements for sanity check, delete later for production
    #print ""
    #print "Images result: {}".format(r_imgs)
    #print ""

    # Creating generic functions for NFVIS
    #nfvis_data.reg_vmimage_nvfis(s, url)

    print " verify vm image"
    #nfvis_data_testfunctions.nfv_register_vm_img(s, url, img)

    #nfvis_data_testfunctions.nfv_verify_vm_img(s, url, img, deep_key=False)

    #nfvis_data_testfunctions.nfv_assign_port_lanbridge(s, url, new_bridge)

    #nfvis_data_testfunctions.nfv_verify_lanbridge(s, url, deep_key=False)

    #nfvis_data_testfunctions.nfv_verify_networks(s, url, deep_key=False)

    #nfvis_data_testfunctions.nfv_verify_asa_deployment(s, url, device, deep_key=False)
    print 150 * "#"
    #nfvis_data_testfunctions.nfv_prune_name(s, url)
    print 150 * "#"
    #nfvis_data_testfunctions.nfv_get_config_info(s, url)
    nfvis_data_testfunctions.nfv_test_filejson_payload(s, url)

    #do_message_(message_board.nfv_assigned_port_lanbrdige)
    #do_message_(message_board.nfv_created_lanbridge)




    #print "image config"
    #nfvis_data.get_image_config(s, url)
    #print "verify port lan bridge"
    #nfvis_data.verify_port_lan_bridge(s, url)
    #print "networks"
    #nfvis_data.verify_networks(s, url)
    #print "asa deployment"
    #nfvis_data.verify_asa_deployment(s, url)

    #nfvis_data.create_new_bridge(s, url, new_bridge)

    print "Testing nested stuff\n"
    #nfvis_data_testfunctions.testing_nested_dict()

    #nfvis_data_testfunctions.nfv_get_name_id(s, url)




