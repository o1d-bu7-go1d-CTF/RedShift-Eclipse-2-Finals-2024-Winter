# Базовый образ
FROM gcc:latest
# Установка необходимых пакетов
RUN apt-get update && apt-get install -y \
    socat \
    sqlite3 \
    wget \
    build-essential \
    gawk \
    bison \
    python3 \
    texinfo \
    && apt-get clean && rm -rf /var/lib/apt/lists/*


# Копирование файлов в контейнер
WORKDIR /service
COPY aes reactor_state.dat reactor_users.db /service/
RUN chmod +x ./aes

# Запуск socat для работы с сервисом
CMD socat TCP-LISTEN:12345,reuseaddr,fork EXEC:./aes
