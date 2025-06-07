# Диаграмма Контекста
 Диаграмма показывает систему в масштабе ее взаимодействия с пользователями и другими системами.

```mermaid
C4Context
    title Система информирования о донорстве

    Enterprise_Boundary(Фонд, "Благотворительный фонд 'Advita'") {
        System(DonorBot, "Telegram-бот DonorGuide", "Отвечает на вопросы о донорстве")
        Person(Сотрудник, "Сотрудник фонда", "Обновляет базу знаний")
    }

    Person(Донор, "Потенциальный донор")
    System_Ext(Telegram, "Платформа Telegram")
    System_Ext(Metrica, "Яндекс Метрика", "Система аналитики")

    Rel(Донор, Telegram, "Задает вопросы через бота")
    Rel(Сотрудник, Telegram, "Получает вопросы от пользователей")
    Rel(DonorBot, Telegram, "Работает внутри мессенджера")
    Rel(Telegram, DonorBot, "Переадресует запросы")
    Rel(DonorBot, Metrica, "Отправляет события посещения")
    Rel(Сотрудник, Metrica, "Просматривает аналитику")


    UpdateRelStyle(Донор, Telegram, $offsetY="20", $offsetX="-40")
    UpdateRelStyle(Сотрудник, Telegram, $offsetY="100", $offsetX="40")
    UpdateRelStyle(DonorBot, Telegram, $textColor="blue", $lineColor="blue", $offsetY="10", $offsetX="-220")
    UpdateRelStyle(Telegram, DonorBot, $offsetY="10", $offsetX="20")
    UpdateRelStyle(DonorBot, Metrica, $textColor="green", $lineColor="green", $offsetY="-20")
    UpdateRelStyle(Сотрудник, Metrica, $textColor="blue", $lineColor="blue", $offsetY="-60", $offsetX="30")
```

## Описание компонентов:
1. DonorGuide Bot. Telegram-бот, отвечающий на вопросы о донорстве крови и костного мозга.
2. Сотрудник фонда. Администрирует базу знаний: добавляет новые вопросы/ответы и обрабатывает индивидуальные запросы.
3. Потенциальный донор. Основной пользователь, взаимодействующий с ботом для получения информации.

## Внешние системы:
1. Telegram — платформа для работы бота, передаёт запросы от пользователей в DonorGuide и отображает ответы.
2. Яндекс Метрика — система аналитики, в которую бот отправляет события взаимодействия.

## Взаимодействия:
1. Донор задаёт вопрос через Telegram.
2. Telegram передаёт запрос в DonorGuide.
3. DonorGuide отправляет ответ или пересылает вопрос сотруднику.
4. DonorGuide фиксирует события в Яндекс Метрике.
5. Сотрудник анализирует поведение пользователей через интерфейс Яндекс Метрики.
