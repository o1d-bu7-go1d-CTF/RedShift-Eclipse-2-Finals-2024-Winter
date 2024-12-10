#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <pthread.h>
#include "reactor.h"

// Глобальные переменные для потоков
static pthread_t temperature_thread;
static pthread_t coolant_thread;
static pthread_t radiation_thread;
static bool stop_threads = true; // Флаг для остановки потоков

int position;
int power;
// Имя файла для сохранения состояния реактора
#define REACTOR_STATE_FILE "reactor_state.dat"

// Функция для сохранения состояния реактора в файл
void save_reactor_state(const Reactor *reactor) {
    FILE *file = fopen(REACTOR_STATE_FILE, "wb");
    if (file == NULL) {
        perror("Ошибка при сохранении состояния реактора");
        return;
    }

    // Записываем данные структуры `Reactor` в файл
    if (fwrite(reactor, sizeof(Reactor), 1, file) != 1) {
        perror("Ошибка записи в файл");
    } else {
        printf("Состояние реактора сохранено в файл \"%s\".\n", REACTOR_STATE_FILE);
    }

    fclose(file);
}

// Функция для загрузки состояния реактора из файла
bool load_reactor_state(Reactor *reactor) {
    FILE *file = fopen(REACTOR_STATE_FILE, "rb");
    if (file == NULL) {
        return false; // Файл не найден
    }

    // Читаем данные из файла в структуру `Reactor`
    if (fread(reactor, sizeof(Reactor), 1, file) != 1) {
        perror("Ошибка чтения из файла");
        fclose(file);
        return false;
    }

    fclose(file);
    printf("Состояние реактора загружено из файла \"%s\".\n", REACTOR_STATE_FILE);
    return true;
}

// Функция для инициализации нового реактора
void initialize_new_reactor(Reactor *reactor, const char *name, const char *type, int operational_years) {
    initialize_reactor(reactor, name, type, operational_years);
    save_reactor_state(reactor); // Сохраняем состояние сразу после инициализации
    printf("Новый реактор инициализирован и сохранен.\n");
}

// Функция для отображения текущего состояния реактора
void reactor_status(const Reactor *reactor) {
    printf("\n=== Статус реактора \"%s\" ===\n", reactor->reactor_name);
    printf("Тип реактора: %s\n", reactor->reactor_type);
    printf("Годы эксплуатации: %d\n", reactor->operational_years);
    printf("Состояние: %s\n", reactor->is_running ? "Работает" : "Выключен");
    printf("\n--- Параметры активной зоны ---\n");
    printf("  Температура активной зоны: %.2f °C\n", reactor->core.core_temperature);
    printf("  Поток нейтронов: %.2e нейтронов/см^2·с\n", reactor->core.neutron_flux);
    printf("  Выходная мощность: %.2f МВт\n", reactor->core.power_output);
    printf("  Положение управляющих стержней: %.2f%%\n", reactor->core.control_rod_position);
    printf("\n--- Система охлаждения ---\n");
    printf("  Температура охлаждающей жидкости (вход): %.2f °C\n", reactor->cooling.coolant_temperature_in);
    printf("  Температура охлаждающей жидкости (выход): %.2f °C\n", reactor->cooling.coolant_temperature_out);
    printf("  Скорость потока охлаждающей жидкости: %.2f л/с\n", reactor->cooling.coolant_flow_rate);
    printf("  Давление охлаждающей жидкости: %.2f атм\n", reactor->cooling.coolant_pressure);
    printf("  Уровень охлаждающей жидкости: %.2f%%\n", reactor->cooling.coolant_level);
    printf("\n--- Состояние топлива ---\n");
    printf("  Выгорание топлива: %.2f%%\n", reactor->fuel.fuel_burnup);
    printf("  Обогащение топлива: %.2f%%\n", reactor->fuel.fuel_enrichment);
    printf("  Температура топлива: %.2f °C\n", reactor->fuel.fuel_temperature);
    printf("  Количество топливных стержней: %d\n", reactor->fuel.fuel_rod_count);
    printf("\n--- Система безопасности ---\n");
    printf("  Уровень радиации: %.2f мкЗв/ч\n", reactor->safety.radiation_level);
    printf("  Давление в гермооболочке: %.2f атм\n", reactor->safety.containment_pressure);
    printf("  Аварийное отключение: %s\n", reactor->safety.emergency_shutdown ? "Активировано" : "Нет");
    printf("  Утечки: %s\n", reactor->safety.leak_detected ? "Обнаружены" : "Нет");
    printf("=============================\n");
}

