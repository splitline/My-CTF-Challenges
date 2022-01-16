<?php
require __DIR__ . '/../vendor/autoload.php';
require __DIR__ . '/../lib/inc.common.php';

Flight::set('flight.views.path', '../views/');

Flight::before('start', function () {
    if (isset($_SESSION['user'])) {
        // We can use Flight::get('user') to get $_SESSION['user'].
        Flight::set('user', $_SESSION['user']);
    }
});

Flight::route('/', function () {
    if (!Flight::get('user')) return Flight::redirect('/login');

    Flight::render('home', ['title' => 'Imgura Album']);
});

Flight::route('GET /login', function () {
    Flight::render('login', ['title' => 'Login']);
});

Flight::route('POST /login', function () {
    $username = Flight::request()->data->username;
    $_SESSION['user'] = new User($username);
    Flight::redirect('/');
});

Flight::route('/new', function () {
    if (!Flight::get('user')) return Flight::redirect('/login');

    $id = bin2hex(random_bytes(8));
    $album = new Album($id);
    $album->create();
    Flight::get('user')->addAlbum($id);
    Flight::redirect("/album/$id/");
});

Flight::route('/album/@id', function ($id) {
    $album = new Album($id);
    if (!$album->isExist())
        Flight::redirect('/');
    else
        Flight::render('album', ['title' => 'Album::' . $album->getAlbumId(), 'album' => $album]);
});

Flight::route('POST /album/@id/add', function ($id) {
    if (!Flight::get('user')) return Flight::redirect('/login');

    $album = new Album($id);
    $album->addImage(
        Flight::request()->files->image['tmp_name'],
        Flight::request()->files->image['name']
    );
    Flight::redirect("/album/$id/");
});

Flight::start();
