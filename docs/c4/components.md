# Диаграмма компонентов
Диаграмма компонентов показывает внутреннюю структуру контейнера, разбивая его на логические компоненты (модули, классы, сервисы) и связи между ними.

```mermaid
C4Component
    title Диаграмма компонентов Telegram-бота DonorGuide 

    System_Boundary(ext, "Внешние системы") {
        System_Ext(telegram, "Telegram API", "Официальное API Telegram")
    }
    
    System_Boundary(boundary, "Система DonorGuide") {
        Container_Boundary(bot_container, "Контейнер: Telegram-бот") {

            Boundary(handlers, "Обработчики сообщений") {
                Component(handler, "Обработчик вопросов", "Python", "Обрабатывает входящие сообщения<br>и callback-запросы")
            }

            Boundary(repos, "Репозитории для работы с БД") {
                Component(user_repo, "UserRepository", "Python", "Работает с данными пользователей")
                Component(question_repo, "UserQuestionRepository", "Python", "Работает с вопросами пользователей")
            }
        }
        Container_Boundary(db_container, "Контейнер: База данных") {
            ContainerDb(db, "База данных", "PostgreSQL", "Хранит пользователей и вопросы")
        }
    }

    Rel(handler, user_repo, "Получает/обновляет данные пользователей")
    UpdateRelStyle(handler, user_repo, $offsetX="-40", $offsetY="40")
    Rel(handler, question_repo, "Сохраняет вопросы")
    UpdateRelStyle(handler, question_repo, $offsetX="-70", $offsetY="40")
    Rel(user_repo, db, "Чтение/запись", "SQL")
    UpdateRelStyle(user_repo, db, $offsetX="0", $offsetY="-40")
    Rel(question_repo, db, "Чтение/запись", "SQL")
    Rel(handler, telegram, "Отправка/получение сообщений", "HTTPS")

    UpdateLayoutConfig($c4ShapeInRow="3", $c4BoundaryInRow="3")
```

Диаграмма отображает внутреннюю структуру системы  на уровне компонентов. Система разделена на два основных контейнера:
1. Контейнер Telegram-бота включает:
  - Обработчики сообщений (принимают и маршрутизируют запросы).
  - Репозитории (работают с данными через БД).
2. Контейнер базы данных:
  - PostgreSQL (хранит данные пользователей и их вопросы)

Ключевые взаимодействия:
- Бот обменивается сообщениями через Telegram API.
- Обработчик координирует работу с данными через репозитории.
- Репозитории работают с базой данных.