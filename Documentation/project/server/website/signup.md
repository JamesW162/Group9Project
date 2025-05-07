# signup.html documentation

## File Overview

The file creates a user registration page for BSL Bridge with the following features:
- Clean, responsive design with a blue color scheme
- Account creation form with field validation
- Google sign-up option
- Firebase database integration

## HTML Structure

### Header Section
```html
<header>
    <div class="logo">
        <img src="logoNoBackground.png" alt="BSL Bridge Logo"> 
        <h1>BSL Bridge</h1>
    </div>
    <p class="tagline">TRANSLATING ONE SIGN AT A TIME</p>
</header>
```
The header displays the BSL Bridge logo, name, and tagline "TRANSLATING ONE SIGN AT A TIME" at the top of the page.

### Sign-Up Form
```html
<form id="signup-form">
    <h2>Create an Account</h2>
    <input type="text" id="fullname" placeholder="Full Name" required>
    <input type="email" id="email" placeholder="Email" required>
    <input type="password" id="password" placeholder="Password" required>
    <input type="password" id="confirm-password" placeholder="Confirm Password" required>
    <input type="text" id="piid" placeholder="Device ID (on side container)" required>

    <div class="checkbox-container">
        <input type="checkbox" id="terms" required>
        <label for="terms">I agree to the Terms and Conditions</label>
    </div>
    
    <button type="submit" id="signup-button">Sign Up</button>
    <!-- Additional elements -->
</form>
```
The form collects user information including name, email, password, and a "Device ID" which suggests hardware integration with the service.

### Alternative Sign-Up Method
```html
<div class="separator">
    <span>or</span>
</div>

<button type="button" id="google-signup" class="social-button">
    <img src="https://cdn.cdnlogo.com/logos/g/35/google-icon.svg" alt="Google">
    Sign up with Google
</button>
```
Offers Google sign-up as an alternative registration method.

## JavaScript Functionality

### Firebase Initialization
```javascript
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

// Initialize Firebase
firebase.initializeApp(firebaseConfig);
```
Initializes Firebase with configuration details for database integration.

### Form Submission Handler
```javascript
document.getElementById('signup-form').addEventListener('submit', function(e) {
    e.preventDefault();
    
    const fullname = document.getElementById('fullname').value;
    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;
    const confirmPassword = document.getElementById('confirm-password').value;
    const statusMessage = document.getElementById('status-message');
    const signupButton = document.getElementById('signup-button');
    const piid = document.getElementById('piid').value;

    // Basic validation
    if (password !== confirmPassword) {
        statusMessage.textContent = 'Passwords do not match!';
        statusMessage.className = 'error';
        return;
    }
    
    // Generate a random ID for the user
    const userId = 'user_' + Math.random().toString(36).substr(2, 9);
```
Handles form submission by:
1. Preventing default form submission
2. Collecting form values
3. Validating password match
4. Generating a random user ID

### User Data Storage
```javascript
firebase.database().ref('plaintext_users/' + userId).set({
    fullname: fullname,
    email: email,
    password: password, // Storing password as plain text as requested
    piid: piid,
    timestamp: new Date().toISOString()
})
```
Stores user data in Firebase Realtime Database with passwords in plain text (a significant security issue).

### Success Handling
```javascript
// Show success message
statusMessage.textContent = 'Account created successfully! Redirecting...';
statusMessage.className = 'success';

// Store user info in localStorage for convenience
localStorage.setItem('logged_in', 'true');
localStorage.setItem('email', email);
localStorage.setItem('fullname', fullname);
localStorage.setItem('user_id', userId);
localStorage.setItem('pi_id', piid);

// Redirect to main page after a short delay
setTimeout(function() {
    window.location.href = 'webpage.html';
}, 1500);
```
After successful registration:
1. Displays success message
2. Stores user information in browser's localStorage
3. Redirects to the main page after 1.5 seconds

### Google Sign-Up Simulation
```javascript
document.getElementById('google-signup').addEventListener('click', function() {
    // Generate a random ID and fake Google user data
    const userId = 'google_user_' + Math.random().toString(36).substr(2, 9);
    const randomName = 'Google User ' + Math.floor(Math.random() * 1000);
    const randomEmail = 'google_user_' + Math.floor(Math.random() * 1000) + '@gmail.com';
```
The Google sign-up button doesn't actually implement OAuth but instead:
1. Creates mock user data with random name and email
2. Stores this data in Firebase
3. Simulates a successful Google sign-up