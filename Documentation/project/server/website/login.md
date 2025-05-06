
# 📄 BSL Bridge - Login Page Documentation

## 🔸 Overview

This login page allows users to sign in using either email/password or a simulated Google login. It includes Firebase integration using **Firebase Realtime Database (v8 SDK)**, and manages session state using `localStorage`.

---

## 🧩 File Structure

The code is a single HTML file structured into the following major sections:

- **Header and Branding**
- **Login Form UI**
- **Firebase Configuration and Initialization**
- **Login Logic**
- **Google Login Simulation**
- **Basic User Session Handling via localStorage**

---

## 🌐 HTML Breakdown

### `<header>`

- Contains logo image (`logoNoBackground.png`) and site title `BSL Bridge`.
- Tagline displayed under the logo: _“TRANSLATING ONE SIGN AT A TIME”_.

### `.login-container`

- Holds the main login `<form>`:
    - Input fields for email and password.
    - Login button.
    - Separator with “or”.
    - Simulated Google sign-in button.
    - Links to "Forgot Password", "Signup", and "Home".

### `<footer>`

- Footer with copyright.

---

## 🎨 CSS Summary

- **Design Theme**: Light background with blue and yellow accents.
- **Form UI**: Card-style centered login form with subtle shadow.
- **Buttons**: Styled with hover effects.
- **Responsiveness**: Centered vertically via flexbox.

---

## 🔌 Firebase Setup

### Firebase SDK Scripts:

```html
<script src="https://www.gstatic.com/firebasejs/8.10.1/firebase-app.js"></script>
<script src="https://www.gstatic.com/firebasejs/8.10.1/firebase-database.js"></script>
```

### Firebase Configuration:

```javascript
const firebaseConfig = {
    apiKey: "...",
    authDomain: "...",
    databaseURL: "...",
    ...
};
firebase.initializeApp(firebaseConfig);
```

> ✅ Note: Only Realtime Database is used. No Firebase Auth SDK.

---

## 🔐 Login Logic

### 1. **Session Check**

```javascript
if (localStorage.getItem('logged_in') === 'true') {
    window.location.href = 'webpage.html';
}
```

### 2. **Hard-Coded Admin Login**

- Admin credentials: `admin@gmail.com` / `1234`.
- On success, logs event, sets localStorage, redirects to main page.

### 3. **Email/Password Login Flow**

- Reads from `plaintext_users` node.
- If credentials match:
    - Logs success.
    - Calls `findUserPIID()` to retrieve `piid` from `plaintext_logs`.
    - Stores `user_email`, `fullname`, `user_id`, and optional `user_piid` in `localStorage`.
- On failure:
    - Logs reason.
    - Displays error message.

### 4. **findUserPIID(email, callback)**

Searches for the user's signup `piid` under `plaintext_logs` matching email.

---

## 🔍 Google Login Simulation

Triggered by the "Sign in with Google" button:

- Logs attempt.
- Queries `plaintext_users` with `provider: google`.
- The actual handling logic appears **incomplete** at the end.

---

## 💾 `localStorage` Keys Used

| Key           | Description                                |
|---------------|--------------------------------------------|
| `logged_in`   | Indicates session state                    |
| `user_email`  | Email of logged-in user                     |
| `fullname`    | Full name (fallback to email)               |
| `is_admin`    | Only set for admin login                   |
| `user_id`     | Firebase key of the user                   |
| `user_piid`   | Unique PIID from signup log                |

---

## 🛡️ Logging (Database Paths)

| Firebase Path           | Purpose                             |
|-------------------------|-------------------------------------|
| `plaintext_logs/`        | Login attempts, successes, fails   |
| `plaintext_users/`       | Registered user accounts           |
| `plaintext_errors/`      | Exception logging during login    |

---

## ⚠️ Notes & Recommendations

- 🔓 **Security Risk**: Passwords and emails are handled in plaintext and stored in Firebase without encryption. Consider using Firebase Auth for secure login.
- 🔧 **Google Login**: The simulation is incomplete (code ends in `if (...`).
- 🧪 **Testing**: Should verify proper login redirection and log entries.