// Поток для управления температурой
void *temperature_control(void *arg) {
    Reactor *reactor = (Reactor *)arg;
    while (!stop_threads) {
        if (reactor->is_running) {
            reactor->core.core_temperature += 5.0;

            if (reactor->core.core_temperature > 1000.0) {
                printf("ВНИМАНИЕ: Температура активной зоны критически высока!\n");
                handle_overheat(reactor); // Запуск критического события
            }
        }
        sleep(1); // Имитация реального времени
    }
    return NULL;
}


// Поток для управления охлаждающей жидкостью
void *coolant_control(void *arg) {
    Reactor *reactor = (Reactor *)arg;
    bool coolant_warning_shown = false; // Флаг для предупреждения

    while (!stop_threads) {
        if (reactor->is_running) {
            reactor->cooling.coolant_level -= 1.0;

            if (reactor->cooling.coolant_level < 20.0) {
                if (!coolant_warning_shown) {
                    printf("ВНИМАНИЕ: Уровень охлаждающей жидкости критически низкий!\n");
                    coolant_warning_shown = true;
                }
            } else {
                // Сбрасываем флаг, если уровень восстановлен
                coolant_warning_shown = false;
            }
        }
        sleep(2); // Имитация реального времени
    }
    return NULL;
}

// Поток для управления уровнем радиации
void handle_radiation_spike(Reactor *reactor) {
    printf("КРИТИЧЕСКОЕ СОБЫТИЕ: Выброс радиации!\n");
    printf("Уровень радиации достиг опасных значений! Реактор будет остановлен.\n");
    reactor->is_running = false;
    stop_threads = true;

    // Завершение программы с ошибкой
    exit(1);
}

void *radiation_control(void *arg) {
    Reactor *reactor = (Reactor *)arg;
    bool radiation_warning_shown = false; // Флаг для предупреждения
    bool critical_event_triggered = false; // Флаг для критического события

    while (!stop_threads) {
        if (reactor->is_running) {
            reactor->safety.radiation_level += 0.1;

            if (reactor->safety.radiation_level > 5.0) {
                if (!critical_event_triggered) {
                    handle_radiation_spike(reactor); // Критическое событие
                    critical_event_triggered = true;
                }
            } else if (reactor->safety.radiation_level > 3.0) {
                if (!radiation_warning_shown) {
                    printf("ВНИМАНИЕ: Уровень радиации превышает допустимое значение!\n");
                    radiation_warning_shown = true;
                }
            } else {
                // Сбрасываем флаги, если уровень радиации снизился
                radiation_warning_shown = false;
                critical_event_triggered = false;
            }
        }
        sleep(3); // Имитация реального времени
    }
    return NULL;
}

// Функция для запуска реактора
void start_reactor(Reactor *reactor) {
    if (reactor->is_running) {
        printf("Реактор уже работает.\n");
        return;
    }

    printf("Запуск реактора...\n");
    reactor->is_running = true;
    stop_threads = false;

    // Создаем потоки
    pthread_create(&temperature_thread, NULL, temperature_control, reactor);
    pthread_create(&coolant_thread, NULL, coolant_control, reactor);
    pthread_create(&radiation_thread, NULL, radiation_control, reactor);

    printf("Реактор запущен.\n");
}

// Функция для остановки реактора
void stop_reactor(Reactor *reactor) {
    if (!reactor->is_running) {
        printf("Реактор уже остановлен.\n");
        return;
    }

    printf("Остановка реактора...\n");
    reactor->is_running = false;
    stop_threads = true;

    // Ожидаем завершения потоков
    pthread_join(temperature_thread, NULL);
    pthread_join(coolant_thread, NULL);
    pthread_join(radiation_thread, NULL);

    printf("Реактор остановлен.\n");
}

