from pyngrok import ngrok
import time
import requests
import json
import os
import src.sql as sql

def getPublicAdress():
    ngrok.set_auth_token("1QqOxkpRRnI3Az72Pp0KdtDqeLw_5nZ8zn187XqPL6BjzYmT8")
    ssh_tunnel_https = ngrok.connect(sql.getSetting("appPort"), "http",bind_tls=True)
    time.sleep(4)
    url = "http://127.0.0.1:4040/api/tunnels"
    content = requests.get(url).text
    data = json.loads(content)["tunnels"]
    ar = data[0]
    url = ar["public_url"]
    return url

