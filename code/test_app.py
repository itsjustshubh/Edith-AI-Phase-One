import time  # Add this import at the beginning of your test file
import json
import pytest
from app import app, socketio

@pytest.fixture
def client():
    app.config['TESTING'] = True
    return app.test_client()

@pytest.fixture
def socketio_client():
    return socketio.test_client(app)

def test_analyze_emotion_route(client):
    # Sample data for a valid request
    valid_data = {
        "data_limit": 10000,
        "user_profile": {"age": 21, "gender": "female"},
        "user_predictions": [
            {"heart-rate-bpm": 120, "breathing-rate-breaths-min": 24, "hrv-ms": 30, "skin-temp-c": 20, "emg-mv": 0.1, "bvp-unit": 0.2},
            {"heart-rate-bpm": 80, "breathing-rate-breaths-min": 18, "hrv-ms": 55, "skin-temp-c": 32, "emg-mv": 0.3, "bvp-unit": 0.9}
        ]
    }

    response = client.post('/analyze-emotion', data=json.dumps(valid_data), content_type='application/json')
    assert response.status_code == 202
    response_data = json.loads(response.data)
    assert response_data['message'] == 'Analysis started'

def test_socketio_events(socketio_client):
    # Sample data to send
    data = {
        "data_limit": 10000,
        "user_profile": {"age": 21, "gender": "female"},
        "user_predictions": [
            {"heart-rate-bpm": 120, "breathing-rate-breaths-min": 24, "hrv-ms": 30, "skin-temp-c": 20, "emg-mv": 0.1,
             "bvp-unit": 0.2},
            {"heart-rate-bpm": 80, "breathing-rate-breaths-min": 18, "hrv-ms": 55, "skin-temp-c": 32, "emg-mv": 0.3,
             "bvp-unit": 0.9}
        ]
    }

    socketio_client.emit('analyze-emotion', data)
    socketio_client.get_received()  # Clear previously received messages

    timeout = 25
    start_time = time.time()
    received = []

    while time.time() - start_time < timeout and not received:
        received = socketio_client.get_received()
        time.sleep(0.5)

    assert len(received) > 0
    assert received[0]['name'] == 'progress'
    assert 'stage' in received[0]['args'][0]

def test_error_handling(client):
    # Sample invalid data
    invalid_data = {
        "data_limit": 10000,
        "user_profile": {"age": 21, "gender": "jedi"},
        "user_predictions": [
            {"heart-rate-bpm": 120, "breathing-rate-breaths-min": 24, "hrv-ms": 30, "skin-temp-c": 20, "emg-mv": 0.1,
             "bvp-unit": 0.2},
            {"heart-rate-bpm": 80, "breathing-rate-breaths-min": 18, "hrv-ms": 55, "skin-temp-c": 32, "emg-mv": 0.3,
             "bvp-unit": 0.9}
        ]
    }

    response = client.post('/analyze-emotion', data=json.dumps(invalid_data), content_type='application/json')
    assert response.status_code != 200