void initialize_reactor(Reactor *reactor, const char *name, const char *type, int operational_years) {
    // Устанавливаем основную информацию о реакторе
    strncpy(reactor->reactor_name, name, sizeof(reactor->reactor_name) - 1);
    strncpy(reactor->reactor_type, type, sizeof(reactor->reactor_type) - 1);
    reactor->reactor_name[sizeof(reactor->reactor_name) - 1] = '\0'; // Гарантия завершения строки
    reactor->reactor_type[sizeof(reactor->reactor_type) - 1] = '\0'; // Гарантия завершения строки
    reactor->operational_years = operational_years;
    reactor->is_running = false;

    // Инициализация активной зоны
    reactor->core.core_temperature = 25.0;  // Начальная температура (°C)
    reactor->core.neutron_flux = 0.0;       // Поток нейтронов в выключенном состоянии
    reactor->core.power_output = 0.0;       // Выходная мощность (МВт)
    reactor->core.control_rod_position = 100; // Управляющие стержни полностью вставлены

    // Инициализация системы охлаждения
    reactor->cooling.coolant_temperature_in = 25.0;   // Начальная температура охлаждающей жидкости на входе (°C)
    reactor->cooling.coolant_temperature_out = 25.0;  // Начальная температура на выходе (°C)
    reactor->cooling.coolant_flow_rate = 0.0;         // Поток жидкости (реактор выключен)
    reactor->cooling.coolant_pressure = 1.0;          // Давление жидкости (атм)
    reactor->cooling.coolant_level = 100.0;           // Уровень охлаждающей жидкости (%)

    // Инициализация системы топлива
    reactor->fuel.fuel_burnup = 0.0;      // Топливо свежее (%)
    reactor->fuel.fuel_enrichment = 4.0; // Обогащение урана (обычно 4%)
    reactor->fuel.fuel_temperature = 25.0; // Начальная температура топлива (°C)
    reactor->fuel.fuel_rod_count = 100;  // Количество топливных стержней (условное)

    // Инициализация системы безопасности
    reactor->safety.emergency_shutdown = false;  // SCRAM выключен
    reactor->safety.radiation_level = 0.1;       // Уровень радиации (мкЗв/ч)
    reactor->safety.containment_pressure = 1.0;  // Давление в гермооболочке (атм)
    reactor->safety.leak_detected = false;       // Утечек нет

    printf("Реактор \"%s\" (%s) успешно инициализирован.\n", reactor->reactor_name, reactor->reactor_type);
}

void adjust_control_rods(Reactor *reactor) {
    power =  reactor->core.power_output;
    printf("Введите новое положение управляющих стержней (0-100%%): ");
    scanf("%lf", &position);
    if (position < 0.0 || position > 100.0) {
        printf("Ошибка: недопустимое значение. Допустимый диапазон 0-100%%.\n");
        return;
    }
    reactor->core.power_output = power;
    reactor->core.control_rod_position = position;
    printf("Управляющие стержни установлены на %.2f%%.\n", reactor->core.control_rod_position);
}


void add_coolant(Reactor *reactor, double amount) {
    if (amount <= 0.0) {
        printf("Ошибка: Количество добавляемой жидкости должно быть больше 0.\n");
        return;
    }

    reactor->cooling.coolant_level += amount;
    if (reactor->cooling.coolant_level > 100.0) {
        reactor->cooling.coolant_level = 100.0;
    }

    printf("Уровень охлаждающей жидкости увеличен. Текущий уровень: %.2f%%.\n", reactor->cooling.coolant_level);
}

void increase_coolant_flow(Reactor *reactor, double rate) {
    if (rate <= 0.0) {
        printf("Ошибка: Скорость потока должна быть больше 0.\n");
        //return;
    }

    reactor->cooling.coolant_flow_rate += rate;
    printf("Скорость потока охлаждающей жидкости увеличена. Текущий поток: %.2f л/с.\n", reactor->cooling.coolant_flow_rate);
}

void activate_emergency_cooling(Reactor *reactor) {
    printf("Экстренная система охлаждения активирована!\n");

    // Резкое снижение температуры
    reactor->core.core_temperature -= 200.0;
    if (reactor->core.core_temperature < 25.0) {
        reactor->core.core_temperature = 25.0; // Минимальная температура
    }

    // Восстановление уровня охлаждающей жидкости
    reactor->cooling.coolant_level = 100.0;

    printf("Температура снижена до %.2f°C. Уровень охлаждающей жидкости восстановлен.\n", reactor->core.core_temperature);
}


void handle_overheat(Reactor *reactor) {
    printf("КРИТИЧЕСКОЕ СОБЫТИЕ: Перегрев реактора!\n");
    printf("У вас есть 10 секунд, чтобы охладить реактор. Используйте команды управления!\n");

    // Ожидание 10 секунд
    sleep(10);

    // Проверяем, снизилась ли температура ниже критической
    if (reactor->core.core_temperature > 1000.0) {
        printf("ВЗРЫВ РЕАКТОРА!!! СИСТЕМА ПОВРЕЖДЕНА.\n");
        reactor->is_running = false;
        stop_threads = true;

        // Завершение программы с ошибкой
        exit(1);
    } else {
        printf("Температура стабилизирована. Перегрев предотвращен.\n");
    }
}
