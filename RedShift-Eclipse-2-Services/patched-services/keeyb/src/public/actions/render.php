<?php
// render.php

if (isset($_SESSION['user'])) {
    if ($_SERVER['REQUEST_METHOD'] === 'POST' && isset($_POST['user_input'])) {
        $user_input = htmlspecialchars($_POST['user_input'], ENT_QUOTES, 'UTF-8'); // Sanitize user input
        
        try {
            // Using a predefined template instead of creating from user input
            $result = $twig->render('user_template.twig', ['user_input' => $user_input]);
            echo "Your text: $result";
        } catch (Exception $e) {
            // Обрабатываем ошибки
            echo 'Ошибка в шаблоне: ' . $e->getMessage();
        }
    } else {
        echo $twig->render('training.twig', ['user' => $_SESSION['user']]);
    }
} else {
    header('Location: /?action=login');
    exit;
}