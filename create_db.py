import os
import db_api

def create_table(dbstring):

    sql = """CREATE TABLE `batch_mgmt` (
      `fid` int(11) NOT NULL AUTO_INCREMENT,
      `url` text,
      `uploaded_file_size` text,
      `downloaded_file_size` text,
      `process_time` datetime DEFAULT NULL,
      `user_ip` text,
      `end_time` datetime DEFAULT NULL,
      PRIMARY KEY (`fid`)
    )"""
    
    conn, curr = db_api.get_connection(dbstring)
    curr.execute(sql)
    conn.commit()
    curr.close()
    conn.close()
    return
    
def create_db(dbstring):

    ip, usr, pswd, dbname = dbstring.split('#')
    sql = "create database %s"%dbname
    conn, curr = db_api.get_nodb_connection("%s#%s#%s"%(ip, usr, pswd))
    curr.execute(sql)
    conn.commit()
    curr.close()
    conn.close()
    return

def main():

    basepath = os.path.dirname(os.path.realpath(__file__))
    config_path =  os.path.join(basepath, "config.ini")
    dbstring = db_api.generate_dbstring(config_path)
    create_db(dbstring)
    create_table(dbstring) 


if __name__ == '__main__':
    main()


