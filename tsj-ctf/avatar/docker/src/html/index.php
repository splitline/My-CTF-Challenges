<?php require_once('include.php'); ?>
<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="utf-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Avatar</title>
    <link rel="stylesheet" type="text/css" href="/static/style.css">
</head>

<body>
    <h1>Upload your avatar</h1>
    <hr>
    <br>
    <?php if (!isset($_SESSION['username'])) : ?>
        <h2>Login / Register</h2>
        <form action="/login.php" method="POST">
            <p>
                <label for="username">Username: </label>
                <input type="text" name="username" id="username" minlength="8">
            </p>
            <p>
                <label for="password">Password: </label>
                <input type="password" name="password" id="password" minlength="8">
            </p>
            <input type="submit" value="Sign in">
        </form>
    <?php else : ?>
        <?php $user = $fluent->from('users')->where('username', $_SESSION['username'])->fetch() ?>

        <h2>Hello @<?= $user['username'] ?>, here is your avatar:</h2>
        
        <div class="container">
            <img class="avatar" src="<?= $user['avatar'] ? "data:image/png;base64," . base64_encode($user['avatar']) : '/static/images/default.jpeg' ?>" alt="avatar">
        </div>
        <h3>Update Avatar</h3>
        <p>Please upload an image less than 64 kb.</p>

        <div>
            <nav>
                <a href="#file">Upload via file</a>
                <a href="#url">Upload via URL</a>
            </nav>

            <div id="file" class="content">
                <form enctype="multipart/form-data" action="/update.php?mode=file" method="POST">
                    <p>
                        <input type="file" name="avatar_file">
                        <input type="submit" value="Upload">
                    </p>
                </form>
            </div>

            <div id="url" class="content">
                <form action="/update.php?mode=url" method="POST">
                    <p>
                        <input type="url" name="url" placeholder="http(s)://example.com/avatar.png">
                        <input type="submit" value="Upload">
                    </p>
                </form>
            </div>
        </div>
    <?php endif; ?>
</body>

</html>