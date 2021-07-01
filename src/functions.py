import random
import string
import src.ngrok as ngrok
import src.sql as sql
import shutil
import os 
import requests

currentKey = ""
port = sql.getSetting("appPort")
urlHead = sql.getSetting("appIp")+":"+port

publicAdress = ngrok.getPublicAdress()

def deleteKey(key):
    if key != "" and key != None and key:
        sql.keyDelete(key)
        if os.path.isdir(os.getcwd()+"/uploads/"+key):            
            shutil.rmtree(os.getcwd()+"/uploads/"+key)
            print("dosya silindi")

def getQR():
    randomKey = generateKey()
    global currentKey
    currentKey = str(randomKey)
    print("url reloaded, new url is: "+urlHead+"/"+str(randomKey))    
    endUrl = publicAdress+"/"+str(currentKey)
    qr = "https://api.qrserver.com/v1/create-qr-code/?size=150x150&data="+str(endUrl)
    return qr

def createLink():
    randomKey = generateKey()
    url = publicAdress+"/"+str(randomKey)
    link = shortLink(url)
    sql.addlink(link,randomKey)

def generateKey():
    letters = string.ascii_lowercase+string.ascii_uppercase+string.digits
    randomKey = ''.join(random.choice(letters) for i in range(10))
    return randomKey

def getAllowedFilesArray():
    allowed_extensions = eval(sql.getSetting("allowedFiles"))
    return allowed_extensions

def shortLink(longUrl):
    url= "https://api-ssl.bitly.com/v4/shorten"
    authtoken = sql.getSetting("bitlyToken")
    hed = {'Authorization': 'Bearer ' + authtoken ,'Content-Type':'application/json'}
    data = {"long_url": longUrl}
    response = requests.post(url, json=data, headers=hed)
    return response.json()["link"]

def allowed_file(filename):
    return '.' in filename and "."+str(filename.split('.', 1)[1].lower()) in getAllowedFilesArray()

def getGoogleDoc(downloadUrl):
    stri = "https://docs.google.com/gview?url="+downloadUrl
    return(stri)

def filesArray():
    keys = sql.getKeys()
    keylist = []
    for key in keys:
        newkey = list(key)
        filesar = list(sql.getFiles(key[1]))
        note = sql.getNote(key[1])
        newkey.append(note)
        newfiles = []
        for file in filesar:
            newfile = list(file)
            downurl = publicAdress+"/"+str(key[1])+"/download/"+str(file[2])
            if str(file[2]).endswith((".doc",".docx","ppt","pptx","xls","xlsx")):          
                googUrl = getGoogleDoc(downurl)
                newfile.append(googUrl)
            else:
                newfile.append(downurl)

            if str(newfile[4]) == "" or str(newfile[4]) == None or not str(newfile[4]):
                newfile[4] = "Tümü"

            newfiles.append(newfile)

        newkey.append(newfiles)        
        keylist.append(newkey)
    print(list(reversed(keylist)))
    return list(reversed(keylist))

def saveSettingsPage(request):
    domain = request.form.get("domain")
    useNgrok = request.form.get("useNgrok")
    userName = request.form.get("userName")
    userPassword = request.form.get("userPassword")
    maxCopy = request.form.get("maxCopy")
    refresh_delay = request.form.get("refreshDelay")
    appPort = request.form.get("appPort")
    appIp = request.form.get("appIp")
    bitlyToken = request.form.get("bitlyToken")

    alwexs = []
    if request.form.get("check_pdf") == 'on':
        alwexs.append(".pdf")
    
    for field in request.form:
        if field.startswith("check_"):
            ar = field.split("_")
            ext = str("."+ar[1])
            if request.form.get(field) == 'on':
                alwexs.append(ext)

    strexs = str(alwexs).replace("'",'"')
    sql.addSettings("allowedFiles",strexs)                
    
    if userName:
        sql.addSettings("adminName",userName)                
    if userPassword:
        sql.addSettings("adminPass",userPassword)
    if maxCopy:
        sql.addSettings("maxCopy",maxCopy)
    if refresh_delay:
        sql.addSettings("refreshDelay",refresh_delay)
    if appPort:                    
        sql.addSettings("appPort",appPort)
    if appIp:
        sql.addSettings("appIp",appIp)
    if domain:
        sql.addSettings("domain",domain)                
    if bitlyToken:
        sql.addSettings("bitlyToken",bitlyToken)

    if useNgrok == 'on':
        sql.addSettings("useNgrok",'true')
    elif useNgrok == 'off':
        sql.addSettings("useNgrok",'false')

def getLinksArray():
    links = sql.getlinks()
    ar = []
    for link in links:
        key = link[2]
        ar.append(key)
    return ar
