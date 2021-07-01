from flask import Flask, render_template, request, send_from_directory
from flask.templating import render_template_string
import requests
from werkzeug.utils import redirect, secure_filename
import os
from flask import Blueprint
import src.functions as func
import src.sql as sql

listener = Blueprint("listener",__name__,template_folder='templates')

memoryKeys = []

publicAdress = func.publicAdress

@listener.route('/<key>/download/<path:filename>', methods=['GET', 'POST'])
def download(key,filename):
    return send_from_directory(directory=os.getcwd()+"/uploads/"+key, filename=filename)

@listener.route("/", methods=['GET', 'POST'])
def index():
    name = request.args.get("name")
    password = request.args.get("pass")
    page = request.args.get("page")
    removekey = request.args.get("removekey")
    removelink = request.args.get("removelink")

    if name == sql.getSetting("adminName") and password == sql.getSetting("adminPass"):

        url = "?name="+name+"&pass="+password
        if page == None or page == "":
            filesarray = func.filesArray()
            if removekey == None or removekey == "":                
                return render_template("dashboard.html",url=url,filesar = filesarray,logoid=sql.getSetting("logoid"))
            else:
                func.deleteKey(removekey)
                return redirect("/?name="+sql.getSetting("adminName")+"&pass="+sql.getSetting("adminPass"),code=302)

        elif page == "qrcode":
            refreshDelay = '''
                {% extends "qrcode.html" %}
                {% block refreshDelay %}
                <meta http-equiv="refresh" name="refresh" content="'''+sql.getSetting("refreshDelay")+'''"/>
                {% endblock %}
                '''
            
            return render_template_string(refreshDelay,url=url,page="qrcode",qrcode=str(func.getQR()),logoid=sql.getSetting("logoid"))

        elif page == "settings":
            if request.method == "GET":
                checkngrok = False

                if sql.getSetting("useNgrok") == 'true':
                    checkngrok = True
                else:
                    checkngrok = False

                return render_template("settings.html",url=url,placeMaxcopy=sql.getSetting("maxCopy"),
                placeRefresh=sql.getSetting("refreshDelay"),placePort=sql.getSetting("appPort"),placeIp=sql.getSetting("appIp"),
                placeUsername=sql.getSetting("adminName"),placeDomain=sql.getSetting("domain"),allowedFilesArray=func.getAllowedFilesArray(),
                checkUseNgrok=checkngrok,logoid=sql.getSetting("logoid"),placeBitlyToken=sql.getSetting("bitlyToken")
                )

            elif request.method == "POST":
                companyLogo = request.files.get("company-logo")
                if companyLogo:
                    logoid = sql.getSetting("logoid")
                    sql.addSettings("logoid",str(int(logoid)+1))
                    print("logoid: "+str(int(logoid)+1))
                    companyLogo.save(os.getcwd()+"/static/img/company-logo-"+str(int(logoid)+1)+".png")

                func.saveSettingsPage(request)                                                    

                return redirect("/?name="+sql.getSetting("adminName")+"&pass="+sql.getSetting("adminPass")+"&page=settings",code=302)
        
        elif page == "links":
            if removelink == None or removelink == "":
                _links = list(reversed(sql.getlinks()))
                return render_template("links.html",url=url,logoid=sql.getSetting("logoid"),links=_links)
            else:
                sql.removeLink(removelink)
                return redirect("/?name="+sql.getSetting("adminName")+"&pass="+sql.getSetting("adminPass")+"&page=links",code=302)

        elif page == "createlink":
            func.createLink()            
            return redirect("/?name="+sql.getSetting("adminName")+"&pass="+sql.getSetting("adminPass")+"&page=links",code=302)

        elif page == "reports":
            pass

    elif name is not set and password is not set:
        return render_template("login.html",logoid=sql.getSetting("logoid"))
    else:
        return render_template("404.html")

@listener.route("/<key>")
def uploadIndex(key):
    if key == func.currentKey or key in memoryKeys or key in func.getLinksArray():

        if key not in memoryKeys:
            memoryKeys.append(key)

        return render_template("upload.html",url=str(publicAdress+"/uploadfile/"+key),logoid=sql.getSetting("logoid"))
    else:
        return render_template('404.html')

@listener.route("/uploadfile/<key>", methods = ["GET", "POST"])
def uploadFile(key):
    if request.method == "POST" and key in memoryKeys:

        if os.path.isdir("uploads/"+str(key)) == False:
            os.mkdir("uploads/"+str(key))

        files = request.files.getlist("files[]")
        data = []
        for file in files:
            if file and func.allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save("uploads/"+key+"/"+filename)
                data.append(filename)
            else:
                return render_template("404.html")
        
        return render_template("print.html",data=data,url=str(publicAdress+"/printfile/"+key),dataLen=len(data),maxCopy=sql.getSetting("maxCopy"))
    else:
        return render_template("404.html")

@listener.route("/printfile/<key>", methods = ["GET", "POST"])
def printFile(key):
    if request.method == "POST" and key in memoryKeys:
        sql.addKey(key)
        dataLenght = request.form.get("itemsLen")

        for i in range(int(dataLenght)):
            fileName = request.form.get("itemName_"+str(i+1))
            copy = request.form.get("rangeInput_"+str(i+1))
            extraNote = request.form.get("extraNote")

            if fileName.endswith((".pdf",".doc",".docx")):
                pages = request.form.get("input_pages_"+str(i+1))
                pageRadio = request.form.get("radios_"+str(i+1))
            else:
                pages = ""
                pageRadio = ""

            sql.addNote(key,extraNote)
            sql.addFile(key,fileName,copy,pages,pageRadio)    

        if key in func.getLinksArray():
            sql.removeLink(key)
        if key in memoryKeys:
            memoryKeys.remove(key)

        return render_template("success.html")
        
    else:
        return render_template("404.html")