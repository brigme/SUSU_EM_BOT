import telebot
import logging
from datetime import datetime
import os
from dotenv import load_dotenv


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def main():
    load_dotenv()

    BOT_TOKEN = os.getenv('BOT_TOKEN')
    CHAT_ID = os.getenv('CHAT_ID')

    question = name_polly()
    options_1, options_2, options_3 = text_polly()
    send_telegram_poll(BOT_TOKEN, CHAT_ID, question, options_1, options_2, options_3)


def name_polly():
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    question = f"Занимаем очередь на пару от: {current_time}"

    return question


def text_polly():
    options_1 = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10"]
    options_2 = ["11", "12", "13", "14", "15", "16", "17", "18", "19", "20"]
    options_3 = ["21", "22", "23", "24", "25", "26", "27", "28", "29", "30"]

    return options_1, options_2, options_3


def send_telegram_poll(BOT_TOKEN, CHAT_ID, question, options_1, options_2, options_3, poll_type="regular",
                       is_anonymous=False, allows_multiple_answers=False, correct_option_id=None):
    try:
        if not BOT_TOKEN or not CHAT_ID:
            logger.error("Не указаны BOT_TOKEN или CHAT_ID в .env файле")
            return False

        bot = telebot.TeleBot(BOT_TOKEN)

        if len(options_1) < 2 or len(options_2) < 2 or len(options_3) < 2:
            logger.error("Для опроса нужно как минимум 2 варианта ответа")
            return False

        if len(options_1) > 10 or len(options_2) > 10 or len(options_3) > 10:
            logger.error("Максимум 10 вариантов ответа")
            options_1 = options_1[:10]  # Обрезаем до 10 вариантов
            options_2 = options_2[:10]
            options_3 = options_3[:10]

        poll_params = {
            'chat_id': CHAT_ID,
            'question': question,
            'options': options_1,
            'is_anonymous': is_anonymous,
            'allows_multiple_answers': allows_multiple_answers
        }

        sent_poll = bot.send_poll(**poll_params)

        logger.info(f"Опрос успешно отправлен в чат {CHAT_ID}")
        logger.info(f"ID опроса: {sent_poll.poll.id}")

        poll_params = {
            'chat_id': CHAT_ID,
            'question': question,
            'options': options_2,
            'is_anonymous': is_anonymous,
            'allows_multiple_answers': allows_multiple_answers
        }

        sent_poll = bot.send_poll(**poll_params)

        logger.info(f"Опрос успешно отправлен в чат {CHAT_ID}")
        logger.info(f"ID опроса: {sent_poll.poll.id}")

        poll_params = {
            'chat_id': CHAT_ID,
            'question': question,
            'options': options_3,
            'is_anonymous': is_anonymous,
            'allows_multiple_answers': allows_multiple_answers
        }

        sent_poll = bot.send_poll(**poll_params)

        logger.info(f"Опрос успешно отправлен в чат {CHAT_ID}")
        logger.info(f"ID опроса: {sent_poll.poll.id}")

        return True

    except Exception as e:
        logger.error(f"Ошибка при отправке опроса: {e}")
        return False

if __name__ == '__main__':
    main()