from user_data_loader import UserDataLoader
from emotion_analysis import EmotionAnalysis
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
                # Numerical comparison with tolerance
                tolerance = 5  # years for age, etc.
                score += weight * max(0, 1 - abs(value - user_value) / tolerance)

            elif isinstance(value, str) and isinstance(user_value, str):
                # Categorical comparison
                score += weight if value.lower() == user_value.lower() else 0

            elif isinstance(value, datetime.datetime) and isinstance(user_value, datetime.datetime):
                # Date comparison with a tolerance of days
                day_tolerance = 365  # one year
                diff_days = abs((value - user_value).days)
                score += weight * max(0, 1 - diff_days / day_tolerance)

    normalized_score = score / total_weight if total_weight > 0 else 0
    return normalized_score

def find_most_suitable_user(provided_user_details, users, data_limit=30000):
    user_scores = [(user, calculate_similarity_score(user.profile, provided_user_details)) for user in users]
    user_scores.sort(key=lambda x: x[1], reverse=True)  # Sort users based on their similarity scores

    top_users = []
    total_data_count = 0
    data_limit_scale_factor = data_limit / 30000  # Calculate a scaling factor based on the data limit

    # Adjust score threshold based on data limit
    score_threshold = 0.5 + 0.25 * data_limit_scale_factor  # Increase threshold as data limit increases

    for user, score in user_scores:
        if total_data_count < data_limit and score > score_threshold:
            user_data_count = min(len(user.physiological_data), data_limit - total_data_count)
            top_users.append((user, score, user_data_count))
            total_data_count += user_data_count

    if not top_users and user_scores:
        # If no suitable users are found, choose the closest match
        closest_match = user_scores[0]
        closest_match_data_count = min(len(closest_match[0].physiological_data), data_limit)
        top_users.append((closest_match[0], closest_match[1], closest_match_data_count))

    return top_users

def clear_screen():
    # Check if 'TERM' environment variable is set
    if "TERM" in os.environ:
        if sys.platform == 'win32':
            os.system('cls')  # For Windows
        else:
            os.system('clear')  # For macOS and Linux
    else:
        print("\n" * 100)  # Fallback method to clear the screen

def display_user_statistics(users, user_index):
    # Display statistics for a given user
    if user_index < 1 or user_index > len(users):
        print("Invalid user index.")
        return

    user = users[user_index - 1]  # Adjust index for 0-based list
    print(f"User ID: {user.profile.get('unique-id')}")
    user.print_statistics()  # Assumes User class has a method print_statistics()

def test_predictions(user, test_samples):
    predictions = EmotionAnalysis.make_predictions_for_user(user, test_samples)
    for sample, prediction in zip(test_samples, predictions):
        print(f"Test Sample: {sample}, Predicted Emotion: {prediction}")

def read_user_profile(file_path):
    user_profile = {}
    with open(file_path, 'r') as file:
        for line in file:
            if line.startswith('#') or line.strip() == '':
                continue  # Skip comments or empty lines
            key, value = line.strip().split(': ')
            if value.isdigit():
                value = int(value)
            elif value.lower() in ['true', 'false']:
                value = value.lower() == 'true'
            user_profile[key] = value
    return user_profile

def read_test_samples(file_path):
    test_samples = []
    with open(file_path, 'r') as file:
        for line in file:
            if line.startswith('#') or line.strip() == '':
                continue  # Skip comments or empty lines
            sample_data = json.loads(line)
            test_samples.append(sample_data)
    return test_samples

def main(directory_path, data_limit=30000):
    data_loader = UserDataLoader(directory_path)
    users = data_loader.load_users()

    if not users:
        print("No users found in the directory.")
        return

    # Read preferred user details from a file
    user_profile_path = os.path.join("test-user", "user-profile.txt")
    try:
        preferred_user_details = read_user_profile(user_profile_path)
    except FileNotFoundError:
        print(f"User profile file not found in path: {user_profile_path}")
        return
    except json.JSONDecodeError:
        print(f"Error decoding JSON from the user profile file: {user_profile_path}")
        return

    # Find and display the most suitable users
    suitable_user_info = find_most_suitable_user(preferred_user_details, users, data_limit)
    print("\nSuitable Users:")
    for user, score, data_count in suitable_user_info:
        print(
            f"User ID: {user.profile.get('unique-id')}, Score: {score:.2f}, Data Count: {data_count}, Name: {user.profile.get('first-name')} {user.profile.get('last-name')}")

    for user, score, data_count in suitable_user_info:
        if not user.emotion_model.is_trained:
            # Use only the first 'data_count' physiological data points for training
            limited_data = user.physiological_data[:data_count]
            EmotionAnalysis.train_user_model(user, limited_data)

            # Read test samples for emotion analysis
            test_samples_path = os.path.join("test-user", "user-predictions.txt")
            try:
                test_samples = read_test_samples(test_samples_path)
            except FileNotFoundError:
                print(f"Test samples file not found in path: {test_samples_path}")
                continue
            except json.JSONDecodeError:
                print(f"Error decoding JSON from the test samples file: {test_samples_path}")
                continue

            print(f"\nAnalytics for User ID: {user.profile.get('unique-id')}")
            user.print_statistics()
            test_predictions(user, test_samples)

if __name__ == "__main__":
    directory_path = "sample-users"
    custom_data_limit = 30000
    main(directory_path, custom_data_limit)
