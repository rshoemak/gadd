
import sys
import json
import creds
import acitoolkit.acitoolkit as aci


# Main Program
tt = "Ben-Ten1"


def get_overall_app_health(session):
    # Get Application overall health score
    uu = session.get("/api/node/mo/uni/tn-" + tt + "/ap-BM/health.json")
    page = json.loads(uu.content)
    app_healthscore = page["imdata"][0]["healthInst"]['attributes']['twScore']
    return app_healthscore


if __name__ == '__main__':

    # log into APIC
    a_url, a_login, a_password = creds.apic_GetArgs()
    session = aci.Session(a_url, a_login, a_password)
    session.verify_ssl = False
    a_resp = session.login()
    if not a_resp.ok:
        print "%% Could not login to APIC"
        sys.exit(0)

    # ACI metric calls
    print get_overall_app_health(session)
