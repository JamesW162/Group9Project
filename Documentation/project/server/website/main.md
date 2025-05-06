# BSL Bridge Main Page Explanation

This file contains the code for the main landing page of the BSL Bridge application, which showcases the project's mission, features, and social impact related to British Sign Language translation.

## Key Components

### 1. Header & Navigation

The page features a prominent header with the project logo and navigation menu:

```html
<header>
    <div class="container">
        <div class="logo">
            <img src="logoNoBackground.png" alt="BSL Bridge Logo"> 
            <h1>BSL Bridge</h1>
        </div>
        <p class="tagline">TRANSLATING ONE SIGN AT A TIME</p>
        <div class="login-status">
            <span id="username-display"></span>
            <button id="translate-btn" class="btn" style="display: none;">Translate</button>
            <button id="logout-btn" class="btn" style="display: none;">Logout</button>
            <button id="login-btn" class="btn">Login</button>
            <button id="signup-btn" class="btn">Sign Up</button>
        </div>
    </div>
</header>
```

### 2. Hero Section with Video Background

A visually engaging hero section introduces the project with a video background:

```html
<div class="hero">
    <div class="hero-video-container">
        <video class="hero-video" autoplay loop muted>
            <source src="video.mp4" type="video/mp4">
            Your browser does not support the video tag.
        </video>
    </div>
    <div class="video-overlay"></div>
    <div class="container">
        <h2>British Sign Language Translator</h2>
        <p>Bridging communication gaps with innovative technology to empower the deaf and hard of hearing community</p>
        <button class="btn"><a href="#project" style="text-decoration: none;">Learn More</a></button>
    </div>
</div>
```

### 3. Project Mission

An overview of the project's mission and impact:

```html
<div class="card">
    <h3>Our Mission</h3>
    <p>At BSL Bridge, we believe communication is a fundamental human right. Our innovative technology bridges the gap between the deaf community and the hearing world, fostering understanding, inclusion, and equal access to opportunities.</p>
    <p><strong>Impact Statistics:</strong></p> 
    <ul>
        <li>Over 430 million people worldwide experience disabling hearing loss</li>
        <li>BSL has been recognized as an official language in the UK since 2003</li>
        <li>Our solution provides a 16:1 return on social investment over 10 years</li>
        <li>87% of deaf people report improved quality of life with accessible communication tools</li>
    </ul>   
</div>
```

### 4. Problem Statement

A clear explanation of the challenges faced by the deaf community:

```html
<div class="architecture" id="architecture">
    <h3>THE CHALLENGE</h3>
    <p>For millions of deaf individuals, everyday interactions present significant challenges. Communication barriers lead to:</p>
    <ul>
        <li><b>Educational Barriers:</b> Deaf students experience 30% lower graduation rates in settings without proper support systems</li>
        <li><b>Workplace Limitations:</b> Qualified deaf professionals face a 42% higher unemployment rate despite equal qualifications</li>
        <li><b>Social Isolation:</b> 7 in 10 deaf individuals report feelings of exclusion in group settings and public events</li>
        <li><b>Healthcare Disparities:</b> 63% of medical settings lack proper interpretation services, leading to compromised care</li>
    </ul>  
    <p>Over <b>24%</b> of young people are at risk of hearing loss due to unsafe noise exposure, making accessible communication solutions more critical than ever for future generations.</p>
</div>
```

### 5. Solution Overview

A description of how the BSL Bridge product works:

```html
<div class="data-flow" id="dataflow">
    <h3>OUR SOLUTION</h3>
    <p>The BSL Bridge is an innovative IoT device that captures sign language gestures through a camera and translates them into text in real-time. By providing an affordable, portable alternative to human interpreters, we're making communication accessible in classrooms, workplaces, healthcare settings, and beyond.</p>
    <p><strong>How It Works:</strong></p>
    <ol>
        <li><b>Capture:</b> Our precision camera captures hand gestures in real-time</li>
        <li><b>Analysis:</b> Advanced machine learning algorithms interpret the signs using a comprehensive database of BSL patterns</li>
        <li><b>Translation:</b> The system converts signs into corresponding text, displayed on a webpage</li>
        <li><b>Integration:</b> Portable design allows seamless use throughout daily activities</li>
    </ol>
</div>
```

### 6. Features Section

A grid layout showcasing the main features of the product:

```html
<h2 class="section-title" id="features">FEATURES</h2>
<div class="features">
    <div class="feature-card">
        <img src="raspberrpiCamera.png" alt="Camera Feature">
        <h3>CAMERA</h3>
        <ul>
            <li>Real-time processing</li>
            <li>Hand motion trajectory analysis</li>
        </ul>
    </div>
    
    <!-- Additional feature cards -->
</div>
```

### 7. Social Impact Section

A detailed look at how the product impacts different sectors:

```html
<h2 class="section-title" id="impacts">SOCIAL IMPACT</h2>
<div class="impacts">
    <div class="impact-card">
        <h3>EDUCATION</h3>
        <ul>
            <li>Improvement in classroom participation</li>
            <li>Enhances learning experiences</li>
            <li>Supports inclusive teaching</li>
            <li>Increases academic achievement</li>
            <li>Enables peer interaction</li>
        </ul>
    </div>
    
    <!-- Additional impact cards -->
</div>
```

### 8. Login & Authentication Management

JavaScript code manages user authentication and displays personalized elements:

```javascript
// Check login status
window.onload = function() {
    if (localStorage.getItem('logged_in') === 'true') {
        document.getElementById('username-display').textContent = 'Welcome, ' + (localStorage.getItem('username') || 'User');
        document.getElementById('logout-btn').style.display = 'inline-block';
        document.getElementById('translate-btn').style.display = 'inline-block'; // Show translate button
        document.getElementById('login-btn').style.display = 'none';
        document.getElementById('signup-btn').style.display = 'none';
    }
};
```

### 9. Navigation Controls

Event listeners handle button clicks for user navigation:

```javascript
// Login button redirect
document.getElementById('login-btn').addEventListener('click', function() {
    window.location.href = 'login.html';
});

// Signup button redirect
document.getElementById('signup-btn').addEventListener('click', function() {
    window.location.href = 'signup.html';
});

// Translate button redirect
document.getElementById('translate-btn').addEventListener('click', function() {
    window.location.href = 'webpage.html';
});
```

### 10. Responsive Design

The page includes CSS media queries to ensure proper display on different devices:

```css
@media (max-width: 768px) {
    .grid, .features, .impacts {
        grid-template-columns: 1fr;
    }
    
    .login-status {
        position: static;
        margin-top: 15px;
        text-align: center;
    }
    
    .hero {
        height: 400px;
    }
    
    .hero h2 {
        font-size: 2rem;
    }
    
    .hero p {
        font-size: 1.1rem;
    }
}
```

### 11. Visual Styling and Animation

The page includes numerous visual enhancements for user engagement:

```css
.card:hover {
    transform: translateY(-5px);
    box-shadow: 0 8px 16px rgba(0,0,0,0.15);
}

.section-title::after {
    content: "";
    display: block;
    width: 80px;
    height: 3px;
    background-color: #ffcc00;
    margin: 15px auto 0;
}
```