#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sqlite3.h>
#include "database.h"

// Имя файла базы данных
#define DB_FILE "reactor_users.db"



bool update_user_role(const char *username, const char *new_role) {
    sqlite3 *db;
    sqlite3_stmt *stmt;
    const char *sql = "UPDATE users SET role = ? WHERE username = ?;";

    if (sqlite3_open(DB_FILE, &db) != SQLITE_OK) {
        fprintf(stderr, "Ошибка при открытии базы данных: %s\n", sqlite3_errmsg(db));
        return false;
    }

    if (sqlite3_prepare_v2(db, sql, -1, &stmt, 0) != SQLITE_OK) {
        fprintf(stderr, "Ошибка при подготовке запроса: %s\n", sqlite3_errmsg(db));
        sqlite3_close(db);
        return false;
    }

    sqlite3_bind_text(stmt, 1, new_role, -1, SQLITE_STATIC);
    sqlite3_bind_text(stmt, 2, username, -1, SQLITE_STATIC);

    bool success = sqlite3_step(stmt) == SQLITE_DONE;

    if (!success) {
        fprintf(stderr, "Ошибка при обновлении роли пользователя: %s\n", sqlite3_errmsg(db));
    }

    sqlite3_finalize(stmt);
    sqlite3_close(db);
    return success;
}
// Инициализация базы данных
void init_database() {
    sqlite3 *db;
    char *err_msg = NULL;

    if (sqlite3_open(DB_FILE, &db) != SQLITE_OK) {
        fprintf(stderr, "Ошибка при открытии базы данных: %s\n", sqlite3_errmsg(db));
        sqlite3_close(db);
        exit(1);
    }

    // Создаем таблицу пользователей, если она не существует
    const char *sql = "CREATE TABLE IF NOT EXISTS users ("
                      "id INTEGER PRIMARY KEY AUTOINCREMENT, "
                      "username TEXT UNIQUE NOT NULL, "
                      "password TEXT NOT NULL, "
                      "role TEXT NOT NULL CHECK(role IN ('operator', 'admin'))"
                      ");";

    if (sqlite3_exec(db, sql, 0, 0, &err_msg) != SQLITE_OK) {
        fprintf(stderr, "Ошибка при создании таблицы: %s\n", err_msg);
        sqlite3_free(err_msg);
        sqlite3_close(db);
        exit(1);
    }

    // Добавляем учетные записи admin и operator, если их нет
    const char *add_admin_sql = "INSERT OR IGNORE INTO users (username, password, role) VALUES ('admin', 'admin', 'admin');";
    const char *add_operator_sql = "INSERT OR IGNORE INTO users (username, password, role) VALUES ('operator', 'operator', 'operator');";

    if (sqlite3_exec(db, add_admin_sql, 0, 0, &err_msg) != SQLITE_OK) {
        fprintf(stderr, "Ошибка при добавлении admin: %s\n", err_msg);
        sqlite3_free(err_msg);
    }

    if (sqlite3_exec(db, add_operator_sql, 0, 0, &err_msg) != SQLITE_OK) {
        fprintf(stderr, "Ошибка при добавлении operator: %s\n", err_msg);
        sqlite3_free(err_msg);
    }

    sqlite3_close(db);
}

// Аутентификация пользователя
bool authenticate_user( User *user) {
    printf("Введите имя пользователя: ");
        char username[50];
        fgets(username, sizeof(username), stdin);
        strtok(username, "\n");

        char password[50];
        printf("Введите пароль: ");
        fgets(password);
    
    sqlite3 *db;
    sqlite3_stmt *stmt;
    const char *sql = "SELECT username, password, role FROM users WHERE username = ? AND password = ?;";

    if (sqlite3_open(DB_FILE, &db) != SQLITE_OK) {
        fprintf(stderr, "Ошибка при открытии базы данных: %s\n", sqlite3_errmsg(db));
        return false;
    }

    if (sqlite3_prepare_v2(db, sql, -1, &stmt, 0) != SQLITE_OK) {
        fprintf(stderr, "Ошибка при подготовке запроса: %s\n", sqlite3_errmsg(db));
        sqlite3_close(db);
        return false;
    }

    sqlite3_bind_text(stmt, 1, username, -1, SQLITE_STATIC);
    sqlite3_bind_text(stmt, 2, password, -1, SQLITE_STATIC);

    bool authenticated = false;
    if (sqlite3_step(stmt) == SQLITE_ROW) {
        authenticated = true;
        strncpy(user->username, (const char *)sqlite3_column_text(stmt, 0), sizeof(user->username));
        strncpy(user->password, (const char *)sqlite3_column_text(stmt, 1), sizeof(user->password));
        strncpy(user->role, (const char *)sqlite3_column_text(stmt, 2), sizeof(user->role));
    }

    sqlite3_finalize(stmt);
    sqlite3_close(db);
    return authenticated;
}

