## Диаграмма обработки вопроса

```mermaid
sequenceDiagram
    actor Пользователь as Пользователь
    participant Telegram as Telegram API
    participant Обработчик as Обработчик вопросов
    participant QuestionRepo as QuestionRepository
    participant DB as База данных
    participant MetricService as MetricService
    participant ЯндексМетрика as Яндекс.Метрика

    Пользователь->>Telegram: Выбирает вопрос (callback)
    Telegram->>Обработчик: HTTPS-запрос с callback_data
    activate Обработчик

    Обработчик->>QuestionRepo: get_by_id(question_id)
    activate QuestionRepo
    QuestionRepo->>DB: SELECT * FROM questions WHERE id=?
    activate DB
    DB-->>QuestionRepo: Данные вопроса
    deactivate DB
    QuestionRepo-->>Обработчик: Question DTO
    deactivate QuestionRepo

    Обработчик->>MetricService: send_event(chat_id, question_title)
    activate MetricService
    MetricService->>ЯндексМетрика: HTTPS GET /watch/{counter_id}
    
    activate ЯндексМетрика
    ЯндексМетрика-->>MetricService: 200 OK
    deactivate ЯндексМетрика

    MetricService-->>Обработчик: void
    deactivate MetricService

    alt Есть изображение
        Обработчик->>Обработчик: Проверка answer_file_id

        alt file_id существует
            Обработчик->>Telegram: send_photo(file_id)
        else file_id отсутствует
            Обработчик->>Telegram: send_photo(file_path)
            Telegram-->>Обработчик: Новый file_id
            
            Обработчик->>QuestionRepo: update(question)
            activate QuestionRepo
            QuestionRepo->>DB: UPDATE questions...
            activate DB
            DB-->>QuestionRepo: Question DTO
            deactivate DB 
            QuestionRepo-->>Обработчик: Question DTO
            deactivate QuestionRepo
        end
    else Только текст
        Обработчик->>Telegram: send_message(text)
    end

    Telegram-->>Пользователь: Отображение ответа
    deactivate Обработчик
```
Диаграмма последовательности визуализирует детальный путь обработки запроса в Telegram-боте, когда пользователь выбирает определенный вопрос. Она показывает, как происходит взаимодействие между элементами системы: от нажатия на кнопку до получения ответа и фиксации события в Яндекс Метрике.
Начало процесса – нажатие пользователем на кнопку с нужным вопросом. Telegram передает callback-запрос на сервер, где работает обработчик. Затем выполняются следующие действия:

    1. Извлечение текста ответа из базы данных посредством QuestionRepository;
    
    2. Передача информации о событии в Яндекс Метрику через MetricService;
    
    3. Проверка наличия изображения в ответе;
    
        - При наличии сохраненного изображения (file_id) оно отправляется без дополнительной обработки;
        
        - В противном случае, изображение загружается и сохраняется в базе данных;
        
    4. Передача ответа конечному пользователю, в виде текста или изображения.

Данная схема позволяет наглядно представить цепочку вызовов и обмен данными между компонентами системы и внешними сервисами, что особенно полезно для понимания логики формирования ответа на запрос пользователя.


