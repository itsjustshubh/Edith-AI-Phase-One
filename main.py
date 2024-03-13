from user_data_loader import UserDataLoader
from emotion_analysis import EmotionAnalysis
from typing import Callable, Optional
from user_emotion_model import UserEmotionModel
import os
import sys
import datetime
import json

# Global dictionary for user models
user_models = {}

def parse_user_input(user_input):
    """
    Parses a user input string into a dictionary.

    Args:
        user_input (str): A string representation of user input, formatted as key-value pairs.

    Returns:
        dict: A dictionary with keys and values extracted from the input string.
    """
    user_profile = {}
    for item in user_input.split(", "):
        key, value = item.split(': ')
        key = key.split("'")[1]  # Remove quotes from the key
        # Convert string representations into appropriate data types
        if 'datetime' in value:
            date_str = value.split("(")[1].split(")")[0]
            year, month, day = map(int, date_str.split(", ")[:3])
            value = datetime.datetime(year, month, day)
        elif value == 'None':
            value = None
        elif value in ['True', 'False']:
            value = value == 'True'
        else:
            value = value.strip("'")
        user_profile[key] = value
    return user_profile

def calculate_similarity_score(user_profile, provided_user_details):
    """
    Calculates a similarity score between a user profile and provided user details.

    Args:
        user_profile (dict): The profile of a user.
        provided_user_details (dict): The details of a user to match against.

    Returns:
        float: A normalized similarity score.
    """
    # Define weights for different user attributes
    weights = {
        'age': 0.2, 'gender': 0.1, 'nationality': 0.05, 'languages-spoken': 0.05, # ... other weights
    }

    total_weight = sum(weights.values())
    score = 0

    for key, value in provided_user_details.items():
        if key in user_profile:
            weight = weights.get(key, 0.01)
            user_value = user_profile[key]

            if isinstance(value, int) and isinstance(user_value, int):
                tolerance = 5
                score += weight * max(0, 1 - abs(value - user_value) / tolerance)
            elif isinstance(value, str) and isinstance(user_value, str):
                score += weight if value.lower() == user_value.lower() else 0
            elif isinstance(value, datetime.datetime) and isinstance(user_value, datetime.datetime):
                day_tolerance = 365
                diff_days = abs((value - user_value).days)
                score += weight * max(0, 1 - diff_days / day_tolerance)

    return score / total_weight if total_weight > 0 else 0


def find_most_suitable_user(provided_user_details, users, data_limit=30000, update_progress=None):
    """
    Finds the most suitable users based on provided details.

    Args:
        provided_user_details (dict): User details to match against.
        users (list): A list of User objects.
        data_limit (int): The limit on the amount of data to consider.

    Returns:
        list: A list of tuples containing the user, their score, and data count.
    """
    update_progress("Finding Suitable Users", {"file": "main.py", "function": "find_most_suitable_user"})
    user_scores = [(user, calculate_similarity_score(user.profile, provided_user_details)) for user in users]
    user_scores.sort(key=lambda x: x[1], reverse=True)

    top_users = []
    total_data_count = 0
    data_limit_scale_factor = data_limit / 30000
    score_threshold = 0.5 + 0.25 * data_limit_scale_factor

    for user, score in user_scores:
        if total_data_count < data_limit and score > score_threshold:
            user_data_count = min(len(user.physiological_data), data_limit - total_data_count)
            top_users.append((user, score, user_data_count))
            total_data_count += user_data_count
            # Update progress after adding each top user
            update_progress("Added Top User", {"file": "main.py", "function": "find_most_suitable_user",
                                               "user_id": user.profile.get('unique-id'), "score": score,
                                               "data_count": user_data_count})

    if not top_users and user_scores:
        closest_match = user_scores[0]
        closest_match_data_count = min(len(closest_match[0].physiological_data), data_limit)
        top_users.append((closest_match[0], closest_match[1], closest_match_data_count))
        # Update progress for closest match
        update_progress("Added Closest Match", {"file": "main.py", "function": "find_most_suitable_user",
                                                "user_id": closest_match[0].profile.get('unique-id'),
                                                "user": f"{closest_match[0].profile.get('first-name')} {closest_match[0].profile.get('last-name')}",
                                                "nationality": f"{closest_match[0].profile.get('nationality')}",
                                                "score": closest_match[1], "data_count": closest_match_data_count})

    # Update at the end of finding suitable users
    update_progress("Suitable Users Found",
                    {"file": "main.py", "function": "find_most_suitable_user", "total_suitable_users": len(top_users)})

    # print(f"Found {len(top_users)} suitable users.")
    return top_users


