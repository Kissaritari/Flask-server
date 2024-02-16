from flask import Flask, jsonify, request, json, render_template

app = Flask(__name__)

moods_data = []


@app.route('/')
def home():
    return ("Hello server world : )")


@app.route('/send_moods', methods=['POST'])
def send_moods():
    try:
        data = request.get_json(force=True)
        moods = {'mood':({
                 'value':data['moods'],
                 'time': data['time']
                 })}

        if moods is None:
            return jsonify({"error":"Wrong data"},400)
        
        moods_data.append(moods)
        return jsonify({"message": "Mood sent successfully"}), 200
    
    except Exception as e:
        return jsonify({"error":str(e)}),500
    
@app.route('/get_moods', methods=['GET'])    
def get_moods():
    try:
        if not moods_data:
            return jsonify({"message": "Ei dataa saatavilla"}), 200

        return jsonify({"moods":moods_data,
                        "time":moods_data}), 200

    except Exception as e:
        return jsonify({"error":str(e)}, 500)
    
@app.route('/clear_moods', methods=['GET'])    
def clear_moods():
    moods_data.clear()

    return "Moods data cleared!!"