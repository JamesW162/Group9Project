<?php
session_start();
if (!isset($_SESSION['logged_in']) or $_SESSION['logged_in'] != true) {
    header('Location: login.php');
    exit();
}
?>

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>BSL Bridge Translation</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            text-align: center;
            margin: 0;
            padding: 0;
            background-color: #f9f9f9;
        }
        header {
            background-color: #68a4bc;
            color: white;
            padding: 10px 0;
        }
        header img {
            height: 50px;
        }
        .container {
            margin-top: 50px;
        }
        .loading {
            font-size: 20px;
            font-weight: bold;
            color: #555;
        }
        .progress-bar {
            width: 80%;
            height: 10px;
            background-color: #f3f3f3;
            border-radius: 5px;
            overflow: hidden;
            margin: 50px auto;
        }
        .progress {
            height: 100%;
            width: 0;
            background-color: #68a4bc;
            animation: load 10s ease-in-out infinite;
        }
        .logout_button {
            height: 10%;
            width: 5%;
            float: right;
            margin-right: 2%;

        }
        @keyframes load {
            0% { width: 0; }
            50% { width: 100%; }
            100% { width: 0; }
        }
    </style>
</head>
<body>
    <header>
        <img src="logo.png" alt="Website Logo">
        <a href = "logout.php"><button class = "logout_button">Log Out</button></a>
    </header>
    <div class="progress-bar">
        <div class="progress"></div>
    </div>
    <div class="container">
        <h1 class="loading" id="loadingText">Loading Translation</h1>
    </div>

    <script>
        // Reference the text element and progress bar
        const loadingText = document.getElementById("loadingText");
        const progressBar = document.querySelector(".progress-bar");

        // Add a loading effect
        let dots = "";
        const interval = setInterval(() => {
            dots = dots.length < 3 ? dots + "." : ""; // Cycle through '.', '..', '...'
            loadingText.textContent = `Loading Translation ${dots}`;
        }, 50); // Update every 500ms

        // Simulate loading complete after some time (e.g., 5 seconds)
        setTimeout(() => {
            clearInterval(interval); // Stop the loading animation
            loadingText.textContent = "Sign language text has been loaded!"; // Final content

            // Hide the progress bar
            progressBar.style.display = "none";
        }, 500);

        // This function repeatedly fetches output.txt and replaces the text element with whatever is found
        async function fetchTranslation() {
            try {
                const response = await fetch('output.txt')
                if (response.ok) {
                    const text = await response.text();
                    loadingText.textContent = text;
                }
            } catch (e) {
                loadingText.textContent = "Error fetching translation";
            }
        }
        // repeated every 500. 500 what? idk
        setInterval(fetchTranslation, 500);
    </script>
</body>
</html>
