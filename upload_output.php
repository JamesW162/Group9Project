<?php
if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    $data = $_POST['output'] ?? '';
    file_put_contents("output.txt", htmlspecialchars($data));
    echo "Success";
} else {
    echo "Only POST requests allowed.";
}
?>
