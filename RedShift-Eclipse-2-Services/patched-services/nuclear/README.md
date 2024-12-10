# Compile

Команда для компиляции исходного файла

```bash
gcc aes.c reactor.c database.c -o aes -lreadline -lsqlite3 -fno-stack-protector -std=c99
```