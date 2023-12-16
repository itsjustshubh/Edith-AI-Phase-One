import numpy as np
from scipy.spatial import distance
from collections import Counter
from user import User

from user_emotion_model import UserEmotionModel
from utilities import format_data, format_label

# Global dictionary for user models
user_models = {}

class Emotion:
    import numpy as np
    from scipy.spatial import distance
    from collections import Counter
    from utilities import format_data, format_label
    from user_emotion_model import UserEmotionModel

    # Global dictionary for user models
    user_models = {}

    def get_user_model(user_id):
        # Retrieve or create a model for a specific user
        if user_id not in user_models:
            user_models[user_id] = UserEmotionModel(user_id)
        return user_models[user_id]

    class Emotion:
        # Class representing different emotions with their physiological values
        # Each method corresponds to a specific emotion
        def __init__(self, name, **kwargs):
            self.name = name
            self.values = kwargs

        @classmethod
        def HAPPY(cls):
            # Based on Greater Good study: Lower heart rate and cortisol levels
            # indicate a calmer cardiovascular state in happiness.
            return cls("Happy", heart_rate=65, breathing_rate=16, hrv=65, skin_temp=32, emg=0.2, bvp=0.8,
                       movement_data={},
                       sleep_duration=8, social_activity={}, voice_features={})

        @classmethod
        def SAD(cls):
            # According to the American Heart Association, sadness (especially when associated with depression)
            # can increase heart rate and cortisol levels, which might affect heart rate variability and other factors.
            return Emotion("Sad", heart_rate=70, breathing_rate=14, hrv=45, skin_temp=31, emg=0.3, bvp=0.7,
                           movement_data={}, sleep_duration=9, social_activity={}, voice_features={})

        @classmethod
        def ANXIOUS(cls):
            # Mayo Clinic notes that anxiety causes an increased heart rate and rapid breathing.
            # This aligns with a heightened fight-or-flight response.
            return Emotion("Anxious", heart_rate=85, breathing_rate=18, hrv=40, skin_temp=31, emg=0.4, bvp=0.9)

        @classmethod
        def CONFUSED(cls):
            # Confusion is marked by an inability to think clearly, leading to disorientation and difficulty in decision-making. It is often associated with a fast pulse rate.
            return Emotion("Confused", heart_rate=75, breathing_rate=17, hrv=50, skin_temp=31, emg=0.3, bvp=0.8)

        @classmethod
        def SURPRISED(cls):
            # Surprises can cause the body to produce excessive stress hormones like adrenaline, leading to narrowed arteries and heart rhythm changes akin to a heart attack.
            return Emotion("Surprised", heart_rate=80, breathing_rate=19, hrv=55, skin_temp=31, emg=0.3, bvp=0.85)

        @classmethod
        def RELAXED(cls):
            # Deep breathing and relaxation techniques have been shown to effectively improve mood and reduce stress. This is often reflected in lower heart rate and cortisol levels.
            return Emotion("Relaxed", heart_rate=55, breathing_rate=12, hrv=70, skin_temp=30, emg=0.1, bvp=0.6)

        @classmethod
        def CALM(cls):
            # Similar to being relaxed, a calm state is likely to be associated with lower heart rate and cortisol levels, reflecting a reduction in stress and an improved mood.
            return Emotion("Calm", heart_rate=60, breathing_rate=14, hrv=65, skin_temp=30, emg=0.2, bvp=0.7)

        @classmethod
        def CONTENT(cls):
            # While specific research on contentment's physiological effects is limited, it can be assumed to be similar to other positive emotions like happiness. This would typically feature lower heart rate and cortisol levels.
            return Emotion("Content", heart_rate=65, breathing_rate=15, hrv=60, skin_temp=30, emg=0.2, bvp=0.7)

        @classmethod
        def STRESSED(cls):
            # Stressed: Increased cortisol, adrenaline, heart rate, respiration rate.
            # Notable biomarkers: cortisol, ACTH, BDNF, catecholamines, etc.
            return cls("Stressed", heart_rate=90, breathing_rate=20, hrv=40, skin_temp=33, emg=0.5, bvp=1.0)

        @classmethod
        def FEARFUL(cls):
            # Fearful: Fight-or-flight response, increased heart rate, blood pressure, skin conductance.
            return cls("Fearful", heart_rate=100, breathing_rate=22, hrv=35, skin_temp=34, emg=0.6, bvp=1.1)

        @classmethod
        def EXHAUSTED(cls):
            # Exhausted: Linked with muscle fatigue, can lead to chronic fatigue syndrome.
            # Common in strenuous activities and prolonged focus (like videoconferencing).
            return cls("Exhausted", heart_rate=70, breathing_rate=16, hrv=48, skin_temp=32, emg=0.4, bvp=0.9)

        @classmethod
        def ANGRY(cls):
            # Angry: Increased heart rate, blood pressure, muscle tension, adrenaline release.
            return cls("Angry", heart_rate=95, breathing_rate=21, hrv=42, skin_temp=33, emg=0.5, bvp=1.0)

        @classmethod
        def JOYFUL(cls):
            # Joyful: Affects circulatory system; involves dopamine, serotonin, norepinephrine, endorphin.
            return cls("Joyful", heart_rate=68, breathing_rate=16, hrv=62, skin_temp=30, emg=0.25, bvp=0.75)

        @classmethod
        def UNDEFINED(cls):
            # Undefined: Represents a state with no clearly identifiable emotional characteristics.
            # Default values can be set to represent a neutral or baseline state.
            return cls("Undefined", heart_rate=0, breathing_rate=0, hrv=0, skin_temp=0, emg=0, bvp=0)

        @classmethod
        def _find_closest_emotion_generic(cls, physiological_data, k=3):
            # Find the closest emotion for generic users
            emotions = [cls.HAPPY(), cls.SAD(), cls.ANXIOUS(), cls.RELAXED(), cls.STRESSED(),
                        cls.CALM(), cls.FEARFUL(), cls.CONFUSED(), cls.CONTENT(), cls.EXHAUSTED(),
                        cls.SURPRISED(), cls.ANGRY(), cls.JOYFUL()]

            # Extract the first row of physiological_data as it's a 2D array with shape (1, -1)
            physiological_data_row = physiological_data[0]

            heart_rate, breathing_rate, hrv, skin_temp, emg, bvp = physiological_data_row

            normalized_input = [
                heart_rate / 120,  # Max heart rate
                breathing_rate / 25,  # Max breathing rate
                hrv / 120,  # Max HRV
                skin_temp / 37,  # Normal skin temp
                emg / 1,  # Max EMG
                bvp / 2  # Max BVP
            ]

            emotion_distances = []
            for e in emotions:
                emotion_values = [
                    e.values.get('heart_rate', 0) / 100,
                    e.values.get('breathing_rate', 0) / 30,
                    e.values.get('hrv', 0) / 100,
                    e.values.get('skin_temp', 0) / 40,
                    e.values.get('emg', 0) / 1,
                    e.values.get('bvp', 0) / 1.5
                ]
                dist = distance.euclidean(normalized_input, emotion_values)
                emotion_distances.append((e, dist))

            k_nearest_emotions = sorted(emotion_distances, key=lambda x: x[1])[:k]
            most_common_emotion = Counter([e[0].name for e in k_nearest_emotions]).most_common(1)[0][0]
            closest_emotion = next(e[0] for e in k_nearest_emotions if e[0].name == most_common_emotion)

            # Modify the return statement to return the name of the closest emotion
            return closest_emotion.name

        @classmethod
        def update_user_model(cls, user_model, physiological_data_list, reported_emotions):
            # user_model is an instance of UserEmotionModel passed as a parameter
            X = np.vstack([format_data(d) for d in physiological_data_list])
            y = np.array([format_label(e) for e in reported_emotions])

            user_model.train_model(X, y)
            print(f"Updated the model for user: {user_model.user_id}")

        @staticmethod
        def find_closest_emotion(user_id, physiological_data):
            if isinstance(physiological_data, dict):
                formatted_data = format_data(physiological_data)
            else:
                formatted_data = physiological_data  # Already formatted

            if user_id in user_models and user_models[user_id].is_trained:
                predicted_label = user_models[user_id].predict_emotion(formatted_data)
                return Emotion.map_label_to_emotion(predicted_label)
            else:
                return Emotion._find_closest_emotion_generic(formatted_data)

        def __str__(self):
            emotion_str = f"Emotion: {self.name}, Values: {self.values}\n"
            if hasattr(self, 'distance'):
                emotion_str += f"Distance: {self.distance}\n"
            return emotion_str

    # Example user conditions and model initialization
    user_conditions = {
        'user123': {'gender': 'male', 'age': 30},
        'user456': {'gender': 'female', 'age': 25}
    }

    # Initialize models for each user
    for user_id, conditions in user_conditions.items():
        user_models[user_id] = UserEmotionModel(user_id, conditions)

# Example user conditions and model initialization
user_conditions = {
    'user123': {'gender': 'male', 'age': 30},
    'user456': {'gender': 'female', 'age': 25}
}

# Initialize models for each user
for user_id, conditions in user_conditions.items():
    user_models[user_id] = UserEmotionModel(user_id, conditions)