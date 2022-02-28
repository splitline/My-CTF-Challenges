<?php
require __DIR__ . '/../vendor/autoload.php';

$pdo = new \PDO("mysql:host=database;dbname=db", "user", "p@55w0rd");
$fluent = new \Envms\FluentPDO\Query($pdo);

session_start();
