<?php
session_start();
ini_set("file-uploads", 1);
isset($_GET['8']) && ($_GET['8'] === '===D') && exit(!show_source(__FILE__));

if (!isset($_SESSION['dir'])) {
    $dir = 'sandbox/' . bin2hex(random_bytes(16));
    $_SESSION['dir'] = $dir;
} else {
    $dir = $_SESSION['dir'];
}
if (!file_exists($dir)) mkdir($dir);
chdir($dir);
?>
<!DOCTYPE html>
<html>

<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>WTF</title>
    <link rel="stylesheet" href="bootstrap.min.css">
</head>

<body>
    <div class="container">
        <h1 class="page-header">
            <span style="color:#ff5a00">W</span><span style="color:#ffb400">h</span><span style="color:#f0ff00">a</span><span style="color:#96ff00">t</span><span style="color: transparent;text-shadow: none;">&nbsp;</span><span style="color:#00ff1e">t</span><span style="color:#00ff78">h</span><span style="color:#00ffd2">e</span>
            <blink><span style="color:#0078ff">F</span><span style="color:#001eff">i</span><span style="color:#3c00ff">l</span><span style="color:#9600ff">e</span><span style="color:#f000ff">?</span><span style="color:#ff00b4">!</span><span style="color:#ff005a">?</span><span style="color:#ff0000">!</span></blink>
            <img src="/img/hot.gif">
        </h1>
        <marquee scrolldelay="10">
            I can determine your file's file type for you owo!
        </marquee>
        <table cellspacing="2" cellpadding="2">
            <tbody>
                <tr>
                    <td><img src="/img/ie_logo.gif"></td>
                    <td><img src="/img/ns_logo.gif"></td>
                    <td><img src="/img/noframes.gif"></td>
                    <td><img src="/img/notepad.gif"></td>
                </tr>
            </tbody>
        </table>
        <center>
            <a href="/?8====D"><img src="/img/click.gif" width="150"></a>
        <br>
        <br>
            <img src="/img/divider.gif">
        </center>
        <br>
        <form method="POST" class="form-horizontal well" enctype="multipart/form-data">
            <div class="control-group">
                <label class="control-label" for="file">File to file (?)</label>
                <div class="controls">
                    <input type="file" name="file" id="file">
                </div>
            </div>
            <div class="control-group text-center">
                <button class="btn btn-primary">file me UwU</button>
                <button type="reset" class="btn">Cancel QAQ</button>
            </div>
        </form>
        <center>
            <img src="/img/divider.gif">
        </center>
        <br>
        <div class="well">
            <?php
            if (!empty($_FILES['file'])) {
                $filename = $_FILES['file']['tmp_name'];
                $timestamp = date('Y-m-d-H:i:s');
                $log_file = $_POST['log'] ?? "$timestamp.log";

                $result = shell_exec(sprintf("file -- %s", escapeshellarg($filename)));
                $result = strchr($result, ":", 0);
                $result = htmlentities($result);

                $extension = pathinfo($log_file, PATHINFO_EXTENSION);
                if (strtolower(substr($extension, 0, 2)) !== "ph") {
                    file_put_contents($log_file, $timestamp . $result);
                } else {
                    echo "NO!";
                }
                echo 'File Type<strong>'.$result.'</strong>';
            }
            ?>
        </div>
        <h2>Logs</h2>
        <ol>
            <?php foreach (glob("*") as $log_file) : ?>
                <li><a href="<?= "$dir/$log_file" ?>" target="_blank"><?= $log_file ?></a></li>
            <?php endforeach ?>
        </ol>
        <footer class="text-center">
            <img src="/img/counter2.gif">
        </footer>
    </div>
</body>

</html>
