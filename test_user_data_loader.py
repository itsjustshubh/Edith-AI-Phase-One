import unittest
from unittest.mock import patch, MagicMock
from user_data_loader import UserDataLoader
import pandas as pd
from datetime import datetime
from io import BytesIO

class TestUserDataLoader(unittest.TestCase):
    def setUp(self):
        # Example of user profile data as it would be structured in an Excel file
        self.profile_data = {
            'User Profile Aspect': ['Unique ID', 'First Name', 'Last Name', 'Date Of Birth', 'Gender'],
            'Details': ['123456', 'Alex', 'Johnson', '1990-04-15', 'Male']
        }
        self.profile_df = pd.DataFrame(self.profile_data)

        # Example of physiological data as it would be structured in an Excel file
        self.physiological_data = {
            'heart-rate-bpm': [85.3447, 60.7059],
            'breathing-rate-breaths-min': [18.5971, 12.2553],
            'hrv-ms': [58.3913, 62.8153],
            'skin-temp-c': [33.7697, 30.4123],
            'emg-mv': [0.4739, 0.1398],
            'bvp-unit': [0.8963, 0.8710],
            'predicted-emotion': ['Surprised', 'Joyful']
        }
        self.physiological_df = pd.DataFrame(self.physiological_data)

    def test_parse_user_profile(self):
        data_loader = UserDataLoader(None)
        profile = data_loader._parse_user_profile(self.profile_df)

        self.assertIsInstance(profile, dict)
        self.assertEqual(profile['unique-id'], 123456)
        self.assertEqual(profile['first-name'], 'Alex')
        self.assertEqual(profile['last-name'], 'Johnson')

        expected_date_of_birth = '1990-04-15'  # Expected date as a string
        actual_date_of_birth = profile['date-of-birth']
        self.assertEqual(actual_date_of_birth, expected_date_of_birth)

    def test_parse_physiological_data(self):
        # Correctly use self.physiological_df
        data_loader = UserDataLoader(None)
        physiological_entries = data_loader._parse_physiological_data(self.physiological_df)

        self.assertIsInstance(physiological_entries, list)
        self.assertEqual(len(physiological_entries), 2)
        self.assertEqual(physiological_entries[0]['heart-rate-bpm'], 85.3447)
        self.assertEqual(physiological_entries[1]['predicted-emotion'], 'Joyful')

    @patch('os.path.exists', return_value=True)
    @patch('os.listdir', return_value=['user1.xlsx', 'user2.xlsx'])
    def test_load_users_with_valid_files(self, mock_listdir, mock_exists):
        # Test loading of users with valid Excel files
        mock_exists.return_value = True
        mock_listdir.return_value = ['user1.xlsx', 'user2.xlsx']

        with patch('pandas.read_excel') as mock_read_excel:
            mock_read_excel.side_effect = [
                {'user-profile': self.profile_df, 'data': self.physiological_df},
                {'user-profile': self.profile_df, 'data': self.physiological_df}
            ]
            data_loader = UserDataLoader('some/directory')
            users = data_loader.load_users()
            self.assertEqual(len(users), 2)
            # More assertions to check the content of the users...

    @patch('os.path.exists', return_value=False)
    def test_directory_does_not_exist(self, mock_exists):
        # Test when the directory does not exist
        mock_exists.return_value = False
        data_loader = UserDataLoader('non/existent/directory')
        with self.assertRaises(FileNotFoundError):
            data_loader.load_users()

    @patch('os.path.exists', return_value=True)
    @patch('os.listdir', return_value=[])
    def test_no_files_in_directory(self, mock_listdir, mock_exists):
        # Test when the directory is empty
        mock_exists.return_value = True
        mock_listdir.return_value = []
        data_loader = UserDataLoader('empty/directory')
        users = data_loader.load_users()
        self.assertEqual(len(users), 0)

    @patch('os.path.exists', return_value=True)
    @patch('os.listdir', return_value=['user1.xlsx'])
    @patch('pandas.read_excel')
    def test_invalid_excel_file_format(self, mock_read_excel, mock_listdir, mock_exists):
        # Simulate read_excel raising an EmptyDataError
        mock_read_excel.side_effect = pd.errors.EmptyDataError

        data_loader = UserDataLoader('some/directory')
        with self.assertRaises(pd.errors.EmptyDataError):
            data_loader.load_users()

    @patch('os.path.exists', return_value=True)
    @patch('os.listdir', return_value=['user1.xlsx'])
    @patch('pandas.read_excel', return_value={})
    def test_missing_expected_sheets(self, mock_read_excel, mock_listdir, mock_exists):
        # Simulate read_excel returning an empty dict, as if the sheets are missing
        data_loader = UserDataLoader('some/directory')
        users = data_loader.load_users()
        self.assertEqual(len(users), 0)

    # Correct the patch decorators for the following tests
    @patch('os.path.exists', return_value=True)
    @patch('os.listdir', return_value=['user1.xlsx'])
    @patch('pandas.read_excel')
    def test_partial_data_in_profile(self, mock_read_excel, mock_listdir, mock_exists):
        # Test when some user profile data is missing
        # Make sure all arrays are of the same length
        incomplete_profile_data = {
            'User Profile Aspect': ['Unique ID', 'First Name', 'Last Name', 'Date Of Birth'],
            'Details': ['123456', 'Alex', None, None]  # Use None for missing values
        }
        incomplete_profile_df = pd.DataFrame(incomplete_profile_data)

        mock_read_excel.return_value = {
            'user-profile': incomplete_profile_df,
            'data': self.physiological_df
        }

        data_loader = UserDataLoader('some/directory')
        users = data_loader.load_users()
        self.assertEqual(len(users), 1)
        self.assertIn('unique-id', users[0].profile)  # Access profile attribute of User
        self.assertEqual(users[0].profile['unique-id'], 123456)
        self.assertEqual(users[0].profile['first-name'], 'Alex')
        self.assertIn('last-name', users[0].profile)
        self.assertIsNone(users[0].profile['last-name'])  # Use 'last-name'

    @patch('os.path.exists', return_value=True)
    @patch('os.listdir', return_value=['user1.xlsx'])
    @patch('pandas.read_excel')
    def test_missing_data_in_physiological_data(self, mock_read_excel, mock_listdir, mock_exists):
        # Set up the mock to return the correct structure for the DataFrame
        incomplete_physiological_df = pd.DataFrame({
            'heart-rate-bpm': [None, 60.7059],
            'breathing-rate-breaths-min': [18.5971, 12.2553],
            'hrv-ms': [58.3913, 62.8153],
            'skin-temp-c': [33.7697, 30.4123],
            'emg-mv': [0.4739, 0.1398],
            'bvp-unit': [0.8963, 0.8710],
            'predicted-emotion': ['Surprised', 'Joyful']
        })

        # Mock the pandas.read_excel method to return a dictionary with the DataFrame
        mock_read_excel.return_value = {
            'user-profile': self.profile_df,
            'data': incomplete_physiological_df
        }

        data_loader = UserDataLoader('some/directory')
        users = data_loader.load_users()

if __name__ == '__main__':
    unittest.main()
