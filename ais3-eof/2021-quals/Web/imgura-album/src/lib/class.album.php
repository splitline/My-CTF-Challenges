<?php
class Album
{
    private $albumId;

    public function __construct($albumId)
    {
        $this->albumId = $albumId;
    }

    public function isExist()
    {
        return file_exists($this->getAlbumPath());
    }

    public function create()
    {
        if (!$this->isExist()) mkdir($this->getAlbumPath());
    }

    public function getAlbumId()
    {
        return $this->albumId;
    }

    public function getAlbumPath()
    {
        return "./uploads/$this->albumId";
    }

    public function addImage($uploaded_file_path, $image_name)
    {
        if (getimagesize($uploaded_file_path) === false)
            throw new Exception("File is not an image");

        // NO WEBSHELL THIS TIME :D
        if (str_ends_with($image_name, 'jpg') || str_ends_with($image_name, 'jpeg') || str_ends_with($image_name, 'png'))
            move_uploaded_file($uploaded_file_path, $this->getAlbumPath() . "/$image_name");
        else
            throw new Exception("Invalid extension");
    }

    public function listAll()
    {
        $files = array();
        // list images in this album
        foreach (glob($this->getAlbumPath() . "/*.{jpg,jpeg,png}", GLOB_BRACE) as $file) {
            $files[] = array(
                'name' => basename($file),
                'url' => "/uploads/$this->albumId/" . basename($file)
            );
        }

        return $files;
    }
}
