from flask import Flask, render_template, request, send_from_directory, current_app
from werkzeug.utils import secure_filename
import os
from flask import Blueprint
import src.functions as func
import src.sql as sql

listener = Blueprint("listener",__name__)

publicAdress = func.publicAdress
adminName = sql.getSetting("adminName")
adminPass = sql.getSetting("adminPass")

@listener.route('/<key>/download/<path:filename>', methods=['GET', 'POST'])
def download(key,filename):
    return send_from_directory(directory=os.getcwd()+"/uploads/"+key, filename=filename)

@listener.route("/")
def index():
    name = request.args.get("name")
    password = request.args.get("pass")
    page = request.args.get("page")
    if name == adminName and password == adminPass:
        if page is not set:
            return render_template("admin.html")
        if page == "qrcode":
            return render_template("qrcode.html", qrcode=str(func.getQR()))
    elif name is not set and password is not set:
        return render_template("index.html")
    else:
        return render_template("404.html")

@listener.route("/<key>")
def uploadIndex(key):
    if key in func.Keys:
	    return render_template("upload.html",url=str(publicAdress+"/uploadfile/"+key))
    else:
        return render_template('404.html')

@listener.route("/uploadfile/<key>", methods = ["GET", "POST"])
def uploadFile(key):
    if request.method == "POST" and key in func.Keys:

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
        
        return render_template("print.html",data=data,url=str(publicAdress+"/printfile/"+key),dataLen=len(data))
    else:
        return render_template("404.html")

@listener.route("/printfile/<key>", methods = ["GET", "POST"])
def printFile(key):
    if request.method == "POST" and key in func.Keys:
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

            sql.addFile(key,fileName,copy,pages,pageRadio)    

        return render_template("success.html")
        
    else:
        return render_template("404.html")