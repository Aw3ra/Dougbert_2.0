import requests



def send_dm(message, session, key, to_user_name=None, to_user_id=None, media_id=None):
    url = "https://twttrapi.p.rapidapi.com/send-dm"

    payload = {
        "message": message,
        "to_user_name": to_user_name,
        "to_user_id": to_user_id,
        "media_id": media_id
    }
    headers = {
        "content-type": "application/x-www-form-urlencoded",
        "twttr-session": session,
        "X-RapidAPI-Key": key,
        "X-RapidAPI-Host": "twttrapi.p.rapidapi.com"
    }

    return requests.post(url, data=payload, headers=headers)