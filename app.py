from flask import Flask, jsonify, request
from flask_restful import Api, Resource
import threading
import os, re, time, datetime
import requests 
import db_api
import ConfigParser

app = Flask(__name__)
api = Api(app)


@app.route('/')
def index():

    html = open('index.txt').read()
    return html


class Download(Resource):

    def post(self):
        #If I am here, then the resouce Download was requested using the method POST

        #Step 1: Get posted data:
        postedData = request.get_json()
        #Steb 2: Verify validity of posted data
        status_code = 200
        if "url" not in postedData: status_code = 301 #Missing parameter

        if (status_code!=200):
            retJson = {
                "File ID": "",
                "Message": "An error happened",
                "Status Code":status_code
            }
            return jsonify(retJson)

        #If i am here, then status_code == 200
        url = postedData["url"]
        content_length = self.get_content_length(url)
        client_ip = request.environ['REMOTE_ADDR']#request.remote_addr
        basepath = os.path.dirname(os.path.realpath(__file__))
        config_path =  os.path.join(basepath, "config.ini")
        dbstring = db_api.generate_dbstring(config_path)
        fid = db_api.insert_into_file_mgmt(url, content_length, dbstring, client_ip)

        msg = "Success"
        if fid != -1:
            t1 = time.time()
            #Step 3: download file
            thread = threading.Thread(target=self.download_file_from_url, kwargs={'file_url': url, 'dbstring': dbstring, 'fid':fid})
            thread.start()
        else: 
            status_code = 500###Internal Server Error
            msg = "Internal Server Error"
        retMap = {
            'File ID': str(fid), #ID to keep a track of file
            'Message': msg,
            'Status Code': status_code
        }
        return jsonify(retMap)

    def get_filename_from_cd(self, cd):
        """
        Get filename from content-disposition
        """
        if not cd:
            return None
        fname = re.findall('filename=(.+)', cd)
        if len(fname) == 0:
            return None
        return fname[0]


    def get_content_length(self, file_url):
    
        ##Fetching content length from header
        h = requests.head(file_url, allow_redirects=True)
        header = h.headers
        content_length = header.get('content-length', None)
        return content_length

    def download_file_from_url(self, file_url, dbstring, fid):

        """
        Download file from URL
        """
        ##Creating download directory if not exists
        basedir = os.path.abspath(os.path.dirname(__file__))
        print basedir
        download_path = os.path.join(basedir, 'url_file_downloads/')
        if not os.path.exists(download_path): 
            try:os.makedirs(download_path)
            except:pass

        content_length = self.get_content_length(file_url)
        print 'START :::', content_length
        ##Reading URL data in streams
        r = requests.get(file_url, stream = True) 

        ##Fetching filename from headers, if not present then considering the last part of url as filename
        filename = self.get_filename_from_cd(r.headers.get('content-disposition'))
        if filename == None: filename = file_url.split('/')[-1]

        ##Writing URL contents into file in chunks of 1024 and keeping a track of downloaded data
        cnt = 0 
        with open(os.path.join(download_path, filename),"wb") as fw: 
            for chunk in r.iter_content(chunk_size=1024): 
                 if chunk:
                    cnt += len(chunk)
                    fw.write(chunk) 
                    db_api.update_batch_mgmt(cnt, dbstring, fid)
        print 'END :::', cnt
        return cnt


class Status(Resource):

    def get(self):
       
        #If I am here, then the resouce Status was requested using the method GET

        #Step 1: Get parameters present after status?{}:
        postedData = request.args

        #Steb 2: Verify validity of posted data
        status_code = 200
        if "id" not in postedData: status_code = 301 #Missing parameter

        if (status_code!=200):
            retJson = {
                "Message": "An error happened",
                "Status Code":status_code,
                "Data": {}
            }
            return jsonify(retJson)

        #If i am here, then status_code == 200
        file_id = postedData["id"]
        basepath = os.path.dirname(os.path.realpath(__file__))
        config_path =  os.path.join(basepath, "config.ini")
        dbstring = db_api.generate_dbstring(config_path)
        file_status = db_api.get_file_status(file_id, dbstring)
        rem_size = float(file_status[2]) - float(file_status[3])
        msg = 'File ID Not Exists'
        data_dict = {}
        if file_status: 
            msg = 'Success'
            data_dict = {'file_id': str(file_status[0]), 'url': file_status[1], 'upload size': file_status[2], 'downloaded': file_status[3], 'start time': file_status[4], 'user ip': file_status[5], 'end time': file_status[6], 'remaining size': str(rem_size)}
        #Step 3: fetch status of file id
        retMap = {
            'Message': msg,
            'Data': data_dict,
            'Status Code': 200
        }
        return jsonify(retMap) 


api.add_resource(Download, "/download")
api.add_resource(Status, '/status')


#@app.route('/')
#def hello_world():
#    return "Hello World!\n"


if __name__=="__main__":

    basepath = os.path.dirname(os.path.realpath(__file__))
    config_path =  os.path.join(basepath, "config.ini")
    config = ConfigParser.ConfigParser()
    config.read(config_path)
    app.run(host=config.get('flask', 'host'), port=config.get('flask', 'port'), debug=True)
    #app.run(host='172.16.20.10', port=11008, debug=True)