def clear_screen():
    """
    Clears the terminal screen.
    """
    if "TERM" in os.environ:
        os.system('cls' if sys.platform == 'win32' else 'clear')
    else:
        print("\n" * 100)


def display_user_statistics(users, user_index):
    """
    Displays statistics for a given user.

    Args:
        users (list): A list of User objects.
        user_index (int): Index of the user in the list.
    """
    if user_index < 1 or user_index > len(users):
        print("Invalid user index.")
        return

    user = users[user_index - 1]
    print(f"User ID: {user.profile.get('unique-id')}")
    user.print_statistics()


def test_predictions(user, test_samples, update_progress=None):
    """
    Tests and prints predictions for a given user and test samples.

    Args:
        user (User): The user object.
        test_samples (list): A list of test samples.
    """
    update_progress("Testing Custom User Model", {"file": "main.py", "function": "test_predictions", "test_samples": f"{len(test_samples)}"})
    predictions = EmotionAnalysis.make_predictions_for_user(user, test_samples)
    for sample, prediction in zip(test_samples, predictions):
        print(f"Test Sample: {sample}, Predicted Emotion: {prediction}")


def read_user_profile(file_path):
    """
    Reads user profile from a text file.

    Args:
        file_path (str): Path to the file.

    Returns:
        dict: A dictionary containing the user profile.
    """
    user_profile = {}
    with open(file_path, 'r') as file:
        for line in file:
            if line.startswith('#') or line.strip() == '':
                continue
            key, value = line.strip().split(': ')
            if value.isdigit():
                value = int(value)
            elif value.lower() in ['true', 'false']:
                value = value.lower() == 'true'
            user_profile[key] = value
    return user_profile


def read_test_samples(file_path):
    """
    Reads test samples from a text file.

    Args:
        file_path (str): Path to the file.

    Returns:
        list: A list of test samples.
    """
    test_samples = []
    with open(file_path, 'r') as file:
        for line in file:
            if line.startswith('#') or line.strip() == '':
                continue
            sample_data = json.loads(line)
            test_samples.append(sample_data)
    return test_samples

def find_valence_range(emotion):
    """ Map emotions to Spotify valence range. """
    emotion_to_valence = {
        "Happy": (0.7, 1.0),
        "Sad": (0.0, 0.3),
        "Anxious": (0.2, 0.5),
        "Relaxed": (0.4, 0.7),
        "Stressed": (0.1, 0.4),
        "Calm": (0.5, 0.8),
        "Fearful": (0.0, 0.3),
        "Confused": (0.2, 0.5),
        "Content": (0.5, 0.8),
        "Exhausted": (0.1, 0.4),
        "Surprised": (0.6, 0.9),
        "Angry": (0.0, 0.3),
        "Joyful": (0.7, 1.0)
    }
    return emotion_to_valence.get(emotion, (0.0, 1.0))  # Default range if emotion is not in the dictionary

def get_analysis_results(suitable_user_info, user_predictions_list, provided_user_details, update_progress=None):
    """
    Gathers and formats the results of the analysis for frontend display.

    Args:
        suitable_user_info (list): List of tuples containing the user, their score, and data count.
        user_predictions_list (list): A list of dictionaries containing user prediction data.
        provided_user_details (dict): The user details that were used for matching.

    Returns:
        list: A list of dictionaries with formatted results for each user.
    """
    update_progress("Compiling Results", {"file": "main.py", "function": "get_analysis_results"})
    results = []
    for user, score, data_count in suitable_user_info:
        matched_features = {k: user.profile[k] for k in provided_user_details if k in user.profile}

        user_result = {
            "User ID": user.profile.get('unique-id'),
            "Matched Features": matched_features,
            "Predictions": []
        }

        predictions = EmotionAnalysis.make_predictions_for_user(user, user_predictions_list)
        for sample, prediction in zip(user_predictions_list, predictions):
            sample_with_prediction = sample.copy()
            sample_with_prediction["Predicted Emotion"] = prediction
            valence_low, valence_high = find_valence_range(prediction)
            sample_with_prediction["Valence Range"] = [valence_low, valence_high]
            user_result["Predictions"].append(sample_with_prediction)

        results.append(user_result)

    return results


