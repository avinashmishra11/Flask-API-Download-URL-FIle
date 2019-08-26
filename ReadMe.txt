#Flask restful API for file downloading

Make sure you have MySQL database and Python version 2.7 and above.

## Flask Restful API
A simple Flask Restful API using Flask-restful

## Description
- A simple Flask Restful API with following endpoints:
    - /download : **POST method**
    - /status : **GET method**

Download Method
---------------

- Input data format
```
 --> {"url":"http://codex.cs.yale.edu/avi/db-book/db4/slide-dir/ch1-2.pdf"}
example: curl http://0.0.0.0:80/download -d '{"url":"http://codex.cs.yale.edu/avi/db-book/db4/slide-dir/ch1-2.pdf"}' -H 'Content-Type: application/json'

```
- Response format
```
{
 'File ID': "1",                  ##ID to keep a track of file
 'Message': "Success",            ##Success or Error Message
 'Status Code': "200"             ##200 for success
}
```

Status Method
---------------

- Input data format
```
 --> "id" =  <File ID>
example : curl http://0.0.0.0:80/status?id=1

```
- Response format
```
{
 'Message': "Success",            ##Success or Error Message
 'Data'   : {                     ## File download info
    "downloaded": "366592",
    "end time": "Mon, 26 Aug 2019 12:23:06 GMT",
    "file_id": "1",
    "remaining size": "88988.0",
    "start time": "Mon, 26 Aug 2019 12:22:51 GMT",
    "upload size": "455580",
    "url": "http%3A//codex.cs.yale.edu/avi/db-book/db4/slide-dir/ch1-2.pdf",
    "user ip": "0.0.0.0"
  }
 'Status Code': "200"             ##200 for success
}
```


-----------------
$$ How to run $$
-----------------

* Clone the repo
* $ cd Flask-API-Download-URL-FIle-master
* Install required packages using --> "pip install -r requirements.txt"
* open config file <config.ini> and provide mysql details (ip, user, password, database name)
* database name provided in config file will be used to maintain file download info
* in config file provide host ip and port number for Flask service
* run --> "python create_db.py" <-- for creating all required databases and tables
* run --> "python app.py" <-- for starting flask restful service
-----------------
$$ Upload URL $$
-----------------
Use any of the below method to upload URL and view result:
* host the ip:port (ex : http://0.0.0.0:80/) to browser for upload form (upload URL from UI and also check status there)
* use curl or other techniques to initiate request 


Note :: Downloaded files can be find in 'Flask-API-Download-URL-FIle-master/url_file_downloads/' directory.




