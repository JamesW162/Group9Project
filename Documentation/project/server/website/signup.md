# signup.html documentation

## Features

- **User Registration**: Users can create an account by entering their full name, email, password, and device ID (PIID).
- **Password Validation**: The system checks that the password and confirmation match before proceeding.
- **Firebase Database Integration**: User data is stored in Firebase Realtime Database, including the email, full name, password (plaintext), and device ID.
- **Google Sign-Up Simulation**: A mock sign-up using Google credentials stores random user data for demonstration purposes.
- **User Feedback**: Status messages are displayed after form submission, indicating success or failure.
- **Redirect After Success**: After successfully creating an account, users are redirected to the main page of the platform.

## Getting Started

### Prerequisites

- An active Firebase account.
- Firebase Realtime Database setup.
- Basic knowledge of HTML, CSS, and JavaScript.

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/bsl-bridge-signup.git
Open the index.html file in your browser.

Set up Firebase:

Replace the Firebase configuration in the script with your own Firebase project details.

Example:

const firebaseConfig = {
    apiKey: "your-api-key",
    authDomain: "your-auth-domain",
    databaseURL: "your-database-url",
    projectId: "your-project-id",
    storageBucket: "your-storage-bucket",
    messagingSenderId: "your-sender-id",
    appId: "your-app-id",
    measurementId: "your-measurement-id"
};
File Structure

bsl-bridge-signup/
│
├── index.html       # Main sign-up page with the form
├── logoNoBackground.png # Logo for the platform (optional)
└── README.md        # Project documentation (this file)
Technologies Used
HTML: Structure of the sign-up page.

CSS: Styling the form and layout.

JavaScript: Handling form submission, form validation, and Firebase interaction.

Firebase: For storing user data and handling event logging.

How to Use
Sign Up Form:

Users must fill out their full name, email, password, confirm the password, and device ID.

If the password and confirmation don't match, an error message will display.

Users must agree to the terms and conditions to submit the form.

Google Sign-Up:

Clicking on the "Sign up with Google" button simulates a Google-based sign-up and stores random user data for demonstration.

Account Creation:

Upon successful submission, the account is created, and the user is redirected to the main page after a short delay.

Firebase Configuration
javascript

const firebaseConfig = {
    apiKey: "AIzaSyAEzhS9bkzcN5-YLuvta9Vm2aYM6DYl2PU",
    authDomain: "bsltranslator-93f00.firebaseapp.com",
    databaseURL: "https://bsltranslator-93f00-default-rtdb.europe-west1.firebasedatabase.app",
    projectId: "bsltranslator-93f00",
    storageBucket: "bsltranslator-93f00.appspot.com",
    messagingSenderId: "547548973040",
    appId: "1:547548973040:web:4c7b2802aedcf6e84a7f35",
    measurementId: "G-9T2S36E0LJ"
};
Make sure to replace the firebaseConfig details with your own Firebase project credentials.

Security Warning
Important: The app stores passwords as plain text, which is not recommended for production environments. Firebase Authentication should be used for secure user management.

Contribution
Feel free to fork the repository and submit pull requests. Ensure that any changes comply with the project's coding style and structure.

License
This project is licensed under the MIT License - see the LICENSE file for details.
"""

Saving the README content to a file
file_path = "/mnt/data/bsl_bridge_signup_README.md"
with open(file_path, "w") as file:
file.write(readme_content)

file_path
