import sqlite3 as sql
import datetime

db = sql.connect("printer.db")
cur = db.cursor()


def defaultControl():
    tablefiles = """CREATE TABLE if not exists 'files' ('id', 'key', 'fileName', 'copy', 'pages', 'pageradio')"""
    tablesettings = """CREATE TABLE if not exists 'settings' ('variable', 'value')"""
    tablekeys = """CREATE TABLE if not exists 'keys' ('id', 'key', 'time')"""
    tablenotes = """CREATE TABLE if not exists 'notes' ('id', 'key', 'note')"""

    sqlunique = "CREATE UNIQUE INDEX if not exists idx_settings ON settings (variable);"
    sqlunique2 = "CREATE UNIQUE INDEX if not exists idx_files ON files (id);"
    sqlunique3 = "CREATE UNIQUE INDEX if not exists idx_keys ON keys (id);"
    sqlunique4 = "CREATE UNIQUE INDEX if not exists idx_notes ON notes (id);"

    adminname = "INSERT OR IGNORE INTO settings (variable,value) VALUES('adminName','admin');"
    adminpass = "INSERT OR IGNORE INTO settings (variable,value) VALUES('adminPass','admin');"
    appip = "INSERT OR IGNORE INTO settings (variable,value) VALUES('appIp','127.0.0.1');"
    appport = "INSERT OR IGNORE INTO settings (variable,value) VALUES('appPort','8080');"
    
    cur.execute(tablefiles)
    cur.execute(tablesettings)
    cur.execute(tablekeys)
    cur.execute(tablenotes)

    cur.execute(sqlunique)
    cur.execute(sqlunique2)
    cur.execute(sqlunique3)
    cur.execute(sqlunique4)

    cur.execute(adminname)
    cur.execute(adminpass)
    cur.execute(appip)
    cur.execute(appport)

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

def getKey(file):
    pass

def getNote(key):
    sql = "SELECT note FROM notes WHERE key = '"+key+"'"
    cur.execute(sql)
    return(cur.fetchall()[0][0])

def addNote(key,note):
    if keyIsExists(key):
        sqlid = "SELECT MAX(id) FROM notes"
        cur.execute(sqlid)
        id = cur.fetchall()[0][0]
        if id == None:
            id = 0
        add = "INSERT INTO notes VALUES ('"+str(int(id)+1)+"', '"+key+"', '"+note+"')"
        cur.execute(add)
        db.commit()
    else:
        print("key is not exist")

def addKey(key):
    if not keyIsExists(key):
        e = datetime.datetime.now()
        date = "%s/%s/%s" % (e.day, e.month, e.year)
        time = "%s:%s:%s" % (e.hour, e.minute, e.second)
        fulldate = date+" - "+time
        sqlid = "SELECT MAX(id) FROM keys"
        cur.execute(sqlid)
        id = cur.fetchall()[0][0]
        if id == None:
            id = 0
        add = "INSERT OR IGNORE INTO keys VALUES ('"+str(int(id)+1)+"', '"+key+"', '"+fulldate+"')"
        cur.execute(add)
        db.commit()
    else:
        print("key is already defined")

def addFile(key,fileName,copy,pages,pageradio):
    if keyIsExists(key):
        sqlid = "SELECT MAX(id) FROM files"
        cur.execute(sqlid)
        id = cur.fetchall()[0][0]
        if id == None:
            id = 0
        add = "INSERT INTO files VALUES ('"+str(int(id)+1)+"', '"+key+"', '"+fileName+"', '"+copy+"','"+pages+"','"+pageradio+"')"
        cur.execute(add)
        db.commit()
    else:
        print("key is not exist")

def addSettings(variable,value):
    sql = "INSERT OR REPLACE INTO settings (variable,value) VALUES('"+variable+"','"+value+"');"
    cur.execute(sql)
    db.commit()

def getSetting(variable):
    sql = "SELECT value FROM settings WHERE variable = '"+variable+"'"
    cur.execute(sql)
    return(cur.fetchall()[0][0])

defaultControl()