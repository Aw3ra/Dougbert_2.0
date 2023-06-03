import http.client




def login_to_twitter(email, password, key):
    conn = http.client.HTTPSConnection("twttrapi.p.rapidapi.com")
    payload = f"username_or_email={email}&password={password}"

    headers = {
        'content-type': "application/x-www-form-urlencoded",
        'X-RapidAPI-Key': key,
        'X-RapidAPI-Host': "twttrapi.p.rapidapi.com"
    }

    conn.request("POST", "/login-email-username", payload, headers)

    res = conn.getresponse()
    data = res.read()

    print(data.decode("utf-8"))