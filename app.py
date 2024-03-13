from main import main, get_analysis_results
from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_socketio import SocketIO
import threading

app = Flask(__name__)

# Configuring CORS for HTTP routes
CORS(app, resources={r"/analyze-emotion": {"origins": ["http://localhost:3000", "https://harmonize-ai.vercel.app"]}})

# Configuring CORS for SocketIO
socketio = SocketIO(app, cors_allowed_origins=["http://localhost:3000", "https://harmonize-ai.vercel.app"])

def analyze_and_emit(socketio, directory_path, data_limit, user_profile_dict, user_predictions_list):
    try:
        # Using a structured JSON format for progress updates
        emit_progress = lambda stage, details=None: socketio.emit('progress', {'stage': stage, 'details': details})

        # Call the main function with the emit_progress function
        results = main(directory_path, data_limit, user_profile_dict, user_predictions_list,
                       display_results=True, emit_progress=emit_progress)

        socketio.emit('completed', {'results': results})
    except Exception as e:
        socketio.emit('error', {'message': str(e)})

def start_analysis_task(directory_path, data_limit, user_profile_dict, user_predictions_list):
    """ Function to start the analysis in a separate thread """
    with app.app_context():
        analyze_and_emit(socketio, directory_path, data_limit, user_profile_dict, user_predictions_list)

@app.route('/analyze-emotion', methods=['POST'])
def analyze_emotion():
    data = request.json
    directory_path = data.get('directory_path', 'sample-users')
    data_limit = data.get('data_limit', 30000)
    user_profile_dict = data.get('user_profile', {'age': 19, 'gender': 'male'})
    user_predictions_list = data.get('user_predictions', [
        {"heart-rate-bpm": 120, "breathing-rate-breaths-min": 24, "hrv-ms": 30, "skin-temp-c": 20, "emg-mv": 0.1, "bvp-unit": 0.2},
        {"heart-rate-bpm": 80, "breathing-rate-breaths-min": 18, "hrv-ms": 55, "skin-temp-c": 32, "emg-mv": 0.3, "bvp-unit": 0.9}])

    # Schedule the analysis task to start after the request has been responded to
    threading.Thread(target=start_analysis_task, args=(directory_path, data_limit, user_profile_dict, user_predictions_list)).start()

    return jsonify({'message': 'Analysis started'}), 202

if __name__ == '__main__':
    socketio.run(app, debug=True, allow_unsafe_werkzeug=True)
