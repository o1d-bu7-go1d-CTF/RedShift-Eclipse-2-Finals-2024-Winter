<?php
// about.php

if (isset($_SESSION['user'])) {
    echo $twig->render('about.twig', ['user' => $_SESSION['user']]);
} else {
    header('Location: /?action=login');
}