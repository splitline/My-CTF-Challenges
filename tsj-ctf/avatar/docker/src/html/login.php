<?php
require_once('include.php');

if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    if(strlen($_POST['password']) < 8 || strlen($_POST['username']) < 8) {
        die('<script>alert("Username or password is too short (min 8 characters)"); location.href = "/";</script>');
    }

    $result = $fluent->from('users')->select('username, password')->where('username', $_POST['username'])->fetch();

    if ($result === false) {
        // Auto-register
        $fluent->insertInto('users', [
            'username' => $_POST['username'],
            'password' => $_POST['password'],
        ])->execute();
    } else if ($_POST['password'] !== $result['password']) {
        die('<script>alert("Incorrect password"); location.href = "/";</script>');
    }
    $_SESSION['username'] = $_POST['username'];
    header('Location: /');
}
?>