def main(directory_path, data_limit=30000, user_profile_dict=None, user_predictions_list=None,
         display_results=False, emit_progress: Optional[Callable[[str], None]] = None):
    """
    Main function to execute the application logic.

    Args:
        directory_path (str): Path to the directory containing user data.
        data_limit (int): Limit on the amount of data to consider.
        user_profile_dict (dict, optional): A dictionary containing the user profile.
        user_predictions_list (list, optional): A list of dictionaries containing user prediction data.
    """
    def update_progress(stage: str, details: dict = None):
        if emit_progress:
            try:
                print(f"{stage}: {details}")
                emit_progress(stage, details)
            except Exception as e:
                print(f"Error in emit_progress: {e}")
        else:
            # Fallback for non-SocketIO environments
            detail_str = ", ".join([f"{key}: {value}" for key, value in details.items()]) if details else ""
            print(f"{stage}" + (f" - {detail_str}" if detail_str else ""))

    # Emitting a progress update at the start of the analysis.
    update_progress("Initializing Analysis", {"file": "main.py", "function": "main"})

    # Loading user data from the provided directory path.
    data_loader = UserDataLoader(directory_path, update_progress=update_progress)
    users = data_loader.load_users()

    # Handling the case where no users are found in the directory.
    if not users:
        update_progress("No users found in the directory.")
        return

    # Reading the user profile if not already provided.
    if user_profile_dict is None:
        update_progress("Reading User Profile")
        user_profile_path = os.path.join("test-user", "user-profile.txt")
        try:
            user_profile_dict = read_user_profile(user_profile_path)
        except FileNotFoundError:
            update_progress("User profile file not found", {"path": user_profile_path})
            return
        except json.JSONDecodeError:
            update_progress("Error decoding JSON", {"file": user_profile_path})
            return

    # Finding the most suitable users based on the provided profile.
    suitable_user_info = find_most_suitable_user(user_profile_dict, users, data_limit, update_progress=update_progress)

    # Reading user predictions, if not provided.
    if user_predictions_list is None:
        update_progress("Reading User Predictions")
        test_samples_path = os.path.join("test-user", "user-predictions.txt")
        try:
            user_predictions_list = read_test_samples(test_samples_path)
        except FileNotFoundError:
            update_progress("Test samples file not found", {"path": test_samples_path})
            return
        except json.JSONDecodeError:
            update_progress("Error decoding JSON", {"file": test_samples_path})
            return

    # Processing suitable users and making predictions based on the data.
    for user, score, data_count in suitable_user_info:
        if not user.emotion_model.is_trained:
            limited_data = user.physiological_data[:data_count]
            EmotionAnalysis.train_user_model(user, limited_data, update_progress=update_progress)
            test_predictions(user, user_predictions_list, update_progress=update_progress)

    # Compiling the results for display if required.
    if display_results:
        results = get_analysis_results(suitable_user_info, user_predictions_list, user_profile_dict, update_progress=update_progress)
        for result in results:
            print(json.dumps(result, indent=4))  # Pretty print the results

    # Indicating the completion of the analysis process.
    update_progress("Analysis Complete", {"file": "main.py", "function": "main"})
    return results if display_results else None

if __name__ == "__main__":
    directory_path = "sample-users"
    custom_data_limit = 100000
    user_profile = {'age': 19, 'gender': 'female', 'nationality': 'Indian','smoking-habits': 'none','ethnicity':'Indian','sleep-patterns':'regular'}
    user_predictions = [{"heart-rate-bpm": 60, "breathing-rate-breaths-min": 20, "hrv-ms": 30, "skin-temp-c": 20, "emg-mv": 0.1, "bvp-unit": 0.2},
                        {"heart-rate-bpm": 80, "breathing-rate-breaths-min": 18, "hrv-ms": 55, "skin-temp-c": 32, "emg-mv": 0.3, "bvp-unit": 0.9}]
    results = main(directory_path, data_limit=custom_data_limit, user_profile_dict=user_profile,
                   user_predictions_list=user_predictions, display_results=False)
    # print(results)
