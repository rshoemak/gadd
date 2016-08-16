
import requests
import sys
import json
import creds
# import staticvars
import events
import sparky
import acitoolkit.acitoolkit as aci
import aci_data
import nfvis_data


# Main Program
'''
# Test login functionality - get images
def test_nvfis(ss):
    message = "Logged into NFVis and looking at images"
    u = url + "/api/config/esc_datamodel/images"
    page = ss.get(u)
    img = json.loads(page.content)
    do_message_(message)
    return img
    # stuff to work with parsing
    # resp = img['images']['image']
    # resp = page.json()
    # return resp
    # resp = page.content  #open format print out for reference
'''

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
