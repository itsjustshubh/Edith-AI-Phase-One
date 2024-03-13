from user import User
import json
import sqlite3
import os
import pandas as pd

class UserDataLoader:
    def __init__(self, directory_path, update_progress=None, db_path=None):
        self.directory_path = directory_path
        self.update_progress = update_progress
        self.db_path = db_path

    def connect_db(self):
        return sqlite3.connect(self.db_path)

    def load_users(self):
        if not os.path.exists(self.directory_path):
            raise FileNotFoundError(f"Directory '{self.directory_path}' does not exist.")

        users = []
        self.update_progress("Loading User Data from Files", {"file": "user_data_loader.py", "function": "load_users"})
        for filename in os.listdir(self.directory_path):
            if filename.endswith('.xlsx'):
                user_data = pd.read_excel(os.path.join(self.directory_path, filename), sheet_name=None)
                user_profile_sheet = user_data.get('user-profile')
                data_sheet = user_data.get('data')

                if user_profile_sheet is None or data_sheet is None:
                    self.update_progress(f"Skipping file due to missing data: {filename}")
                    continue  # Skip if required data is missing

                user_profile = self._parse_user_profile(user_profile_sheet)
                physiological_data = self._parse_physiological_data(data_sheet)
                users.append(User(user_profile, physiological_data))  # Create User instance
                self.update_progress(f"Processing file: {filename}",
                                     {"file": "user_data_loader.py", "function": "load_users",
                                      "user": f"{user_profile.get('first-name')} {user_profile.get('last-name')}",
                                      "nationality": f"{user_profile.get('nationality')}",
                                      "data_points": f"{len(physiological_data)}",
                                      })

        if not users:
            self.update_progress(f"No user data files found in '{self.directory_path}'.")
            return []

        self.update_progress("User Data Loaded Successfully", {"file": "user_data_loader.py", "function": "load_users", "users": f"{len(users)}"})
        return users

    def _parse_user_profile(self, profile_df):
        profile_data = {}
        for _, row in profile_df.iterrows():
            key = row['User Profile Aspect'].lower().replace(' ', '-')
            value = row['Details']
            if key in ['unique-id'] and pd.notna(value):
                value = int(value)  # Ensure this matches your test data type expectation
            else:
                value = value if pd.notna(value) else None
            profile_data[key] = value
        return profile_data

    def _parse_physiological_data(self, data_df):
        data_entries = []
        for _, row in data_df.iterrows():
            if row.notnull().any():
                entry = {col: row[col] for col in data_df.columns if pd.notna(row[col])}
                data_entries.append(entry)
        return data_entries

    def save_feedback(self, user_id, feedback):
        conn = self.connect_db()
        cursor = conn.cursor()

        # Assuming feedback is a tuple of physiological_data and emotion
        cursor.execute("INSERT INTO feedback (user_id, physiological_data, emotion) VALUES (?, ?, ?)",
                       (user_id, str(feedback[0]), feedback[1]))
        conn.commit()
        conn.close()

    # Add a function to load users from the database
    def load_users_from_db(self):
        conn = self.connect_db()
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM users")
        users_data = cursor.fetchall()

        users = []
        for user_row in users_data:
            user_id, user_profile_json, physiological_data_json = user_row
            # Assuming user_profile and physiological_data are stored as JSON strings
            user_profile = json.loads(user_profile_json)
            physiological_data = json.loads(physiological_data_json)
            users.append(User(user_profile, physiological_data))

        conn.close()
        return users