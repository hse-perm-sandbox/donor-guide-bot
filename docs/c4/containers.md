# Диаграмма контейнеров
Диаграмма контейнеров C4 показывает высокоуровневую архитектуру системы, выделяя основные подсистемы внутри границ рассматриваемой системы и их взаимодействие с внешними системами.

```mermaid
C4Container
    title Диаграмма контейнеров системы DonorGuide

    System_Boundary(boundary, "Система DonorGuide") {
        Container(bot, "Telegram-бот", "Python + telebot", "Отвечает на вопросы <br>о донорстве, <br>перенаправляет вопросы <br>сотрудникам")
        ContainerDb(db, "База данных", "PostgreSQL", "Хранит FAQ и <br>пользовательские вопросы")
    }
    
    System_Ext(telegram, "Telegram API", "Официальное API Telegram")

    Rel(bot, db, "Читает ответы/Обновляет лог вопросов", "SQL")
    Rel(bot, telegram, "Отправка/получение сообщений", "HTTPS")

    UpdateRelStyle(bot, telegram, $offsetY="-40")
    UpdateRelStyle(bot, db, $offsetY="50")
    UpdateLayoutConfig($c4ShapeInRow="2", $c4BoundaryInRow="1")
```

## Описание контейнеров:
1. Telegram-бот (Python + telebot):
- Ответы на вопросы о донорстве крови.
- Прием обращений пользователей и перенаправление сотрудникам фонда.
2. База данных (PostgreSQL):
- Содержит структурированные FAQ.
- Хранит историю обращений.

## Внешние системы:
1. Telegram — платформа для работы бота. Обеспечивает коммуникацию с пользователями.