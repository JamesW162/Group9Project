<?php
session_start();
$valid_username = "admin";
$valid_password = "1234";

$username = $_POST['username'] ?? '';
$password = $_POST['password'] ?? '';

if ($username === $valid_username && $password === $valid_password) {
    $_SESSION['logged_in'] = true;
    header("Location: Webpage.php");
    exit();
} else {
    echo "Invalid login. <a href='login.php'>Try again</a>";
}
?>