<?php
// home.php

if (isset($_SESSION['user'])) {
    echo $twig->render('home.twig', ['user' => $_SESSION['user']]);
} else {
    header('Location: /?action=login');
}