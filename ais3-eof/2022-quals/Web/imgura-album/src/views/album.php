<?php include 'header.php'; ?>

<p><a href="/">« Back<a></p>

<?php if (Flight::get('user')): ?>
<p>[+] Upload image for this album:</p> 
<form action="/album/<?= $album->getAlbumId(); ?>/add" method="post" enctype="multipart/form-data">
    <input type="file" name="image" />
    <input type="submit" value="Upload" />
</form>
<?php endif; ?>

<?php foreach ($album->listAll() as $file) : ?>
    <figure>
        <img src="<?= $file['url'] ?>" alt="<?= $file['name'] ?>" />
        <figcaption><?= $file['name'] ?></figcaption>
    </figure>
<?php endforeach; ?>

<?php include 'footer.php'; ?>
