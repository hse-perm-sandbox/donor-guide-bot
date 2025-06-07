# Диаграмма компонентов
Диаграмма компонентов показывает внутреннюю структуру контейнера, разбивая его на логические компоненты (модули, классы, сервисы) и связи между ними.

```mermaid
C4Component
    title Диаграмма компонентов Telegram-бота DonorGuide 

    System_Boundary(ext, "Внешние системы") {
        System_Ext(telegram, "Telegram API", "Официальное API Telegram")
        System_Ext(metrica, "Яндекс Метрика", "Система аналитики")
    UpdateLayoutConfig($c4BoundaryInRow="1")
    }
    
    System_Boundary(boundary, "Система DonorGuide") {
        Container_Boundary(bot_container, "Контейнер: Telegram-бот") {

            Boundary(handlers, "Обработчики сообщений") {
                Component(user_question, "UserCallbackHandler", "Python", "Обрабатывает вопросы пользователей")
                Component(folder_handler, "FolderCallbackHandler", "Python", "Обрабатывает выбор папки<br>и отображает подкаталоги и вопросы")
                Component(question_handler, "QuestionCallbackHandler", "Python", "Показывает ответ на выбранный вопрос")
            }

            Boundary(repos, "Репозитории для работы с БД") {
                Component(user_repo, "UserRepository", "Python", "Работает с данными пользователей")
                Component(user_question_repo, "UserQuestionRepository", "Python", "Работает с вопросами пользователей")
                Component(question_repo, "QuestionRepository", "Python", "Хранит частозадаваемые вопросы<br>и ответы на них")
                Component(folder_repo, "FolderRepository", "Python", "Хранит названия папок и их зависимости")
            }
        }
        Container_Boundary(db_container, "Контейнер: База данных") {
            ContainerDb(db, "База данных", "PostgreSQL", "Хранит пользователей и вопросы")
        }
    }

    Rel(user_question, user_repo, "Получает/обновляет данные пользователей")
    UpdateRelStyle(user_question, user_repo, $offsetX="-40", $offsetY="40")
    Rel(user_question, user_question_repo, "Сохраняет вопросы")
    UpdateRelStyle(user_question, user_question_repo, $offsetX="-70", $offsetY="40")
    Rel(user_repo, db, "Чтение/запись", "SQL")
    UpdateRelStyle(user_repo, db, $offsetX="0", $offsetY="-40")
    Rel(user_question_repo, db, "Чтение/запись", "SQL")
    UpdateRelStyle(user_question_repo, db, $offsetX="-70")
    Rel(user_question, telegram, "Отправка/получение сообщений", "HTTPS")
    UpdateRelStyle(user_question, telegram, $offsetX="-50", $offsetY="-40")

    Rel(folder_handler, telegram, "Обрабатывает выбор папки", "HTTPS")
    UpdateRelStyle(folder_handler, telegram, $offsetX="-50", $offsetY="-30")
    Rel(folder_handler, folder_repo, "Получает вложенные папки")
    UpdateRelStyle(folder_handler, folder_repo, $offsetX="60", $offsetY="70")
    Rel(folder_handler, question_repo, "Получает вопросы")
    
    Rel(question_handler, telegram, "Отправляет ответ", "HTTPS")
    UpdateRelStyle(question_handler, telegram, $offsetX="-20", $offsetY="-50")
    Rel(question_handler, question_repo, "Получает вопрос")
    UpdateRelStyle(question_handler, question_repo, $offsetX="0", $offsetY="-20")
    
    Rel(folder_handler, metrica, "Отправляет событие", "HTTPS")
    UpdateRelStyle(folder_handler, metrica, $textColor="blue", $lineColor="blue", $offsetX="-50", $offsetY="0")
    Rel(user_question, metrica, "Отправляет событие", "HTTPS")
    UpdateRelStyle(user_question, metrica, $textColor="blue", $lineColor="blue",  $offsetY="10")
    Rel(question_repo, db, "Чтение вопросов", "SQL")
    Rel(folder_repo, db, "Чтение папок", "SQL")
    UpdateRelStyle(question_repo, db, $offsetY="0", $offsetX="-90")
    UpdateRelStyle(folder_repo, db, $offsetY="-40", $offsetX="-60")





    UpdateLayoutConfig($c4ShapeInRow="1", $c4BoundaryInRow="3")
```

Диаграмма отображает внутреннюю структуру системы  на уровне компонентов. Система разделена на два основных контейнера:
1. Контейнер Telegram-бота содержит два логических блока:

    - Обработчики (handlers) — принимают callback-запросы и маршрутизируют их:
        - UserCallbackHandler: реагирует на вопросы пользователей;
        - FolderCallbackHandler: обрабатывает выбор папки и отображает вложения;
        - QuestionCallbackHandler: показывает ответ на выбранный вопрос.

    - Репозитории (repos) — получают и сохраняют данные в базу:

        - UserRepository: сохраняет и извлекает информацию о пользователях Telegram;
        - UserQuestionRepository: регистрирует вопросы, которые пользователи задают вручную;
        - QuestionRepository: предоставляет доступ к базе часто задаваемых вопросов и их ответов;
        - FolderRepository: управляет иерархией категорий и подкатегорий вопросов.

2. Контейнер базы данных
    - PostgreSQL — централизованное хранилище всех данных пользователей, вопросов и структуры папок.

Взаимодействие с внешними системами
- Telegram API — для отправки/получения сообщений и callback-запросов.
- Яндекс Метрика — получает события взаимодействия пользователей для аналитики.
