from flask import Flask, jsonify, request, json, render_template
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

app = Flask(__name__)

uri = "mongodb+srv://username:Salasana123@cluster0.u6i2ndi.mongodb.net/?retryWrites=true&w=majority"
# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))

db = client["data"]
column = db["moods"]


moods_data = []

@app.route('/')
def home():
    try:
        client.admin.command('ping')
        print("Pinged your deployment. You successfully connected to MongoDB!")
    except Exception as e:
        print(e)
    return ("Hello server world : )")


@app.route('/send_moods', methods=['POST'])
def send_moods():
    try:
        data = request.get_json(force=True)
        moods = ({
                 'value':data['moods'],
                 'time': data['time']
                 })

        if moods is None:
            return jsonify({"error":"Wrong data"},400)
        
        x = column.insert_one(moods)
        return jsonify({"message": "Mood sent successfully"}), 200
    
    except Exception as e:
        return jsonify({"error":str(e)}),500
    
@app.route('/get_moods', methods=['GET'])    
def get_moods():
    try:
        if not moods_data:
            return jsonify({"message": "Ei dataa saatavilla"}), 200

        return jsonify({'data':moods_data}), 200

    except Exception as e:
        return jsonify({"error":str(e)}, 500)
    
@app.route('/clear_moods', methods=['GET'])    
def clear_moods():
    moods_data.clear()

    return "Moods data cleared!!"