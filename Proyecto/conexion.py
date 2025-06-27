from flask import Flask, jsonify, render_template
from pymongo import MongoClient
from datetime import datetime
import pytz

app = Flask(__name__)

# Configura zona horaria
timezone = pytz.timezone('America/Bogota')

# MongoDB URI
mongo_uri = "mongodb+srv://sidney9903:Signey9903%2A@cluster0.yb6qrvx.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
client = MongoClient(mongo_uri)
db = client["arduino_db"]
coleccion = db["dht11"]

@app.route('/')
def index():
    # Obtener últimos 10 registros
    datos = list(coleccion.find().sort("timestamp", -1).limit(10))
    for d in datos:
        d["_id"] = str(d["_id"])
        # Convertir timestamp float a ISO string con zona horaria
        d["timestamp"] = datetime.fromtimestamp(d["timestamp"], timezone).isoformat()
    return render_template('index.html', datos=datos)

@app.route('/api/datos')
def api_datos():
    datos = list(coleccion.find().sort("timestamp", -1).limit(50))
    for d in datos:
        d["_id"] = str(d["_id"])
        d["timestamp"] = datetime.fromtimestamp(d["timestamp"], timezone).isoformat()
    return jsonify(datos)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
