#  Инструкция по развертыванию DonorGuideBot на сервере

##  Общее описание

**DonorGuideBot** — это Telegram-бот, который автоматически отвечает на вопросы о донорстве крови и костного мозга.  
Проект разработан в рамках курсовой работы и поставляется в виде готового Docker-образа.

Docker-образ опубликован в [GitHub Container Registry](https://github.com/hse-perm-sandbox/donor-guide-bot/pkgs/container/donor-guide-bot):  
`ghcr.io/hse-perm-sandbox/donor-guide-bot:v1.0.0`

---

## Что потребуется

Перед началом убедитесь, что на сервере установлены:

- [Docker](https://docs.docker.com/get-docker/)
- [Docker Compose](https://docs.docker.com/compose/)

Проверить установку можно командами:

```bash
docker --version
docker compose version
```

---

## Шаг 1. Подготовка окружения

Задайте значения для переменных окружения:

```bash
export TELEGRAM_TOKEN=your_telegram_bot_token
export RESEND_CHAT_ID=123456789
export RESEND_THREAD_ID=100500
export METRIC_COUNTER_ID=your_metrica_counter_id
export POSTGRES_USER=postgres
export POSTGRES_PASSWORD=postgres
export POSTGRES_DB=donor-guide-db
export POSTGRES_HOST=postgres
export POSTGRES_PORT=5432
export DONATION_URL=https://set.actual.link.here
```

>  Пояснение:
> - `TELEGRAM_TOKEN` — токен Telegram-бота (выдаётся через @BotFather).
> - `RESEND_CHAT_ID` — ID чата, куда будут пересылаться вопросы от пользователей.
> - `RESEND_THREAD_ID` — ID топика чата, куда будут пересылаться вопросы от пользователей, не обязательная переменная.
> - `METRIC_COUNTER_ID` — ID счётчика Яндекс Метрики, если используется, не обязательная переменная.
> - `POSTGRES_USER` — название пользователя в базе данных.
> - `POSTGRES_PASSWORD` — пароль пользователя в базе данных.
> - `POSTGRES_DB` — название базы данных.
> - `POSTGRES_HOST` — адрес хоста, на котором запущена база данных, если СУБД запущена в docker-контейнере и контейнеры объединены в одной сети, указать название контейнера.
> - `POSTGRES_PORT` — порт, на котором запущена СУБД, по умолчанию 5432.
> - `DONATION_URL` — ссылка на страницу для пожертвований.

В целях безопасности задайте уникальное имя пользователя и сложный случайно сгенерированный пароль для доступа к базе данных.

---

##  Шаг 2. Запуск PostgreSQL в контейнере

1. Создайте в docker сеть с названием:

```bash
docker network create donor-guide-network
```

2. Запустите контейнер с PostgreSQL:

```bash
docker run -d \
  -p 5432:5432 \
  -v donor-guide-data:/var/lib/postgresql/data \
  -e POSTGRES_USER=$POSTGRES_USER \
  -e POSTGRES_PASSWORD=$POSTGRES_PASSWORD \
  -e POSTGRES_DB=$POSTGRES_DB \
  --network donor-guide-network \
  --name donor-guide-db \
  postgres:16.0-bullseye
```
---

## Шаг 3. Запуск бота из Docker-образа

Скачайте Docker-образ:

```bash
docker pull ghcr.io/hse-perm-sandbox/donor-guide-bot:v1.0.0
```

Запустите основной контейнер с ботом:

```bash
docker run -d \
  -e TELEGRAM_TOKEN=your_telegram_bot_token \
  -e RESEND_CHAT_ID=$RESEND_CHAT_ID \
  -e RESEND_THREAD_ID=$RESEND_THREAD_ID \
  -e METRIC_COUNTER_ID=$METRIC_COUNTER_ID \
  -e POSTGRES_USER=$POSTGRES_USER \
  -e POSTGRES_PASSWORD=$POSTGRES_PASSWORD \
  -e POSTGRES_DB=$POSTGRES_DB \
  -e POSTGRES_HOST=$POSTGRES_HOST \
  -e POSTGRES_PORT=$POSTGRES_PORT \
  -e DONATION_URL=$DONATION_URL \
  --name donor-guide-bot \
  --network donor-guide-network \
  ghcr.io/hse-perm-sandbox/donor-guide-bot:v1.0.0
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
.venv/bin/alembic upgrade head
.venv/bin/python -m src.database.seeds.initial_data
```

> Это создаст структуру базы данных и загрузит часто задаваемые вопросы.

Посмотреть логи бота можно командой:

```bash
docker logs donor-guide-bot
```
---

## Управление контейнером

Остановить контейнеры с ботом и базой данных:

```bash
docker stop donor-guide-bot
docker stop donor-guide-db
```

Удалить контейнеры с ботом и базой данных:

```bash
docker rm -f donor-guide-bot
docker rm -f donor-guide-db
```

Удалить данные:

```bash
docker volume rm donor-guide-data
```

Удалить сеть:

```bash
docker network remove donor-guide-network
```

Удалить образ:

```bash
docker rmi ghcr.io/hse-perm-sandbox/donor-guide-bot:v1.0.0
```
