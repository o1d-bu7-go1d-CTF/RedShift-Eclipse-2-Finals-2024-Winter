<?php
// login.php

if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    $username = $_POST['username'];
    $password = $_POST['password'];

    $stmt = $db->prepare('SELECT * FROM users WHERE username = :username');
    $stmt->execute(['username' => $username]);
    $user = $stmt->fetch();

    if ($user && password_verify($password, $user['password'])) {
        $_SESSION['user'] = $user['username'];
        header('Location: /?action=profile');
        exit;
    } else {
        echo $twig->render('login.twig', ['error' => 'Invalid credentials']);
    }
} else {
    echo $twig->render('login.twig');
}