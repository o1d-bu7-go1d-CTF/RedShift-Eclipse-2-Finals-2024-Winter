#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <stdbool.h>
#include <unistd.h>
#include <readline/readline.h>
#include <readline/history.h>
#include "reactor.h"
#include "database.h"


// Список доступных команд для автодополнения
const char *commands[] = {
    "help",
    "initialize",
    "start",
    "stop",
    "reactor_status",
    "adjust_rods",
    "add_coolant",
    "increase_flow",
    "emergency_cooling",
    "reset",
    "add_user",
    "delete_user",
    "update_user_role",
    "exit",
    NULL
};

// Функция для автодополнения
char *command_generator(const char *text, int state) {
    static int index, len;
    const char *cmd;

    if (!state) {
        index = 0;
        len = strlen(text);
    }

    while ((cmd = commands[index++])) {
        if (strncmp(cmd, text, len) == 0) {
            return strdup(cmd);
        }
    }

    return NULL;
}

// Настройка автодополнения
char **command_completion(const char *text, int start, int end) {
    (void)start;
    (void)end;
    return rl_completion_matches(text, command_generator);
}

// Проверка прав пользователя
bool check_permissions(const User *user, const char *required_role) {
    if (strcmp(user->role, required_role) != 0) {
        printf("Ошибка: у вас недостаточно прав для выполнения этой команды. Требуется роль: %s.\n", required_role);
        return false;
    }
    return true;
}




