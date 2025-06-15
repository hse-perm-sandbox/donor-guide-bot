#  Инструкция по развертыванию DonorGuideBot из Docker-образа

##  Общее описание

**DonorGuideBot** — это Telegram-бот, который автоматически отвечает на вопросы о донорстве крови и костного мозга.  
Проект разработан в рамках курсовой работы и не требует установки Python: запуск происходит из готового Docker-образа.

Docker-образ опубликован в [GitHub Container Registry (GHCR)](https://ghcr.io):  
`ghcr.io/hse-perm-sandbox/donor-guide-bot:v1.0.0`

---

## Что потребуется

Перед началом убедитесь, что на компьютере установлены:

- [Docker](https://docs.docker.com/get-docker/)
- [Docker Compose](https://docs.docker.com/compose/)

Проверить установку можно командами:

```bash
docker --version
docker compose version
```

---

## Шаг 1. Подготовка окружения

Создайте рабочую директорию, в которой будут все файлы:

```bash
mkdir donor-guide-bot && cd donor-guide-bot
```

Создайте `.env` файл со следующими переменными (обязательные параметры для запуска бота):

```env
TELEGRAM_TOKEN=your_telegram_bot_token
RESEND_CHAT_ID=123456789
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_DB=postgres
METRIC_COUNTER_ID=your_metrica_counter_id
ASSETS_DIR=/assets
```

>  Пояснение:
> - `TELEGRAM_TOKEN` — токен Telegram-бота (выдаётся через @BotFather).
> - `RESEND_CHAT_ID` — ID чата, куда будут пересылаться вопросы от пользователей.
> - `METRIC_COUNTER_ID` — ID счётчика Яндекс Метрики, если используется.
> - Остальные переменные относятся к базе данных.

---

##  Шаг 2. Запуск PostgreSQL в контейнере

1. Запустите контейнер с PostgreSQL:

```bash
docker compose -f docker-compose.local.db.yml up -d
```
Эта команда:
- Поднимает базу данных PostgreSQL (порт по умолчанию: 5433)
- Запускает pgAdmin (порт по умолчанию: 5434)

2. Убедитесь, что база данных работает:

```bash
docker ps
```

Вы должны увидеть контейнер с именем `donor_postgres`.

### Как остановить и удалить контейнеры
Остановить и удалить только контейнеры (без потери данных):
```bash
docker compose -f docker-compose.local.yml down
```
Остановить и удалить контейнеры вместе с данными:
```bash
docker compose -f docker-compose.local.yml down -v
```
---

## Шаг 3. Запуск бота из Docker-образа

Запустите основной контейнер с ботом:

```bash
docker run -d \
  --name donor-guide-bot \
  --env-file .env \
  --network host \
  ghcr.io/hse-perm-sandbox/donor-guide-bot:v1.0.0
```

>  **Если вы используете Windows или Mac (Docker Desktop):**
> Замените `--network host` на:

```bash
  -p 8080:8080
```

---

##  Шаг 4. Применение миграций и заполнение базы данных

После запуска контейнера нужно создать таблицы в базе данных и заполнить их начальными данными.

1. Подключитесь к контейнеру:

```bash
docker exec -it donor-guide-bot /bin/bash
```

2. Выполните команды:

```bash
alembic upgrade head
python -m src.database.seeds.initial_data
```

> Это создаст структуру базы данных и загрузит часто задаваемые вопросы.

---

## Управление контейнером

Остановить бота:

```bash
docker stop donor-guide-bot
```

Удалить контейнер:

```bash
docker rm donor-guide-bot
```

Посмотреть логи:

```bash
docker logs donor-guide-bot
```

