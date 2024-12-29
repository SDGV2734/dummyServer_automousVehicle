from flask import Flask, jsonify
import random
import time

app = Flask(__name__)

# Helper functions to generate random data
def generate_speed():
    return round(random.uniform(0, 200), 2)  # Speed in km/h

def generate_temperature():
    return round(random.uniform(-30, 50), 2)  # Temperature in °C

def generate_gps():
    latitude = round(random.uniform(-90, 90), 6)  # Latitude
    longitude = round(random.uniform(-180, 180), 6)  # Longitude
    return {"latitude": latitude, "longitude": longitude}

def generate_battery_level():
    return round(random.uniform(0, 100), 2)  # Battery level in percentage

# Route for root URL
@app.route('/')
def index():
    return "Welcome to the Dummy Web Server!"

# Routes to fetch the data
@app.route('/sensor_data', methods=['GET'])
def get_sensor_data():
    data = {
        "speed": generate_speed(),
        "temperature": generate_temperature(),
        "gps": generate_gps(),
        "battery_level": generate_battery_level(),
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())
    }
    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True)
