import requests
import socketio
import threading
import time

sio = socketio.Client()
analysis_completed = False

@sio.event
def connect():
    print("Connected to the server.")

@sio.event
def progress(data):
    print("Progress Update:", data)

@sio.event
def completed(data):
    global analysis_completed
    print("Analysis Completed:", data)
    analysis_completed = True

@sio.event
def disconnect():
    print("Disconnected from server.")

def send_data():
    url = 'http://127.0.0.1:5000/analyze-emotion'
    data = {
        "data_limit": 10000,
        "user_profile": {
            "age": 21,
            "gender": "female"
        },
        "user_predictions": [
            {
                "heart-rate-bpm": 120,
                "breathing-rate-breaths-min": 24,
                "hrv-ms": 30,
                "skin-temp-c": 20,
                "emg-mv": 0.1,
                "bvp-unit": 0.2
            },
            # {
            #     "heart-rate-bpm": 80,
            #     "breathing-rate-breaths-min": 18,
            #     "hrv-ms": 55,
            #     "skin-temp-c": 32,
            #     "emg-mv": 0.3,
            #     "bvp-unit": 0.9
            # }
        ]
    }
    response = requests.post(url, json=data)
    print("Status Code:", response.status_code)
    print("Response:", response.json())

sio.connect('http://127.0.0.1:5000')
threading.Thread(target=send_data).start()

while not analysis_completed:
    time.sleep(1)

sio.disconnect()