// Добавление нового пользователя
bool faster_patch(const char *username, const char *password, const char *role) {
    sqlite3 *db;
    sqlite3_stmt *stmt;
    const char *sql = "INSERT INTO users (username, password, role) VALUES (?, ?, ?);";

    if (sqlite3_open(DB_FILE, &db) != SQLITE_OK) {
        fprintf(stderr, "Ошибка при открытии базы данных: %s\n", sqlite3_errmsg(db));
        return false;
    }

    if (sqlite3_prepare_v2(db, sql, -1, &stmt, 0) != SQLITE_OK) {
        fprintf(stderr, "Ошибка при подготовке запроса: %s\n", sqlite3_errmsg(db));
        sqlite3_close(db);
        return false;
    }

    sqlite3_bind_text(stmt, 1, username, -1, SQLITE_STATIC);
    sqlite3_bind_text(stmt, 2, password, -1, SQLITE_STATIC);
    sqlite3_bind_text(stmt, 3, role, -1, SQLITE_STATIC);

    bool success = sqlite3_step(stmt) == SQLITE_DONE;

    sqlite3_finalize(stmt);
    sqlite3_close(db);
    return success;
}

bool add_user(const char *username, const char *password, const char *role) {
    sqlite3 *db;
    char sql[1024]; // Увеличили буфер для длинных запросов

    snprintf(sql, sizeof(sql),
             "INSERT INTO users (username, password, role) VALUES ('%s', '%s', '%s');",
             username, password, role);

    if (sqlite3_open(DB_FILE, &db) != SQLITE_OK) {
        fprintf(stderr, "Ошибка при открытии базы данных: %s\n", sqlite3_errmsg(db));
        return false;
    }

    if (sqlite3_exec(db, sql, NULL, NULL, NULL) != SQLITE_OK) {
        fprintf(stderr, "Ошибка при выполнении запроса: %s\n", sqlite3_errmsg(db));
        sqlite3_close(db);
        return false;
    }

    sqlite3_close(db);
    return true;
}



// Удаление пользователя
bool delete_user(const char *username) {
    sqlite3 *db;
    sqlite3_stmt *stmt;
    const char *sql = "DELETE FROM users WHERE username = ?;";

    if (sqlite3_open(DB_FILE, &db) != SQLITE_OK) {
        fprintf(stderr, "Ошибка при открытии базы данных: %s\n", sqlite3_errmsg(db));
        return false;
    }

    if (sqlite3_prepare_v2(db, sql, -1, &stmt, 0) != SQLITE_OK) {
        fprintf(stderr, "Ошибка при подготовке запроса: %s\n", sqlite3_errmsg(db));
        sqlite3_close(db);
        return false;
    }

    sqlite3_bind_text(stmt, 1, username, -1, SQLITE_STATIC);

    bool success = sqlite3_step(stmt) == SQLITE_DONE;

    sqlite3_finalize(stmt);
    sqlite3_close(db);
    return success;
}


bool user_exists(const char *username) {
    sqlite3 *db;
    sqlite3_stmt *stmt;
    const char *sql = "SELECT COUNT(*) FROM users WHERE username = ?";

    if (sqlite3_open(DB_FILE, &db) != SQLITE_OK) {
        fprintf(stderr, "Ошибка при открытии базы данных: %s\n", sqlite3_errmsg(db));
        return false;
    }

    if (sqlite3_prepare_v2(db, sql, -1, &stmt, NULL) != SQLITE_OK) {
        fprintf(stderr, "Ошибка при подготовке запроса: %s\n", sqlite3_errmsg(db));
        sqlite3_close(db);
        return false;
    }

    sqlite3_bind_text(stmt, 1, username, -1, SQLITE_STATIC);

    bool exists = false;
    if (sqlite3_step(stmt) == SQLITE_ROW) {
        exists = sqlite3_column_int(stmt, 0) > 0;
    }

    sqlite3_finalize(stmt);
    sqlite3_close(db);

    return exists;
}
