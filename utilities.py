def format_data(physiological_sample):
    """
    Format the physiological data to be used by the model.

    Args:
        physiological_data (dict): A dictionary containing physiological data.

    Returns:
        list: A list of physiological data values.
    """
    # Extract necessary parameters and convert them into a numeric feature array
    heart_rate = physiological_sample.get('heart-rate-bpm', 0)
    breathing_rate = physiological_sample.get('breathing-rate-breaths-min', 0)
    hrv = physiological_sample.get('hrv-ms', 0)
    skin_temp = physiological_sample.get('skin-temp-c', 0)
    emg = physiological_sample.get('emg-mv', 0)
    bvp = physiological_sample.get('bvp-unit', 0)

    return [heart_rate, breathing_rate, hrv, skin_temp, emg, bvp]

def format_label(emotion_name):
    """
    Map an emotion name to a numerical label.

    Args:
    emotion_name (str): The name of the emotion.

    Returns:
    int: Numerical label corresponding to the emotion.
    """
    # Mapping of emotion names to numerical labels
    emotion_to_label = {
        'Happy': 1,
        'Sad': 2,
        'Anxious': 3,
        'Relaxed': 4,
        'Stressed': 5,
        'Calm': 6,
        'Fearful': 7,
        'Confused': 8,
        'Content': 9,
        'Exhausted': 10,
        'Surprised': 11,
        'Angry': 12,
        'Joyful': 13,
        'Undefined': 0  # Use 0 or another specific number for undefined or other emotions
    }

    return emotion_to_label.get(emotion_name, 0)  # Default to 0 if emotion_name is not in the dictionary

