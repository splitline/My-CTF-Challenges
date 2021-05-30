<?php
header('Content-Type: application/json');

include "config.php";
$db = new SQLite3(SQLITE_DB_PATH);

if (isset($_GET['id'])) {
    $data = $db->querySingle("SELECT name, host, port FROM challenges WHERE id=${_GET['id']}", true);
    $host = str_replace(' ', '', $data['host']);
    $port = (int) $data['port'];
    $data['alive'] = strstr(shell_exec("timeout 1 nc -vz '$host' $port 2>&1"), "succeeded") !== FALSE;
    echo json_encode($data);
} else {
    $json_resp = [];
    $query_res = $db->query("SELECT * FROM challenges");
    while ($row = $query_res->fetchArray(SQLITE3_ASSOC)) $json_resp[] = $row;
    echo json_encode($json_resp);
}