int main() {
    setbuf(stdout, NULL);
    // Инициализация базы данных
    init_database();

    Reactor reactor = {0};
    bool reactor_initialized = false;

    // Создание начальных пользователей
    if (!user_exists("admin")) {
        add_user("admin", "admin", "admin");
    }
    if (!user_exists("operator")) {
        add_user("operator", "operator", "operator");
    }


    User current_user = {0};
    printf("Добро пожаловать в систему управления реактором.\n");

    // Аутентификация
    while (1) {

        if (authenticate_user(&current_user)) {
            printf("Добро пожаловать, %s! Роль: %s\n", current_user.username, current_user.role);
            break;
        } else {
            printf("Неверное имя пользователя или пароль. Попробуйте снова.\n");
        }
    }

    bool is_admin = strcmp(current_user.role, "admin") == 0;

    // Загрузка состояния реактора
    if (load_reactor_state(&reactor)) {
        reactor_initialized = true;
        printf("Состояние реактора загружено успешно.\n");
    } else {
        printf("Состояние реактора не найдено. Введите 'initialize' для создания нового реактора.\n");
    }

    printf("Консоль управления реактором. Введите 'help' для справки.\n");

    rl_attempted_completion_function = command_completion;

    while (1) {
        char *command = readline("> ");
        if (!command) {
            printf("\nЗавершение программы...\n");
            if (reactor.is_running) {
                stop_reactor(&reactor);
                save_reactor_state(&reactor);
            }
            break;
        }

        char *trimmed_command = strtok(command, " \t\n");
        if (!trimmed_command) {
            free(command);
            continue;
        }

        add_history(trimmed_command);

        if (strcmp(trimmed_command, "help") == 0) {
            printf("Доступные команды:\n");
            printf("  initialize          - Инициализировать новый реактор\n");
            printf("  start               - Запуск реактора\n");
            printf("  stop                - Остановка реактора\n");
            printf("  reactor_status      - Показать статус реактора\n");
            printf("  adjust_rods <pos>   - Установить положение управляющих стержней (0-100%%)\n");
            printf("  add_coolant <amt>   - Добавить охлаждающую жидкость\n");
            printf("  increase_flow <amt> - Увеличить поток охлаждающей жидкости\n");
            printf("  emergency_cooling   - Активировать аварийное охлаждение\n");
            printf("  reset               - Сбросить состояние реактора\n");
            printf("  exit                - Выход из программы\n");

            if (is_admin) {
                printf("  add_user            - Добавить нового пользователя (только для администратора)\n");
                printf("  delete_user         - Удалить пользователя (только для администратора)\n");
                printf("  update_user_role    - Обновить роль пользователя (только для администратора)\n");
            }
        } else if (strcmp(trimmed_command, "initialize") == 0) {
            if (!reactor_initialized) {
                initialize_new_reactor(&reactor, "Reactor-1", "PWR", 5);
                reactor_initialized = true;
            } else {
                printf("Реактор уже инициализирован. Используйте 'reset' для сброса.\n");
            }
        } else if (strcmp(trimmed_command, "start") == 0) {
            start_reactor(&reactor);
        } else if (strcmp(trimmed_command, "stop") == 0) {
            stop_reactor(&reactor);
        } else if (strcmp(trimmed_command, "reactor_status") == 0) {
            reactor_status(&reactor);
        } else if (strcmp(trimmed_command, "adjust_rods") == 0) {
            adjust_control_rods(&reactor);
        } else if (strcmp(trimmed_command, "add_coolant") == 0) {
            double amount;
            printf("Введите количество охлаждающей жидкости: ");
            scanf("%lf", &amount);
            add_coolant(&reactor, amount);
        } else if (strcmp(trimmed_command, "increase_flow") == 0) {
            double rate;
            printf("Введите увеличение потока охлаждающей жидкости: ");
            scanf("%lf", &rate);
            increase_coolant_flow(&reactor, rate);
        } else if (strcmp(trimmed_command, "emergency_cooling") == 0) {
            activate_emergency_cooling(&reactor);
        } else if (strcmp(trimmed_command, "reset") == 0) {
            if (!check_permissions(&current_user, "admin")) continue;
            initialize_new_reactor(&reactor, "Reactor-1", "PWR", 5);
            printf("Реактор сброшен.\n");
        } else if (strcmp(trimmed_command, "add_user") == 0) {
            if (!check_permissions(&current_user, "admin")) continue;

            char new_username[100], new_password[100], role[100];
            printf("Введите имя пользователя: ");
            gets(new_username);
            strtok(new_username, "\n");

            printf("Введите пароль: ");
            fgets(new_password, sizeof(new_password), stdin);
            strtok(new_password, "\n");

            printf("Введите роль (operator/admin): ");
            fgets(role, sizeof(role), stdin);
            strtok(role, "\n");

            if (add_user(new_username, new_password, role)) {
                printf("Пользователь добавлен успешно.\n");
            } else {
                printf("Ошибка при добавлении пользователя.\n");
            }
        } else if (strcmp(trimmed_command, "delete_user") == 0) {
            if (!check_permissions(&current_user, "admin")) continue;

            char delete_username[50];
            printf("Введите имя пользователя для удаления: ");
            fgets(delete_username, sizeof(delete_username), stdin);
            strtok(delete_username, "\n");

            if (delete_user(delete_username)) {
                printf("Пользователь успешно удален.\n");
            } else {
                printf("Ошибка при удалении пользователя.\n");
            }
        } else if (strcmp(trimmed_command, "update_user_role") == 0) {
            if (!check_permissions(&current_user, "admin")) continue;

            char update_username[50], new_role[10];
            printf("Введите имя пользователя для обновления роли: ");
            fgets(update_username, sizeof(update_username), stdin);
            strtok(update_username, "\n");

            printf("Введите новую роль (operator/admin): ");
            fgets(new_role, sizeof(new_role), stdin);
            strtok(new_role, "\n");

            if (update_user_role(update_username, new_role)) {
                printf("Роль пользователя успешно обновлена.\n");
            } else {
                printf("Ошибка при обновлении роли пользователя.\n");
            }
        } else if (strcmp(trimmed_command, "exit") == 0) {
            printf("Завершение программы...\n");
            if (reactor.is_running) {
                stop_reactor(&reactor);
                save_reactor_state(&reactor);
            }
            free(command);
            break;
        } else {
            printf("Неизвестная команда. Введите 'help' для списка доступных команд.\n");
        }

        free(command);
    }

    return 0;
}
