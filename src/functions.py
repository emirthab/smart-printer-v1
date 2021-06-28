import threading
import time
import random
import string
import src.ngrok as ngrok
import src.sql as sql

Keys = []
currentKey = ""
port = sql.getSetting("appPort")
urlHead = sql.getSetting("appIp")+":"+port

publicAdress = ngrok.getPublicAdress()

def getQR():
    endUrl = publicAdress+"/"+str(currentKey)
    qr = "https://api.qrserver.com/v1/create-qr-code/?size=150x150&data="+str(endUrl)
    print(qr)
    return qr

def getKey():
    letters = string.ascii_lowercase
    randomKey = ''.join(random.choice(letters) for i in range(10))
    data = randomKey
    global currentKey
    currentKey = str(randomKey)
    return data

def generateKey():
    while 1:
        key = getKey()
        Keys.append(key)
        print("url reloaded, new url is: "+urlHead+"/"+str(key))
        time.sleep(15)

allowed_extensions = ['txt', 'pdf', 'png', 'jpg', 'jpeg', 'doc', 'docx', 'ppt', 'pptx', 'xls', 'xlsx']

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed_extensions

def getGoogleDoc(downloadUrl):
    str = "https://docs.google.com/gview?url="+downloadUrl

threading.Thread(target=generateKey).start()