# donor-guide-bot
Telegram-бот для ответов на вопросы по донорству

Разделы:
- [Описание](#описание)
- [Функционал](#функционал)
- [Установка и запуск приложения локально](#установка-и-запуск-приложения-локально)
- [Конфигурация приложения](#конфигурация-приложения)
- [Запуск PostgreSQL и pgAdmin в Docker-контейнерах](#запуск-postgresql-и-pgadmin-в-docker-контейнерах)
- [Работа с миграциями базы данных](#работа-с-миграциями-базы-данных)



## Описание
Данный Telegram-бот предназначен для автоматического ответа на вопросы, связанные с донорством крови и костного мозга. Проект разработан в рамках курсовой работы в НИУ ВШЭ (г. Пермь).

## Функционал
- Автоматические ответы на часто задаваемые вопросы.
- Поддержка категорий для удобной навигации:
  - Донорство крови
  - Донорство костного мозга
  - Контакты фонда
- Отправка текстовой информации, изображений, ссылок.
- Возможность задать свой вопрос.

## Установка и запуск приложения локально
### Предварительные требования
- Python 3.12
- Python venv

### Шаги установки
1. Клонируйте репозиторий:

    ```sh
    git clone https://github.com/hse-perm-sandbox/donor-guide-bot.git
    cd donor-guide-bot
    ```

2. Установите Python 3.12 и модуль `venv` (если они еще не установлены).

3. Создайте виртуальное окружение:

    ```sh
    python3 -m venv .venv
    ```

4. Активируйте виртуальное окружение:

    ```sh
    source .venv/bin/activate
    ```

5. Установите Poetry:

    ```sh
    pip install poetry
    ```

6. Установите зависимости проекта:

    ```sh
    poetry install
    ```

7.  Создайте .env файл с переменными окружения:

    ```
    LOG_LEVEL=WARNING
    TELEGRAM_TOKEN=SET_TOKEN_VALUE
    RESEND_CHAT_ID=SET_CHAT_ID
    POSTGRES_USER=postgres
    POSTGRES_PASSWORD=postgres
    POSTGRES_DB=postgres
    ```

8.  Запустите приложение:

    ```sh
    poetry run start
    ```

## Конфигурация приложения

Настройки приложения задаются через класс Settings, который использует библиотеку pydantic-settings для работы с переменными окружения и .env-файлом.

Основные параметры:
- LOG_LEVEL — уровень логирования (по умолчанию: WARNING).
- TELEGRAM_TOKEN — токен Telegram-бота.
- RESEND_CHAT_ID — ID чата для пересылки сообщений.
- POSTGRES_USER — имя пользователя для подключения к базе данных.
- POSTGRES_PASSWORD — пароль пользователя для подключения к базе данных.
- POSTGRES_DB — название базы данных.

Задать параметры приложения можно:
  - Через .env-файл в корне проекта:
    
    ```ini
    TELEGRAM_TOKEN=your_telegram_bot_token
    RESEND_CHAT_ID=12345
    ```

  - Через переменные окружения:
    ```sh
    export TELEGRAM_TOKEN="your_telegram_bot_token"
    ```

### Приоритеты загрузки

Настройки загружаются в следующем порядке:
1. Значения по умолчанию из класса Settings.
2. Переменные из файла .env.
3. Переменные окружения системы (имеют высший приоритет).

Файл .env игнорируется в Git (указан в .gitignore), чтобы избежать утечки чувствительных данных данных.

## Запуск PostgreSQL и pgAdmin в Docker-контейнерах
Для запуска PostgreSQL и pgAdmin используйте Docker Compose. Убедитесь, что у вас установлены Docker и Docker Compose.

1. Убедитесь, что в корне проекта присутствует и заполнен файл .env.
2. Убедитесь, что порты 5433 и 5434 свободны на вашем компьютере.
3. Запустите контейнеры:

```bash
docker compose -f docker-compose.local.yml up -d
```

Это команда:
- Запускает контейнеры PostgreSQL и pgAdmin.

После запуска:
- PostgreSQL будет доступен на localhost:5433.
- pgAdmin будет доступен на localhost:5434.
- Подключитесь к PostgreSQL через pgAdmin, используя:
    * Host: postgres
    * Port: 5432
    * Username: postgres
    * Password: postgres
    * Database: postgres

4. Запустите миграции для базы данных с помощью команды:

```bash
alembic upgrade head
```

### Остановка контейнеров
Чтобы остановить и удалить контейнеры, выполните:

```bash
docker compose -f docker-compose.local.yml down
```

Чтобы остановить и удалить контейнеры, а также удалить volumes с данными, выполните:

```bash
docker compose -f docker-compose.local.yml down -v
```

## Работа с миграциями базы данных
В проекте используется система миграций Alembic для управления изменениями структуры базы данных.

### Основные команды:
1. Создать новую миграцию:

    ```bash
    poetry run alembic revision --autogenerate -m "Описание изменений"
    ```

2. Применить миграции:

    ```bash
    poetry run alembic upgrade head
    ```
3. Откатить последнюю миграцию:

    ```bash
    poetry run alembic downgrade -1
    ```

4. Просмотреть текущую версию:

    ```bash
    poetry run alembic current
    ```

    ```

5. Сбросить все миграции и начать заново:

    ```bash
    poetry run alembic downgrade base && poetry run alembic upgrade head
    ```

Миграции проекта:
- Миграции хранятся в папке migrations/versions в виде Python-скриптов.
- Файл alembic.ini содержит базовые настройки.
- При изменении моделей SQLAlchemy:
    * Создайте миграцию (revision --autogenerate).
    * Проверьте сгенерированный код в migrations/versions/...py.
    * Примените изменения (upgrade head).


## Инициализация базы данных

Для заполнения базы данных вопросами и ответами о донорстве крови выполните команду:

```bash
python -m src.database.seeds.initial_data
```
