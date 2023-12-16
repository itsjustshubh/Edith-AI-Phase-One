
## Edith: AI-Driven Personal Wellness and Productivity Enhancement

### Overview

Edith, an innovative project led by Shubh Thorat, is at the forefront of merging emotional and artificial intelligence. Originating from HackHarvard, Edith utilizes physiological data from wearable devices like Apple Watches and Fitbits to interpret human emotions. This cutting-edge development enhances user experience and well-being by leveraging advanced AI techniques for precise emotion analysis.

### Getting Started

#### Prerequisites

Before running Edith, ensure you have the following:
- Python 3.6 or later
- Pip package manager
- Access to physiological data from compatible wearable devices (e.g., Apple Watch, Fitbit)

#### Installation

1. **Clone the Repository**

   To get started with Edith, clone the repository from GitHub:

   \```
   git clone [GitHub Repository URL]
   \```

2. **Install Dependencies**

   Navigate to the project directory and install the required dependencies:

   \```
   cd [Project Directory]
   pip install -r requirements.txt
   \```

   This will install all necessary Python libraries as listed in `requirements.txt`.

#### Setting Up the Test Environment

1. **Update Test User Data**

   - Navigate to the `test-user` folder.
   - Update or add new user profiles and test samples according to your requirements.
   - Ensure the data format aligns with the project's data processing standards.

2. **Test User Data Format**

   The user profile and test samples should be in the following formats:
   - `user-profile.txt`: Contains the demographic and physiological details of the test users.
   - `user-predictions.txt`: Includes the physiological data samples for emotion analysis.

### Running Edith

1. **Execute the Main Script**

   Run `main.py` to start the emotion analysis process:

   \```
   python main.py
   \```

   This script will load the test user data, process it, and run the emotion analysis models.

2. **Viewing Results**

   The results of the emotion analysis will be displayed on the console. This includes the predicted emotional states based on the provided physiological data.

### Understanding the Codebase

- **`emotion_analysis.py`**: Contains the core logic for emotion recognition using physiological data.
- **`user_data_loader.py` and `test_user_data_loader.py`**: Responsible for loading and processing user data.
- **`user_emotion_model.py`**: Defines the model for user emotion analysis.
- **`utilities.py`**: Provides utility functions used across the project.

### Contributions and Development

This project is a continuous collaborative effort. Contributions to improve the algorithm, enhance data processing, or extend the project's capabilities are welcome. Please follow the standard Git workflow for contributions.

### Support and Feedback

For support, feedback, or further information about the project, feel free to reach out through the GitHub repository's Issues and Discussions sections.

---

**Note:** This README is a general guide. Adjust the paths, URLs, and specific instructions according to the actual setup and repository details of the Edith project.
