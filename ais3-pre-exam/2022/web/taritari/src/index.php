<h1>Tari</h1>
<p>Tari is a service that converts your file into a .tar.gz archive.</p>
<form action="/" method="POST" enctype="multipart/form-data">
    <input type="file" name="file" />
    <input type="submit" value="Upload" />
</form>
<?php
function get_MyFirstCTF_flag()
{
    // **MyFirstCTF ONLY FLAG**
    // Please IGNORE this flag if you are AIS3 Pre-Exam Player

    // Congratulations, you found the flag!
    // RCE me to get the second flag, it placed in the / directory :D
    echo 'MyFirstCTF FLAG: AIS3{../../3asy_pea5y_p4th_tr4ver5a1}';
}

function tar($file)
{
    $filename = $file['name'];
    $path = bin2hex(random_bytes(16)) . ".tar.gz";
    $source = substr($file['tmp_name'], 1);
    $destination = "./files/$path";
    passthru("tar czf '$destination' --transform='s|$source|$filename|' --directory='/tmp' '/$source'", $return);
    if ($return === 0) {
        return [$path, $filename];
    }
    return [FALSE, FALSE];
}

if ($_SERVER['REQUEST_METHOD'] == 'POST') {
    $file = $_FILES['file'];
    if ($file === NULL) {
        echo "<p>No file was uploaded.</p>";
    } elseif ($file['error'] !== 0) {
        echo "<p>Error: Upload error.</p>";
    } else {
        [$path, $filename] = tar($file);
        if ($path === FALSE) {
            echo "<p>Error: Failed to create archive.</p>";
        } else {
            $path = base64_encode($path);
            $filename = urlencode($filename);
            echo "<a href=\"/download.php?file=$path&name=$filename.tar.gz\">Download</a>";
        }
    }
}
