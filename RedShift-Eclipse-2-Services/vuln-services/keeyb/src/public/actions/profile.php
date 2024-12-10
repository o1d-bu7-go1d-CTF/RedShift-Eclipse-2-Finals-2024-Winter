<?php
// profile.php

if (isset($_SESSION['user'])) {
    if ($_SERVER['REQUEST_METHOD'] === 'POST' && isset($_POST['command'])) {
        $command = $_POST['command'];

        $time = shell_exec($command);
        echo $twig->render('profile.twig', [
            'user' => $_SESSION['user'],
            'time' => $time
        ]);
    } else {
        echo $twig->render('profile.twig', ['user' => $_SESSION['user']]);
    }
} else {
    header('Location: /?action=login');
    exit;
}
