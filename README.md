
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

   \```bash
   git clone [GitHub Repository URL]
   \```

2. **Install Dependencies**

   Navigate to the project directory and install the required dependencies:

   \```bash
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

   \```bash
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

### Further Readings

For those interested in learning more about the project's backstory, its development process, and additional features, the following resources provide detailed insights:

- **Khoury College of Computer Sciences Article**: An in-depth look at the inspiration and development of Edith, focusing on how it aims to reduce stress through AI-powered scheduling. [Read more](https://www.khoury.northeastern.edu/meet-edith-the-ai-powered-schedule-assistant-designed-to-reduce-your-stress/).
- **Personal Project Page**: My personal page dedicated to Edith, offering an overview of the project, its objectives, and the technology behind it. [Explore here](https://www.shubhthorat.com/edith).
- **Devpost Software Profile**: A comprehensive description of Edith on Devpost, detailing its features, the technology stack used, and the challenges addressed during development. [Discover more](https://devpost.com/software/edith-brshpa).

As I look to the future, I am committed to continuously evolving Edith, ensuring that it remains at the forefront of AI and user experience design. The journey of Edith is far from over; it is an ongoing process of learning, adapting, and innovating to meet the ever-changing needs of users in the dynamic landscape of technology and AI.

**Note:** This README is a general guide. Adjust the paths, URLs, and specific instructions according to the actual setup and repository details of the Edith project.
