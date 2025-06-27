import serial
import json
from pymongo import MongoClient
import time

# Configurar puerto serial (ajusta el puerto a tu configuración)
arduino = serial.Serial('COM12', 9600, timeout=1)
time.sleep(2)  # Espera a que Arduino se inicialice

# MongoDB Atlas - contraseña con URL encoding si tiene caracteres especiales
mongo_uri = "mongodb+srv://sidney9903:Signey9903%2A@cluster0.yb6qrvx.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
cliente = MongoClient(mongo_uri)

# Selecciona base de datos y colección
bd = cliente["arduino_db"]
coleccion = bd["dht11"]

print("Inicio de lectura desde DHT11...")

try:
    while True:
        if arduino.in_waiting:
            raw_line = arduino.readline()
            try:
                # Decodifica ignorando errores
                linea = raw_line.decode(errors='ignore').strip()
                print("Recibido:", linea)
                # Intenta convertir a JSON
                data = json.loads(linea)
                data["timestamp"] = time.time()
                # Guarda en MongoDB
                coleccion.insert_one(data)
                print("Guardado en MongoDB:", data)
            except json.JSONDecodeError:
                print("Dato inválido, no es JSON:", linea)
except KeyboardInterrupt:
    print("\nLectura detenida por el usuario.")
    arduino.close()
    cliente.close()
