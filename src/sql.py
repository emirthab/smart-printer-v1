import sqlite3 as sql
import datetime

db = sql.connect("printer.db",check_same_thread=False)
cur = db.cursor()


def defaultControl():
    tablefiles = """CREATE TABLE if not exists 'files' ('id', 'key', 'fileName', 'copy', 'pages', 'pageradio')"""
    tablesettings = """CREATE TABLE if not exists 'settings' ('variable', 'value')"""
    tablekeys = """CREATE TABLE if not exists 'keys' ('id', 'key', 'time')"""
    tablenotes = """CREATE TABLE if not exists 'notes' ('id', 'key', 'note')"""
    tablelinks = """CREATE TABLE if not exists 'links' ('id', 'link','key', 'time')"""

    sqlunique = "CREATE UNIQUE INDEX if not exists idx_settings ON settings (variable);"
    sqlunique2 = "CREATE UNIQUE INDEX if not exists idx_files ON files (id);"
    sqlunique3 = "CREATE UNIQUE INDEX if not exists idx_keys ON keys (id);"
    sqlunique4 = "CREATE UNIQUE INDEX if not exists idx_notes ON notes (id);"
    sqlunique5 = "CREATE UNIQUE INDEX if not exists idx_links ON links (id);"

    adminname = "INSERT OR IGNORE INTO settings (variable,value) VALUES('adminName','admin');"
    adminpass = "INSERT OR IGNORE INTO settings (variable,value) VALUES('adminPass','admin');"
    appip = "INSERT OR IGNORE INTO settings (variable,value) VALUES('appIp','127.0.0.1');"
    appport = "INSERT OR IGNORE INTO settings (variable,value) VALUES('appPort','8080');"
    usengrok = "INSERT OR IGNORE INTO settings (variable,value) VALUES('useNgrok','true');"
    domain = "INSERT OR IGNORE INTO settings (variable,value) VALUES('domain','www.example.com');"
    allowedfiles = """INSERT OR IGNORE INTO settings (variable,value) VALUES('allowedFiles','[".pdf",".doc",".docx",".xls",".xlsx",".ppt",".pptx",".txt",".jpg",".jpeg",".png"]');"""
    maxcopy = "INSERT OR IGNORE INTO settings (variable,value) VALUES('maxCopy','20');"
    logoid = "INSERT OR IGNORE INTO settings (variable,value) VALUES('logoid','0');"
    refreshdelay = "INSERT OR IGNORE INTO settings (variable,value) VALUES('refreshDelay','10');"
    bitlytoken = "INSERT OR IGNORE INTO settings (variable,value) VALUES('bitlyToken','');"
    
    cur.execute(tablefiles)
    cur.execute(tablesettings)
    cur.execute(tablekeys)
    cur.execute(tablenotes)
    cur.execute(tablelinks)

    cur.execute(sqlunique2)
    cur.execute(sqlunique)
    cur.execute(sqlunique3)
    cur.execute(sqlunique4)
    cur.execute(sqlunique5)

    cur.execute(adminname)
    cur.execute(adminpass)
    cur.execute(appip)
    cur.execute(appport)
    cur.execute(usengrok)
    cur.execute(domain)
    cur.execute(allowedfiles)
    cur.execute(logoid)
    cur.execute(maxcopy)
    cur.execute(refreshdelay)
    cur.execute(bitlytoken)

    db.commit()

def getFiles(key):
    sql = "SELECT * FROM files WHERE key = '"+key+"'"
    cur.execute(sql)
    return(cur.fetchall())

def keyIsExists(key):
    sql = "SELECT key FROM keys WHERE key = '"+key+"'"
    cur.execute(sql)
    res = cur.fetchall()
    if  len(list(res)) == 0:
        return False
    else:
        return True

def getNote(key):
    sql = "SELECT note FROM notes WHERE key = '"+key+"'"
    cur.execute(sql)
    result = cur.fetchall()
    if len(result) != 0:
        result = result[0][0]
    else:
        result = ""
    return result

def getNotes():
    sql = "SELECT * FROM notes "
    cur.execute(sql)
    return(cur.fetchall())

def addNote(key,note):
    if keyIsExists(key):
        sqlid = "SELECT MAX(CAST(id AS INT )) FROM notes;"
        cur.execute(sqlid)
        _id = cur.fetchall()[0][0]
        if _id == None:
            _id = 0
        add = "INSERT INTO notes VALUES ('"+str(int(_id)+1)+"', '"+key+"', '"+note+"')"
        cur.execute(add)
        db.commit()
    else:
        print("key is not exist")

def addKey(key):
    if keyIsExists(key) == False:
        e = datetime.datetime.now()
        date = "%s/%s/%s" % (e.day, e.month, e.year)
        time = "%s:%s:%s" % (e.hour, e.minute, e.second)
        fulldate = date+" - "+time
        sqlid = "SELECT MAX(CAST(id AS INT )) FROM keys;"
        cur.execute(sqlid)
        _id = cur.fetchall()[0][0]
        if _id == None:
            _id = 0
        add = "INSERT OR IGNORE INTO keys VALUES ('"+str(int(_id)+1)+"', '"+key+"', '"+fulldate+"')"
        cur.execute(add)
        db.commit()
    else:
        print("key is already defined")

def addFile(key,fileName,copy,pages,pageradio):
    if keyIsExists(key):
        sqlid = "SELECT MAX(CAST(id AS INT )) FROM files;"
        cur.execute(sqlid)
        _id = cur.fetchall()[0][0]
        if _id == None:
            _id = 0
        add = "INSERT INTO files VALUES ('"+str(int(_id)+1)+"', '"+key+"', '"+fileName+"', '"+copy+"','"+pages+"','"+pageradio+"')"
        cur.execute(add)
        db.commit()
    else:
        print("key is not exist")

def getlinks():
    sql = "SELECT * FROM links"
    cur.execute(sql)
    return(cur.fetchall())

def removeLink(key):
    sql = "DELETE FROM links WHERE key = '"+key+"'"
    cur.execute(sql)
    db.commit()

def addlink(link,key):
    e = datetime.datetime.now()
    date = "%s/%s/%s" % (e.day, e.month, e.year)
    time = "%s:%s:%s" % (e.hour, e.minute, e.second)
    fulldate = date+" - "+time
    sqlid = "SELECT MAX(CAST(id AS INT )) FROM links;"
    cur.execute(sqlid)
    _id = cur.fetchall()[0][0]
    if _id == None:
        _id = 0
    sql = "INSERT INTO links (id,link,key,time) VALUES('"+str(int(_id)+1)+"','"+link+"','"+key+"','"+fulldate+"');"
    cur.execute(sql)
    db.commit()

def addSettings(variable,value):
    sql = "INSERT OR REPLACE INTO settings (variable,value) VALUES('"+variable+"','"+value+"');"
    cur.execute(sql)
    db.commit()

def getSetting(variable):
    sql = "SELECT value FROM settings WHERE variable = '"+variable+"'"
    cur.execute(sql)
    return(cur.fetchall()[0][0])

def getKeys():
    sql = "SELECT * FROM keys"
    cur.execute(sql)
    return(cur.fetchall())

def keyDelete(key):
    sql = "DELETE FROM keys WHERE key = '"+key+"'"
    cur.execute(sql)
    sql = "DELETE FROM files WHERE key = '"+key+"'"
    cur.execute(sql)
    sql = "DELETE FROM notes WHERE key = '"+key+"'"
    cur.execute(sql)
    db.commit()


defaultControl()