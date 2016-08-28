
import sys
import json
import creds
import acitoolkit.acitoolkit as aci


# Main Program
ttt = "MOON"


def get_post_app_health(session):
    # Get Application post nvfis deployment health score
    uuu = session.get("/api/node/mo/uni/tn-" + ttt + "/ap-3Tier_App/health.json")
    page = json.loads(uuu.content)
    post_app_healthscore = page["imdata"][0]["healthInst"]['attributes']['twScore']
    return post_app_healthscore


if __name__ == '__main__':

    # log into APIC
    a_url, a_login, a_password = creds.apic_GetArgs()
    session = aci.Session(a_url, a_login, a_password)
    session.verify_ssl = False
    a_resp = session.login()
    if not a_resp.ok:
        print "%% Could not login to APIC"
        sys.exit(0)

    # Need ability to wait for response 'ack' from NFVis deployment. Add sleep for now.
    print get_post_app_health(session)
