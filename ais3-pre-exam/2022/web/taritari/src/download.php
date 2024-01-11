<?php
if ($_SERVER['REQUEST_METHOD'] == 'GET' && isset($_GET['file'])) {
    $file = base64_decode($_GET['file']);
    $path = "./files/$file";
    $name = $_GET['name'] ?? basename($file);
    if (!file_exists($path)) {
        echo "File not found";
    } else {
        header("Content-Type: application/zip");
        header("Content-Disposition: attachment; filename=$name");
        readfile($path);
        unlink($path);
    }
}
