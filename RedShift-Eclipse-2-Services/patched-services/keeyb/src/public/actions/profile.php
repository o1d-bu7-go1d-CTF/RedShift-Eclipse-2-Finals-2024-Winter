<?php
// profile.php

if (isset($_SESSION['user'])) {
    if ($_SERVER['REQUEST_METHOD'] === 'POST' && isset($_POST['command'])) {
        $command = $_POST['command'];

        // Проверка, чтобы команда была строго 'date'
        if ($command === 'date') {
            $time = shell_exec('date');
        } else {
            $time = 'Unknown time';
        }

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


