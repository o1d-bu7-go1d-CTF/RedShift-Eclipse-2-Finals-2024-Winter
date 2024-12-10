<?php
// training.php

if (isset($_SESSION['user'])) {
    echo $twig->render('training.twig', ['user' => $_SESSION['user']]);
} else {
    header('Location: /?action=login');
}