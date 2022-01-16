<?php include 'header.php'; ?>
<p>Welcome, @<?= Flight::get('user')->getUsername() ?>.</p>

<a href="/">Home</a> | <a href="/new">Create new album</a>
<h3>Your albums:</h3>
<ol>
    <?php foreach (Flight::get('user')->getAlbums() as $album) : ?>
        <li><a href="/album/<?= $album ?>/">[Album] <?= $album ?></a></li>
    <?php endforeach; ?>
</ol>

<?php if (empty(Flight::get('user')->getAlbums())) : ?>
    (No albums found)
<?php endif; ?>

<?php include 'footer.php'; ?>
