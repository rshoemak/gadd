

import json

tt = "Ben-Ten1"
ttt = "MOON"


def get_overall_app_health(session):
    # Get Application overall health score
    uu = session.get("/api/node/mo/uni/tn-" + tt + "/ap-BM/health.json")
    page = json.loads(uu.content)
    app_healthscore = page["imdata"][0]["healthInst"]['attributes']['twScore']
    mess_app_healthscore = "ACI - Gadd Application overall health: {}".format(app_healthscore)
    return mess_app_healthscore


def get_egress_app_data(session):
    egd = session.get("/api/node/mo/uni/tn-" + tt + "/ap-BM/HDl2EgrBytesAg15min-0.json")
    page = json.loads(egd.content)
    app_egress_mdata = page['imdata'][0]['l2EgrBytesAgHist15min']['attributes']['multicastCum']
    app_egress_unidata = page['imdata'][0]['l2EgrBytesAgHist15min']['attributes']['unicastCum']
    mess_app_egress_data = "ACI - Egress multicast/unicast: {} / {}".format(app_egress_mdata, app_egress_unidata)
    return mess_app_egress_data


def get_ingress_app_data(session):
    ingd = session.get("/api/node/mo/uni/tn-" + tt + "/ap-BM/HDl2IngrBytesAg15min-0.json")
    page = json.loads(ingd.content)
    app_ingress_mdata = page['imdata'][0]['l2IngrBytesAgHist15min']['attributes']['multicastCum']
    app_ingress_unidata = page['imdata'][0]['l2IngrBytesAgHist15min']['attributes']['unicastCum']
    mess_app_ingress_data = "ACI - Ingress multicast/unicast: {} / {}".format(app_ingress_mdata, app_ingress_unidata)
    return mess_app_ingress_data


def get_post_app_health(session):
    # Get Application post nvfis deployment health score
    uuu = session.get("/api/node/mo/uni/tn-" + ttt + "/ap-3Tier_App/health.json")
    page = json.loads(uuu.content)
    post_app_healthscore = page["imdata"][0]["healthInst"]['attributes']['twScore']
    mess_post_app_healthscore = "ACI - Gadd Application health after FW deployment: {}".format(post_app_healthscore)
    return mess_post_app_healthscore
