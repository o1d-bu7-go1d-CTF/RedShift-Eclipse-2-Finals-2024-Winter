<?php
// gallery.php

if (isset($_SESSION['user'])) {
    echo $twig->render('gallery.twig', ['user' => $_SESSION['user']]);
} else {
    header('Location: /?action=login');
}