<?php
require_once('include.php');

// Login required
if (!isset($_SESSION['username'])) {
    die('<script>alert("You need to login first"); location.href = "/";</script>');
}

if ($_GET['mode'] === 'url') {
    $url = filter_var($_POST['url'], FILTER_VALIDATE_URL);

    if (!preg_match('/^(http:\/\/|https:\/\/)/i', $url)) {
        die('Invalid URL');
    }

    $parsed_url = parse_url($url);

    $ip = gethostbyname($parsed_url['host']);
    if (!filter_var($ip, FILTER_VALIDATE_IP, FILTER_FLAG_IPV4 | FILTER_FLAG_NO_PRIV_RANGE | FILTER_FLAG_NO_RES_RANGE)) {
        die('Invalid URL');
    }

    $image_type = pathinfo(urldecode($parsed_url['path']), PATHINFO_EXTENSION) ?? 'png';
    $image = file_get_contents($url, false, stream_context_create([
        'http' => ['header' => [
            "Accept: image/$image_type",
            "User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36",
        ]]
    ]));

    if ($image === false) die('Failed to fetch image');
} else if ($_GET['mode'] === 'file') {
    if (!isset($_FILES['avatar_file'])) die('No file');
    $image = file_get_contents($_FILES['avatar_file']['tmp_name']);
} else {
    die('Invalid mode');
}

// image should less than 64kb
if (strlen($image) >= 64000) die('Image is too large');
$fluent->update('users')->set(['avatar' => $image])->where('username', $_SESSION['username'])->execute();

header('Location: /');
