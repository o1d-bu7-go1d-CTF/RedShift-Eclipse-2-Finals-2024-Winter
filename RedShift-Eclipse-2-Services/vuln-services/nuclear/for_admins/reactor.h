#ifndef REACTOR_H
#define REACTOR_H

#include <stdbool.h>
#include <pthread.h>

// Структура описания параметров активной зоны реактора
typedef struct {
    double core_temperature;      // Температура активной зоны (°C)
    double neutron_flux;          // Поток нейтронов (нейтроны/см^2·с)
    double control_rod_position;  // Положение управляющих стержней (%)
    double power_output;          // Выходная мощность (МВт)
} ReactorCore;

// Структура описания охлаждающей системы
typedef struct {
    double coolant_temperature_in;   // Температура охлаждающей жидкости на входе (°C)
    double coolant_temperature_out;  // Температура охлаждающей жидкости на выходе (°C)
    double coolant_flow_rate;        // Скорость потока охлаждающей жидкости (л/с)
    double coolant_pressure;         // Давление охлаждающей жидкости (атм)
    double coolant_level;            // Уровень охлаждающей жидкости (%)
} CoolingSystem;

// Структура описания топлива
typedef struct {
    double fuel_burnup;          // Выгорание топлива (%)
    double fuel_enrichment;      // Обогащение урана (%)
    double fuel_temperature;     // Температура топлива (°C)
    int fuel_rod_count;          // Количество топливных стержней
} FuelSystem;

// Структура безопасности
typedef struct {
    bool emergency_shutdown;     // Аварийное отключение (SCRAM)
    double radiation_level;      // Уровень радиации в зоне реактора (мкЗв/ч)
    double containment_pressure; // Давление в гермооболочке (атм)
    bool leak_detected;          // Обнаружение утечек
} SafetySystem;

// Общая структура реактора
typedef struct {
    char reactor_name[50];        // Имя реактора
    char reactor_type[50];        // Тип реактора (PWR, BWR, CANDU, и т.д.)
    int operational_years;        // Количество лет эксплуатации
    bool is_running;              // Текущее состояние реактора (включен/выключен)

    ReactorCore core;             // Активная зона реактора
    CoolingSystem cooling;        // Система охлаждения
    FuelSystem fuel;              // Топливная система
    SafetySystem safety;          // Система безопасности
} Reactor;

void initialize_reactor(Reactor *reactor, const char *name, const char *type, int operational_years);
void start_reactor(Reactor *reactor);
void stop_reactor(Reactor *reactor);
void save_reactor_state(const Reactor *reactor);
bool load_reactor_state(Reactor *reactor);
void initialize_new_reactor(Reactor *reactor, const char *name, const char *type, int operational_years);
void reactor_status(const Reactor *reactor);
void adjust_control_rods(Reactor *reactor);
void add_coolant(Reactor *reactor, double amount);
void increase_coolant_flow(Reactor *reactor, double rate);
void activate_emergency_cooling(Reactor *reactor);
void handle_overheat(Reactor *reactor);
void handle_radiation_spike(Reactor *reactor);


#endif // REACTOR_H
