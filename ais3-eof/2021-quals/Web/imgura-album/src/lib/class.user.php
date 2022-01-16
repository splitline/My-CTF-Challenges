<?php
class User {
    private $username;
    private $albums = array();

    public function __construct($username)
    {
        $this->username = $username;
    }

    public function getUsername()
    {
        return $this->username;
    }

    public function getAlbums()
    {
        return $this->albums;
    }

    public function addAlbum($album)
    {
        $this->albums[] = $album;
    }
}