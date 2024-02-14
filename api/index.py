from flask import Flask, jsonify, request, json, render_template

app = Flask(__name__)

moods_data = []

@app.route('/')
def home():
    return('index.html')


@app.route('/about')
def about():
    return('about.html')

@app.route('/send_moods', methods=['POST'])
def send_moods():
    try:
        data = request.get_json(force=True)
        moods = data['moods']

        if moods is None:
            return jsonify({"error":"Wrong data"},400)
        
        moods_data.append(moods)
        return jsonify({"message": "Mood sent successfully"}), 200
    
    except Exception as e:
        return jsonify({"error":str(e)}),500
    
@app.route('/get_moods', methods=['GET'])    
def hae_keskiarvo():
    try:
        if not moods_data:
            return jsonify({"message": "Ei dataa saatavilla"}), 200

        return jsonify({moods_data}), 200

    except Exception as e:
        return jsonify({"error":str(e)}, 500)