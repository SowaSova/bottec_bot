# bottec_project

# e-commerce бот

## Запуск через Docker:

1. Переименовать файлы .env, убрав "\_example"
2. Добавить данные для переменных BOT_TOKEN и YOOKASSA_TOKEN
3. Запустить контейнер

```bash
docker compose up -d --build
```

4. Бот разворачивает собственную бд, но для полноценной работы бота необходима бд, разворачиваемая в модуле (Админ-панели)[https://github.com/SowaSova/bottec_admin]

5. При работе с собственной бд, провести миграции

```bash
docker compose exec bot poetry run alembic upgrade head
```
