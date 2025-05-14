from telebot import types
from src.database.repositories.user import UserRepository
from src.database.repositories.user_question import UserQuestionRepository
from src.config import settings
from src.database.database import get_session
from src.schemas.user import UserBase
from src.schemas.user_question import UserQuestionBase
import logging
from email_validator import validate_email, EmailNotValidError
from src.handlers.keyboards import get_main_menu


logger = logging.getLogger(__name__)
user_data = {}

def register_user_question_handlers(bot):

    @bot.message_handler(func=lambda m: m.text == "Написать свой вопрос")
    def ask_question(message):
        msg = bot.send_message(
            message.chat.id, "📝 Пожалуйста, напишите ваш вопрос. (Отправьте одним сообщением)"
        )
        bot.register_next_step_handler(msg, process_question_text)
        user_data[message.chat.id] = {"state": "awaiting_question"}

    def process_question_text(message):
        user_data[message.chat.id]["question"] = message.text
        msg = bot.send_message(message.chat.id, "📧 Теперь укажите ваш email для обратной связи:")
        bot.register_next_step_handler(msg, process_email)

    def process_email(message):
        email = message.text.strip()

        try:
            valid = validate_email(email)
            email = valid.email
        except EmailNotValidError:
            msg = bot.send_message(
                message.chat.id,
                "❌ Email введён некорректно. Пожалуйста, попробуйте снова:"
            )
            bot.register_next_step_handler(msg, process_email)
            return

        user_data[message.chat.id]["email"] = message.text

        repo = UserRepository(next(get_session()))
        user = repo.create_or_update(
            UserBase.model_construct(
                telegram_chat_id=message.chat.id,
                telegram_username=bot.get_chat(message.chat.id).username,
                email=message.text,
            )
        )

        sent = True
        try:
            send_question_to_fund(message.chat.id)
        except Exception as error:
            logger.error(error)
            sent = False

        repo = UserQuestionRepository(next(get_session()))
        repo.create(
            UserQuestionBase.model_construct(
                question_text=user_data[message.chat.id]["question"],
                sent=sent,
                user_id=user.id,
            )
        )

        bot.send_message(
            message.chat.id,
            "✅ Ваш вопрос и контакты отправлены в фонд. Спасибо!",
            reply_markup=get_main_menu(),
        )

    def send_question_to_fund(chat_id):
        data = user_data.get(chat_id, {})
        question = data.get("question", "Не указан")
        email = data.get("email", "Не указан")
        user = bot.get_chat(chat_id)

        bot.send_message(
            settings.RESEND_CHAT_ID,
            f"❓ Новый вопрос от пользователя:\n"
            f"Имя: {user.first_name}\n"
            f"Username: @{user.username}\n"
            f"Email: {email}\n\n"
            f"Вопрос: {question}",
        )
