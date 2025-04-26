<?php
session_start();
if (!isset($_SESSION['logged_in']) || $_SESSION['logged_in'] !== true) {
    header('Location: login.php');
    exit();
}
if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    $data = $_POST['output'] ?? '';
    file_put_contents("output.txt", htmlspecialchars($data));
    echo "Success";
} else {
    echo "Only POST requests allowed.";
}
?>
