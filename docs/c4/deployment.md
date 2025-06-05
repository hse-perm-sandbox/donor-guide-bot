# Диаграмма развертывания
Диаграмма развертывания C4 показывает физическую инфраструктуру системы DonorGuide, включая расположение контейнеров на серверах и их взаимодействие, в том числе с внешними системами.

```mermaid
C4Deployment
    title Диаграмма развертывания системы DonorGuide

    Deployment_Node(cloud, "Облачный провайдер", "Облачная инфраструктура") {
        Deployment_Node(db_server, "Сервер баз данных", "Ubuntu 22.04 LTS") {
            Deployment_Node(postgres, "PostgreSQL", "PostgreSQL") {
                ContainerDb(db, "База данных", "PostgreSQL", "Хранит FAQ и<br> пользовательские вопросы ")
            }
        }
        
        Deployment_Node(app_server, "Сервер приложений", "Ubuntu 22.04 LTS") {
            Deployment_Node(docker, "Docker", "Docker Engine") {
                Container(bot, "Telegram-бот", "Python + telebot", "Отвечает на вопросы о донорстве,<br> перенаправляет вопросы <br>сотрудникам фонда")
            }
        }
    }

    System_Ext(telegram, "Telegram API", "Официальное API Telegram")

    Rel(bot, db, "Читает ответы/Обновляет лог вопросов", "TCP/IP (SQL)")
    Rel(bot, telegram, "Отправка/получение сообщений", "HTTPS")

    UpdateRelStyle(bot, telegram, $offsetX="-90", $offsetY="-120")
    UpdateRelStyle(bot, db, $offsetX="-90", $offsetY="70")
    UpdateLayoutConfig($c4ShapeInRow="2", $c4BoundaryInRow="2")
```

## Описание узлов:
1. Сервер баз данных:
  - Виртуальная машина с Ubuntu 22.04 LTS, арендованная у облачного провайдера
  - Установлен PostgreSQL 17
  - Хранит данные приложения (FAQ, логи вопросов)
2. Сервер приложений:
  - Виртуальная машина с Ubuntu 22.04 LTS, арендованная у облачного провайдера
  - Устновлен Docker 28
  - В контейнере работает Python-приложение бота

# Особенности развертывания:
- Используются два изолированных сервера для БД и приложения
- Все компоненты развернуты в облачной инфраструктуре
