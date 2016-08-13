import creds
import requests
import json

# Spark room notifications

spark_host = "https://api.ciscospark.com"
spark_api = "https://api.ciscospark.com/v1/messages"
token = creds.spark_GetArgs()
team_email = "rshoemak@cisco.com"
spark_headers = {'Content-type': 'application/json', 'Authorization': token}

# Spark rooms setup
def setup_room():
    room_items = current_rooms()

# Look for a room called "Alert Room"
    alert_room_id = ""
    for room in room_items:
        if room["title"] == "Gadd Alert Room":
            alert_room_id = room["id"]
            return alert_room_id

# If alert room not found, create it
    if alert_room_id == "":
        alert_room = create_alert_room()
        alert_room_id = alert_room["id"]
    return alert_room_id


def create_alert_room():
    spark_r = spark_host + "/v1/rooms"
    spark_body = {"title": "Gadd Alert Room"}
    page = requests.post(spark_r, headers=spark_headers, json=spark_body)
    room = page.json()
    return room


def current_rooms():
    spark_r = spark_host + "/v1/rooms"
    page = requests.get(spark_r, headers=spark_headers)
    rooms = page.json()
    return rooms["items"]


# Team members to the Alert Room
def add_email_alert_room(email, alert_room_id):
    member = get_membership_for_room(alert_room_id)
    personEmail_id = ""

    for k, v in member[0].items():
        if k == 'personEmail':
            personEmail_id = v

    if personEmail_id != email:
        spark_r = spark_host + "/v1/memberships"
        spark_body = {"personEmail": email, "roomId": alert_room_id}
        page = requests.post(spark_r, headers=spark_headers, json=spark_body)
        membership = page.json()
        return membership
    else:
        return


def get_membership_for_room(alert_room_id):
    spark_r = spark_host + "/v1/memberships?roomId=%s" % (alert_room_id)
    page = requests.get(spark_r, headers=spark_headers)
    memberships = page.json()["items"]
    return memberships


# Send message to Alert Room
def send_alert(alert_room_id, message):
    headers = {'Content-type': 'application/json', 'Authorization': token}
    data = {'roomId': alert_room_id, 'text': message}
    requests.post(spark_api, headers=headers, data=json.dumps(data))
