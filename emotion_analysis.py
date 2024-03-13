from user_emotion_model import UserEmotionModel
from emotion import user_models
from utilities import format_data, format_label

class EmotionAnalysis:
    @staticmethod
    def train_initial_model(user_id, X_train, y_train):
        # Train the initial model for a specific user
        if user_id not in user_models:
            raise Exception(f"User model for {user_id} not found. Available IDs: {list(user_models.keys())}")
        user_models[user_id].train_model(X_train, y_train)

    @staticmethod
    def train_user_model(user, limited_data=None, update_progress=None):
        update_progress("Training Custom User Model", {"file": "main.py", "function": "train_user_model"})
        if limited_data is None:
            limited_data = user.physiological_data

        x_train = [format_data(sample) for sample in limited_data]
        y_train = [sample.get('predicted-emotion', 'Undefined') for sample in limited_data]

        update_progress("Training Emotion Model", {"x_train": f'{len(x_train)}', "y_train": f'{len(y_train)}'})
        user.train_emotion_model(x_train, y_train)

    @staticmethod
    def make_predictions_for_user(user, physiological_data_samples):
        predictions = []
        for sample in physiological_data_samples:
            formatted_sample = format_data(sample)
            predicted_emotion = user.predict_emotion(formatted_sample)
            predictions.append(predicted_emotion)

        return predictions

    @staticmethod
    def make_predictions(user_id, physiological_data_samples):
        # Make predictions for a specific user
        if user_id not in user_models or not user_models[user_id].is_trained:
            raise Exception(f"User model for {user_id} not initialized or not trained.")
        predictions = []
        for sample in physiological_data_samples:
            formatted_sample = format_data(sample)
            predicted_emotion = user_models[user_id].predict_emotion(formatted_sample)
            predictions.append(predicted_emotion)
        return predictions

    @staticmethod
    def process_feedback(user_id, feedback_list):
        # Process feedback for a specific user
        if user_id not in user_models:
            raise Exception(f"User model for {user_id} not initialized.")
        for feedback_item in feedback_list:
            sample, actual_emotion, *multiplier = feedback_item
            multiplier = multiplier[0] if multiplier else 1
            formatted_sample = format_data(sample)
            user_models[user_id].provide_feedback(formatted_sample, actual_emotion, multiplier)