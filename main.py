from apitest import ApiTest
from flask import Flask,request,jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

local_server=True

app=Flask(__name__)


app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///Files.sqlite3"
db=SQLAlchemy(app)

#database models
class SONGFILE(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(100),nullable=False)
    duration=db.Column(db.Integer,nullable=False)
    upload_time=db.Column(db.DateTime,nullable=False)

    def __init__(self,name,duration,upload_time):
        self.name=name
        self.duration=duration
        self.upload_time=upload_time

class PodcastFile(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(100),nullable=False)
    duration=db.Column(db.Integer,nullable=False)
    upload_time=db.Column(db.DateTime,nullable=False)
    host=db.Column(db.String(100),nullable=False)
    participants=db.Column(db.String,nullable=True)
    
    def __init__(self,name,duration,upload_time,host):
        self.name=name
        self.duration=duration
        self.upload_time=upload_time
        self.host=host
        #self.participants=kwargs['participants']



class AudioBook(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    title=db.Column(db.String(100),nullable=False)
    author=db.Column(db.Integer,nullable=False)
    narrator=db.Column(db.Integer,nullable=False)
    host=db.Column(db.String(100),nullable=False)
    duration=db.Column(db.Integer,nullable=False)
    upload_time=db.Column(db.DateTime,nullable=False)
    
    def __init__(self,title,author,narrator,host,duration,upload_time):
        self.title=title
        self.author=author
        self.narrator=narrator
        self.host=host
        self.duration=duration
        self.upload_time=upload_time

@app.route("/")
def index():
    return {"Main": "Page"}
    
#CREATE
@app.route('/create',methods=['POST'])
def create():
    if request.content_type=='application/json':
        file_data=request.get_json()
        if file_data['audioFileType'].lower()=='song':
            print(file_data)
            name=file_data['audioFileMetadata']['Name']
            duration=file_data['audioFileMetadata']['Duration']
            upload_time=datetime.now() 
            query=SONGFILE(name,duration,upload_time)
            db.session.add(query)
            db.session.commit()
            return "Song Insertion is successful"
            
        if file_data['audioFileType'].lower()=='podcast':
            name=file_data['audioFileMetadata']['Name']
            duration=file_data['audioFileMetadata']['Duration']
            upload_time=datetime.now()
            host=file_data['audioFileMetadata']['Host']
            if 'Participants' in file_data:
                participants=file_data['audioFileMetadata']['Participants']
                query=PodcastFile(name,duration,upload_time,host,participants)
            else:
                query=PodcastFile(name,duration,upload_time,host)
            db.session.add(query)
            db.session.commit()
            return "Podcast Insertion is successful"

        if file_data['audioFileType'].lower()=='audiobook':
            title=file_data['audioFileMetadata']['Title']
            author=file_data['audioFileMetadata']['Author']
            narrator=file_data['audioFileMetadata']['Narrator']
            host=file_data['audioFileMetadata']['Host']
            duration=file_data['audioFileMetadata']['Duration']
            upload_time=datetime.now()
            query=AudioBook(title,author,narrator,host,duration,upload_time)
            db.session.add(query)
            db.session.commit()
            return "Audiobook Insertion is successful"
        db.session.commit()
        return "Error occured"
    else:
        return "Error Json data Needed"


#DELETE 
@app.route('/delete/<string:audiofiletype>/<int:sid>',methods=['GET'])
def delete(audiofiletype,sid):
    aft=audiofiletype
    print(aft,sid)

    if aft=="song":    
        SONGFILE.query.filter_by(id=int(sid)).delete()
        db.session.commit()
    if aft=="podcast":    
        PodcastFile.query.filter_by(id=int(sid)).delete()
        db.session.commit()
    if aft=="audiobook":    
        AudioBook.query.filter_by(id=int(sid)).delete()
        db.session.commit()
    db.session.commit()
    return "Deleted Successful"

#UPDATE
@app.route('/update/<string:audiofiletype>/<sid>',methods=['POST'])
def update(audiofiletype,sid):
    if request.content_type=='application/json':
        file_data=request.get_json()
        if audiofiletype=='song':
            data=SONGFILE.query.filter_by(id=int(sid)).first()
            data.name=file_data['Name']
            data.duration=file_data['Duration']
            #data.upload_time=datetime.now()
            
        if audiofiletype=='podcast':
            data=PodcastFile.query.filter_by(id=int(sid)).first()
            data.name=file_data['Name']
            data.duration=file_data['Duration']
            #data.upload_time=str(datetime.now())
            data.host=file_data['Host']
            if 'Participants' in file_data:
                data.participants=file_data['Participants']

            
        if audiofiletype=='audiobook':

            data=AudioBook.query.filter_by(id=int(sid)).first()
            data.title=file_data['Title']
            data.author=file_data['Author']
            data.narrator=file_data['Narrator']
            data.host=file_data['Host']
            data.duration=file_data['Duration']
            #data.upload_time=str(datetime.now())
        db.session.commit()
        return "Action is successful"

#GET
@app.route('/get/<audioFileType>/<audioFileID>')
def get(audioFileType,audioFileID):
    if audioFileType=='song':
        song=SONGFILE.query.filter_by(id=int(audioFileID)).first()
        if song==None:
            return jsonify({"Error":"No data exist"})
        else:
            data={"Name":str(song.name),
            "Duration":str(song.duration),
            "Uploaded_time":str(song.upload_time)
            }
            return jsonify(data)
    elif audioFileType=='podcast':
        pod=PodcastFile.query.filter_by(id=int(audioFileID)).first()
        if pod==None:
            return jsonify({"Error":"No data exist"})
        else:
            data={"Name":str(pod.name),
            "Duration":str(pod.duration),
            "Uploaded_time":str(pod.upload_time),
            "Host":str(pod.host),
            "participants":pod.participants
            }
            return jsonify(data)
    elif audioFileType=='audiobook':
        audiobook=AudioBook.query.filter_by(id=int(audioFileID)).first()
        if audiobook==None:
            return jsonify({"Error":"No data exist"})
        else:
            data={"Title":str(audiobook.title),
            "Author":audiobook.title,
            "Narrator":audiobook.narrator,
            "Duration":str(audiobook.duration),
            "Uploaded_time":str(audiobook.upload_time),

            }
            return jsonify(data)

@app.route('/get/<audioFileType>')
def getall(audioFileType):
    data=[]
    if audioFileType=='song':
        songs=SONGFILE.query.all()
        for song in songs:
            data.append({"Name":str(song.name),
        "Duration":str(song.duration),
        "Uploaded_time":str(song.upload_time)
        })
        return jsonify(data)
    elif audioFileType=='podcast':
        pods=PodcastFile.query.all()
        for pod in pods:
            data.append({"Name":str(pod.name),
        "Duration":str(pod.duration),
        "Uploaded_time":str(pod.upload_time),
        "Host":str(pod.host),
        "participants":pod.participants
        })
        return jsonify(data)
    elif audioFileType=='audiobook':
        audiobooks=AudioBook.query.all()
        for audiobook in audiobooks:
            data.append({"Title":str(audiobook.title),
        "Author":audiobook.title,
        "Narrator":audiobook.narrator,
        "Duration":str(audiobook.duration),
        "Uploaded_time":str(audiobook.upload_time)
        })

        return jsonify(data)




if __name__ == "__main__":
    db.create_all()
    app.run(debug=True)
    unittest.main()

