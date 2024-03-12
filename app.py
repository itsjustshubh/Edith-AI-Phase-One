# from flask import Flask, request, jsonify
# from flask_cors import CORS
# from flask_socketio import SocketIO, emit
# import threading
#
# # Import necessary modules and functions
# from main import main, get_analysis_results  # replace with actual module names and functions
#
# app = Flask(__name__)
# CORS(app)
# socketio = SocketIO(app, cors_allowed_origins='*')
#
# def analyze_and_emit(directory_path, data_limit, user_profile_dict, user_predictions_list):
#     # Stage 1: Initializing Analysis
#     emit('progress', {'stage': 'Initializing Analysis'})
#     socketio.sleep(2)  # Simulating delay
#
#     # Stage 2: Loading Data
#     emit('progress', {'stage': 'Loading Data'})
#     socketio.sleep(2)  # Simulating delay
#
#     # Stage 3: Preprocessing Data
#     emit('progress', {'stage': 'Preprocessing Data'})
#     socketio.sleep(2)  # Simulating delay
#
#     # Stage 4: Analyzing Emotional Trends
#     emit('progress', {'stage': 'Analyzing Emotional Trends'})
#     socketio.sleep(3)  # Simulating a longer process
#
#     # Stage 5: Compiling Results
#     emit('progress', {'stage': 'Compiling Results'})
#     socketio.sleep(2)  # Simulating delay
#
#     # Stage 6: Finalizing Report
#     emit('progress', {'stage': 'Finalizing Report'})
#     socketio.sleep(2)  # Simulating delay
#
#     # Actual processing
#     # Replace this with the call to your main processing function and any additional logic
#     results = main(directory_path, data_limit, user_profile_dict, user_predictions_list, display_results=True)
#
#     # Emit final results
#     emit('completed', {'results': results})
#
# @app.route('/analyze-emotion', methods=['POST'])
# def analyze_emotion():
#     data = request.json
#
#     # Extract details from the request
#     directory_path = data.get('directory_path', 'sample-users')  # Adjust as needed
#     data_limit = data.get('data_limit', 30000)
#     user_profile_dict = data.get('user_profile', {'age': 19, 'gender': 'male'})
#     user_predictions_list = data.get('user_predictions', [{"heart-rate-bpm": 120, "breathing-rate-breaths-min": 24, "hrv-ms": 30, "skin-temp-c": 20, "emg-mv": 0.1, "bvp-unit": 0.2},
#                         {"heart-rate-bpm": 80, "breathing-rate-breaths-min": 18, "hrv-ms": 55, "skin-temp-c": 32, "emg-mv": 0.3, "bvp-unit": 0.9}])
#
#     # Call the main function for processing
#     results = main(directory_path, data_limit, user_profile_dict, user_predictions_list, display_results=True)
#
#     # Check if results are empty or None
#     if not results:
#         return jsonify({'error': 'Analysis results are empty'}), 404
#
#     # Start a background thread for processing and emitting updates
#     threading.Thread(target=analyze_and_emit,
#                      args=(directory_path, data_limit, user_profile_dict, user_predictions_list)).start()
#
#     return jsonify({'message': 'Analysis started'}), 202
#
# if __name__ == '__main__':
#     socketio.run(app, debug=True, allow_unsafe_werkzeug=True)

from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_socketio import SocketIO
import threading

# Import necessary modules and functions
# Replace 'main' and 'get_analysis_results' with your actual module names and functions
from main import main, get_analysis_results

app = Flask(__name__)
CORS(app)
socketio = SocketIO(app, cors_allowed_origins='*')

def analyze_and_emit(socketio, directory_path, data_limit, user_profile_dict, user_predictions_list):
    try:
        # Use the socketio.emit function as the emit_progress function
        emit_progress = lambda stage: socketio.emit('progress', {'stage': stage})

        # Call the main function with the emit_progress function
        results = main(directory_path, data_limit, user_profile_dict, user_predictions_list,
                       display_results=True, emit_progress=emit_progress)

        socketio.emit('completed', {'results': results})
    except Exception as e:
        socketio.emit('error', {'message': str(e)})

@app.route('/analyze-emotion', methods=['POST'])
def analyze_emotion():
    data = request.json
    directory_path = data.get('directory_path', 'sample-users')
    data_limit = data.get('data_limit', 30000)
    user_profile_dict = data.get('user_profile', {'age': 19, 'gender': 'male'})
    user_predictions_list = data.get('user_predictions', [
        {"heart-rate-bpm": 120, "breathing-rate-breaths-min": 24, "hrv-ms": 30, "skin-temp-c": 20, "emg-mv": 0.1,
         "bvp-unit": 0.2},
        {"heart-rate-bpm": 80, "breathing-rate-breaths-min": 18, "hrv-ms": 55, "skin-temp-c": 32, "emg-mv": 0.3,
         "bvp-unit": 0.9}])

    socketio.start_background_task(analyze_and_emit, socketio, directory_path, data_limit, user_profile_dict, user_predictions_list)

    return jsonify({'message': 'Analysis started'}), 202

if __name__ == '__main__':
    socketio.run(app, debug=True, allow_unsafe_werkzeug=True)
