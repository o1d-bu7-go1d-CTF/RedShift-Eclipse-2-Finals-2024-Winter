<?php
// render.php

if (isset($_SESSION['user'])) {
    if ($_SERVER['REQUEST_METHOD'] === 'POST' && isset($_POST['user_input'])) {
        $user_input = $_POST['user_input'];
        
        try {
            $template = $twig->createTemplate($user_input);
            $result = $template->render(['user' => $user_input]);
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
