import numpy as np
from collections import Counter
from sklearn.ensemble import RandomForestClassifier
from utilities import format_label

class UserEmotionModel:
    """
    This class represents a model for emotion prediction for a specific user.
    It uses a Random Forest classifier to predict emotions based on physiological data.
    """
    def __init__(self, user_id, user_conditions):
        super().__init__()
        # Initialize the user model with ID and specific conditions like gender, age, etc.
        self.user_id = user_id
        self.emotion_model = RandomForestClassifier()
        self.is_trained = False
        self.X = None  # Training data features
        self.y = None  # Training data labels
        self.user_conditions = user_conditions  # Conditions like gender, age
        self.emotion_counter = Counter()

    # Example of training model in UserEmotionModel
    def train_model(self, X, y):
        self.X = np.vstack([self.X, X]) if self.X is not None else X
        self.y = np.append(self.y, [format_label(emo) for emo in y]) if self.y is not None else np.array(
            [format_label(emo) for emo in y])
        self.emotion_model.fit(self.X, self.y)
        self.is_trained = True

    def predict_emotion(self, physiological_data):
        if not self.is_trained:
            raise Exception("Model not trained")
        predicted_label = self.emotion_model.predict([physiological_data])[0]
        emotion = self.map_label_to_emotion(predicted_label)
        print(f"Predicted label: {predicted_label}, Emotion: {emotion}")
        return emotion

    def process_feedback(self, physiological_data, actual_emotion_label):
        # Assuming that actual_emotion_label is already in the correct format
        # If not, convert it using format_label or a similar method
        # Update the training data (self.X and self.y) with the new feedback data
        self.X = np.vstack([self.X, physiological_data])
        self.y = np.append(self.y, actual_emotion_label)
        # Retrain the model with the updated data
        self.emotion_model.fit(self.X, self.y)
        self.is_trained = True
        print("Feedback processed and model updated.")

    @staticmethod
    def map_label_to_emotion(label):
        # Map the numerical label to the corresponding emotion
        label_to_emotion = {1: 'Happy', 2: 'Sad', 3: 'Anxious', 4: 'Relaxed', 5: 'Stressed',
                            6: 'Calm', 7: 'Fearful', 8: 'Confused', 9: 'Content', 10: 'Exhausted',
                            11: 'Surprised', 12: 'Angry', 13: 'Joyful', 0: 'Undefined'}  # truncated for brevity
        return label_to_emotion.get(label, 'Undefined')

    @staticmethod
    def format_label(emotion_name):
        # Convert emotion name to a label if necessary
        return emotion_name  # If your model can handle string labels directly, just return the name

    def is_relevant_user(self, other_user_conditions):
        """
        Determine if another user's data is relevant for training this model.
        This can be based on similarity in conditions like age, gender, etc.
        """
        # Example: Check if gender is the same
        return self.user_conditions.get('gender') == other_user_conditions.get('gender')

    def calculate_emotion_statistics(self):
        total_samples = sum(self.emotion_counter.values())
        if total_samples == 0:
            print("No data available for statistics.")
            return

        print("Emotion Statistics:")
        for emotion, count in self.emotion_counter.items():
            percentage = (count / total_samples) * 100
            print(f"{emotion}: {percentage:.2f}%")

    def print_average_emotion_values(self):
        # Check if the model is trained
        if not self.is_trained:
            print("Model not trained. No data available for statistics.")
            return

        # Calculate and print average values for each emotion
        emotion_labels = self.y  # Assuming self.y contains emotion labels
        unique_labels = set(emotion_labels)

        for label in unique_labels:
            indices = [i for i, x in enumerate(emotion_labels) if x == label]
            if indices:
                average_values = np.mean([self.X[i] for i in indices], axis=0)
                print(f"Emotion Label {label}: Average Values: {average_values}")
            else:
                print(f"Emotion Label {label}: No data available")