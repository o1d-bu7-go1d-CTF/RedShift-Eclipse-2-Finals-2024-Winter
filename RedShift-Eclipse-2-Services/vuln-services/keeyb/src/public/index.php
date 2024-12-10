<?php
require_once '/var/www/html/vendor/autoload.php';

$loader = new \Twig\Loader\FilesystemLoader('/var/www/html/templates');
$twig = new \Twig\Environment($loader);

$db = new PDO('mysql:host=keeybgallery-db;dbname=mydb', 'user', 'password');

session_start();

if (isset($_GET['action'])) {
    $action = $_GET['action'];
} else {
    $action = 'login';
}

if ($action == 'login') {
    require 'actions/login.php';
} elseif ($action == 'register') {
    require 'actions/register.php';
} elseif ($action == 'profile') {
    require 'actions/profile.php';
} elseif ($action == 'about') {
    require 'actions/about.php';
} elseif ($action == 'training') {
    require 'actions/training.php';
} elseif ($action == 'render') {
    require 'actions/render.php';
} elseif ($action == 'gallery') {
    require 'actions/gallery.php';
} elseif ($action == 'home') {
    require 'actions/home.php';
}
