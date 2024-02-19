from flask import Flask, jsonify, request, json, render_template
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from flask_cors import cross_origin
from datetime import datetime

app = Flask(__name__)

uri = "mongodb+srv://username:Salasana123@cluster0.u6i2ndi.mongodb.net/?retryWrites=true&w=majority"
# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))

db = client["data"]
column = db["moods"]


#oletussivuna pelkistetty hello world, jättää myös vercelin lokiin viestin jos mongoDB toimii
@app.route('/')
def home():
    try:
        client.admin.command('ping')
        print("Pinged your deployment. You successfully connected to MongoDB!")
    except Exception as e:
        print(e)
    return ("Hello server world : )")


@app.route('/send_moods', methods=['POST'])
@cross_origin()
def send_moods():
    try:
        data = request.get_json(force=True)
        current_time = datetime.utcnow()

        moods = {
                 "value":data["moods"],
                 "time": current_time
                 }

        if moods is None:
            return jsonify({"error":"Wrong data"},400)
        
        x = column.insert_one(moods)
        return jsonify({"message": "Mood sent successfully", "inserted id": str(x.inserted_id)}), 200
    
    except Exception as e:
        return jsonify({"error":str(e)}),500
    
@app.route('/get_moods', methods=['GET'])
@cross_origin()    
def get_moods():
    try:
        cursor = column.find({},{"_id": 0})
        result = list(cursor)

        return jsonify({'data':result}), 200

    except Exception as e:
        return jsonify({"error":str(e)}, 500)
    
@app.route('/get_average', methods=['GET'])
@cross_origin()    
def get_average():
    try:
        cursor = column.find({},{"_id": 0})
        result = list(cursor)
        
        return jsonify({'data':result}), 200

    except Exception as e:
        return jsonify({"error":str(e)}, 500)
    