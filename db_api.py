import ast, re, time, os, json, sys
import MySQLdb
import uuid
import urllib
import datetime
import ConfigParser


def get_connection(data):

    khost, kuser , kpasswd , kdb = data.split('#')
    conn = MySQLdb.connect(khost, kuser, kpasswd, kdb, charset="utf8")
    cur = conn.cursor()
    return conn, cur

def get_nodb_connection(data):

    khost, kuser , kpasswd = data.split('#')
    conn = MySQLdb.connect(khost, kuser, kpasswd)
    cur = conn.cursor()
    return conn, cur

def get_file_status(fid, dbstring):

    conn, curr = get_connection(dbstring)
    sql = 'select * from batch_mgmt where fid=%s'
    curr.execute(sql%fid)
    data = curr.fetchone()
    curr.close()
    conn.close()
    return data

def update_batch_mgmt(cnt, dbstring, fid):

    conn, curr = get_connection(dbstring)
    end_time = str(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    sql = 'update batch_mgmt set downloaded_file_size = "%s", end_time="%s" where fid=%s'
    curr.execute(sql%(str(cnt), end_time, fid))
    conn.commit()
    curr.close()
    conn.close()
    return

def insert_into_file_mgmt(url, content_length, dbstring, user_ip):

    conn, curr = get_connection(dbstring)
    url = urllib.quote(url)
    process_time = str(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    isql = 'insert into batch_mgmt (url, uploaded_file_size, downloaded_file_size, process_time, user_ip) values ("%s", "%s", "%s", "%s", "%s")'
    curr.execute(isql%(url, str(content_length), "0", process_time, str(user_ip)))
    conn.commit()
    fsql = 'select fid from batch_mgmt where url="%s" and uploaded_file_size="%s" and process_time="%s" and user_ip="%s"'
    curr.execute(fsql%(url, str(content_length), process_time, str(user_ip)))
    fid = curr.fetchone()
    curr.close()
    conn.close()
    if not fid: return -1
    return fid[0]


def generate_dbstring(config_path):

    config = ConfigParser.ConfigParser()
    config.read(config_path)
    db_ip = config.get('database', 'ip')
    db_user = config.get('database', 'user')
    db_pswd = config.get('database', 'password')
    db_name = config.get('database', 'dbname')
    return '%s#%s#%s#%s'%(db_ip, db_user, db_pswd, db_name)

