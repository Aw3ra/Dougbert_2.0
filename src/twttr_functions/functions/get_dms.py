import http.client
import json

conn = http.client.HTTPSConnection("twttrapi.p.rapidapi.com")


def get_dms(session, rapid_api_key):
    headers = {
        'twttr-session': session,
        'x-rapidapi-key': rapid_api_key,
        'x-rapidapi-host': "twttrapi.p.rapidapi.com"
    }
    conn.request("GET", "/get-dm-conversations", headers=headers)

    res = conn.getresponse()
    data = res.read()
    json_data = json.loads(data)
    if len(json_data) == 0: return []
    DMs = json_data['inbox_initial_state']['conversations']
    for convo_id in DMs:
        convo = DMs[convo_id]
        status = convo['status']
        user = convo['participants'][0]['user_id']
        print(user, status, sep = '   |   ')
