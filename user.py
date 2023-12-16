from user_emotion_model import UserEmotionModel
import numpy as np
from collections import Counter

class User:
    def __init__(self, user_profile, physiological_data):
        self.profile = user_profile
        self.physiological_data = physiological_data
        self.emotion_model = UserEmotionModel(user_profile['unique-id'], user_profile)

    def train_emotion_model(self, X, y):
        self.emotion_model.train_model(X, y)

    def predict_emotion(self, physiological_data):
        return self.emotion_model.predict_emotion(physiological_data)

    def __str__(self):
        return f"User: {self.profile}\nPhysiological Data: {self.physiological_data}"

    def print_statistics(self):
        # Implement statistics calculation and printing here
        # Example:
        emotions_counter = Counter(self.emotion_model.y)
        total = sum(emotions_counter.values())
        print("\nEmotion Statistics:")
        for emotion, count in emotions_counter.items():
            print(f"{emotion}: {count / total * 100:.2f}%")

        # Print average values for each emotion
        print("\nAverage Values for Each Emotion:")
        for label in set(self.emotion_model.y):
            indices = [i for i, y in enumerate(self.emotion_model.y) if y == label]
            if indices:
                average_values = np.mean([self.emotion_model.X[i] for i in indices], axis=0)
                print(f"Emotion {label}: {average_values}")
