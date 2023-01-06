# pythonProject7

# БОТ, ВЕДУЩИЙ TELEGRAM-КАНАЛ С РЕЦЕПТАМИ
# Бот получает список рецептов из файла и случайный рецепт через случайные период времени постит в канал.
# Для этого нам нужно создать свой канал в Telegram,
# добавить в подписчики канала нашего бота и назначить его администратором канала с правом публиковать сообщения.
# Файл с анекдотами должен лежать в папке data рядом со скриптом бота.

# $ pip install schedule - установить внешние зависимости

import telebot
import random
import time
import datetime
import schedule
from multiprocessing import Process

from config import token, channel

# Создаем бота
bot = telebot.TeleBot(token)

# Адрес телеграм-канала, начинается с @
CHANNEL_NAME = channel

# Загружаем список рецептов1
f = open('recipes1.txt', 'r', encoding='UTF-8')
recipes1 = f.read().split('\n\n\n')
f.close()

# Загружаем список рецептов2
f = open('recipes2.txt', 'r', encoding='UTF-8')
recipes2 = f.read().split('\n\n\n')
f.close()

# Загружаем список утренних приветствий
m = open('morning_text.txt', 'r', encoding='UTF-8')
good_morning = m.read().split('\n\n')
m.close()


# Загружаем список вечерних пожеланий
# n = open('nigth_text.txt', 'r', encoding='UTF-8')
# good_night = n.read().split('\n\n')
# n.close()

def random_recipe():
    """
    Выдает случайный список рецептов из заданных
    :return: список рецептов
    """
    lst_nomber = random.randint(1, 2)
    if lst_nomber == 1:
        return recipes1
    else:
        return recipes2


def wish_morning():
    """
    Посылает случайную фразу из списка good_morning в канал CHANNEL_NAME
    :return: строка с утренним пожеланием
    """
    bot.send_message(CHANNEL_NAME, random.choice(good_morning))


# def wish_evening():
#    """
#    Посылает случайную фразу из списка good_night в канал CHANNEL_NAME
#    :return:
#    """
#    bot.send_message(CHANNEL_NAME, random.choice(good_night))


def first_process():
    """
    Каждое утро "7:08" и каждый вечер "23:49" посылать сообщение в чат.
    :return:
    """
    schedule.every().day.at("07:08").do(wish_morning)
    # каждый вечер посылать сообщение в чат
    # schedule.every().day.at("23:49").do(wish_evening)
    while True:
        schedule.run_pending()
        time.sleep(1)


def second_process():
    """
    Посылаем случайный рецепт в чат.
    :return: Строка с рецептом.
    """
    work_bot_fl = True
    while work_bot_fl:
        current_date_time = datetime.datetime.now()
        now = current_date_time.time()  # текущее время
        morning = datetime.time(7, 32, 0)  # время начала работы бота
        night = datetime.time(23, 45, 0)  # время окончания работы бота

        if morning < now < night:  # если день
            recipes = random_recipe()  # выбираем случайный список рецептов
            # таймер работы бота (от 1 до 3 часов)
            bot.send_message(CHANNEL_NAME, random.choice(recipes))
            time.sleep(random.randint(3600, 10800))


if __name__ == '__main__':
    # Запускаем два процесса параллельно
    p1 = Process(target=first_process, daemon=True)
    p2 = Process(target=second_process, daemon=True)
    p1.start()
    p2.start()
    p1.join()
    p2.join()
