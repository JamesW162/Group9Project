<?php
session_start();

if (isset($_SESSION['logged_in']) and $_SESSION['logged_in'] == true) {
    header('Location: Webpage.php');
    exit();
}
?>

<form action="authenticate.php" method="POST">
    <h2>Login</h2>
    <input type="text" name="username" placeholder="Username" required>
    <br><br>
    <input type="password" name="password" placeholder="Password" required>
    <br><br>
    <button type="submit">Login</button>
</form>