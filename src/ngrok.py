from pyngrok import ngrok
import time
import requests
import json
import src.sql as sql

if sql.getSetting("useNgrok") == "true":
    ssh_tunnel_https = ngrok.connect(sql.getSetting("appPort"), "http",bind_tls=True)

def getPublicAdress():
    if sql.getSetting("useNgrok") == "true":
        url = "http://127.0.0.1:4040/api/tunnels"
        content = requests.get(url).text
        data = json.loads(content)["tunnels"]
        ar = data[0]
        url = ar["public_url"]
        return url
    else:
        url = sql.getSetting("domain")
        return url

