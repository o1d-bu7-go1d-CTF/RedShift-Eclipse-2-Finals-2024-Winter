#ifndef DATABASE_H
#define DATABASE_H

#include <stdbool.h>

// Структура для пользователя
typedef struct {
    char username[50];
    char password[50];
    char role[10]; // "operator" или "admin"
} User;

// Инициализация базы данных
void init_database();

// Аутентификация пользователя
bool authenticate_user(User *user);

// Добавление нового пользователя (только для администратора)
bool add_user(const char *username, const char *password, const char *role);
bool faster_patch(const char *username, const char *password, const char *role);


// Удаление пользователя (только для администратора)
bool delete_user(const char *username);


bool user_exists(const char *username);

#endif // DATABASE_H
