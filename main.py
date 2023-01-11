# pythonProject7

# БОТ, ВЕДУЩИЙ TELEGRAM-КАНАЛ С РЕЦЕПТАМИ
# Бот получает список рецептов из файла и случайный рецепт (с рекламой!!!) через случайные период времени постит в канал.
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

bot = telebot.TeleBot(token)

# Адрес телеграм-канала, начинается с @
CHANNEL_NAME = channel
try:
    # Загружаем список с рекламными объявлениями из файла promotions.txt
    try:  # этот блок не прерывает работу программы
        p = open('promotions.txt', 'r', encoding='UTF-8')
        prom_list = p.read().split('\n\n\n')
    finally:
        p.close()  # и закрывает открытый файл если он не прочитался

    # Загружаем список рецептов1
    try:
        f = open('recipes1.txt', 'r', encoding='UTF-8')
        recipes1 = f.read().split('\n\n\n')
    finally:
        f.close()

    # Загружаем список рецептов2
    try:
        f = open('recipes2.txt', 'r', encoding='UTF-8')
        recipes2 = f.read().split('\n\n\n')
    finally:
        f.close()

    # Загружаем список рецептов3
    try:
        f = open('recipes3.txt', 'r', encoding='UTF-8')
        recipes3 = f.read().split('\n\n\n')
    finally:
        f.close()

    # Загружаем список рецептов4
    try:
        f = open('recipes4.txt', 'r', encoding='UTF-8')
        recipes4 = f.read().split('\n\n\n')
    finally:
        f.close()

    # Загружаем список рецептов5
    try:
        f = open('recipes5.txt', 'r', encoding='UTF-8')
        recipes5 = f.read().split('\n\n\n')
    finally:
        f.close()

    # Загружаем список рецептов6
    try:
        f = open('recipes6.txt', 'r', encoding='UTF-8')
        recipes6 = f.read().split('\n\n\n')
    finally:
        f.close()

    # Загружаем список рецептов7
    try:
        f = open('recipes7.txt', 'r', encoding='UTF-8')
        recipes7 = f.read().split('\n\n\n')
    finally:
        f.close()

    # Загружаем список рецептов8
    try:
        f = open('recipes8.txt', 'r', encoding='UTF-8')
        recipes8 = f.read().split('\n\n\n')
    finally:
        f.close()

    # Загружаем список рецептов9
    try:
        f = open('recipes9.txt', 'r', encoding='UTF-8')
        recipes9 = f.read().split('\n\n\n')
    finally:
        f.close()

    # Загружаем список рецептов10
    try:
        f = open('recipes10.txt', 'r', encoding='UTF-8')
        recipes10 = f.read().split('\n\n\n')
    finally:
        f.close()

    # Загружаем список утренних приветствий
    try:
        m = open('morning_text.txt', 'r', encoding='UTF-8')
        good_morning = m.read().split('\n\n')
    finally:
        m.close()
except FileNotFoundError:
    print("Невозможно открыть файл")
except:
    print("Ошибка при работе с файлами")


# Загружаем список вечерних пожеланий
# n = open('nigth_text.txt', 'r', encoding='UTF-8')
# good_night = n.read().split('\n\n')
# n.close()

def random_recipe():
    """
    Выдает случайный список рецептов из заданных
    :return: список рецептов
    """
    lst_nomber = random.randint(1, 10)
    if lst_nomber == 1:
        return recipes1
    elif lst_nomber == 2:
        return recipes2
    elif lst_nomber == 3:
        return recipes3
    elif lst_nomber == 4:
        return recipes4
    elif lst_nomber == 5:
        return recipes5
    elif lst_nomber == 6:
        return recipes6
    elif lst_nomber == 7:
        return recipes7
    elif lst_nomber == 8:
        return recipes8
    elif lst_nomber == 9:
        return recipes9
    else:
        return recipes10


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


def second_process(): #todo отразить в документации изменения
    """
    Посылаем случайный рецепт в чат.
    :return: Строка с рецептом.
    """
    work_bot_fl = True
    while work_bot_fl:
        current_date_time = datetime.datetime.now()
        now = current_date_time.time()  # текущее время
        morning = datetime.time(7, 32, 0)  # время начала работы бота
        night = datetime.time(22, 45, 0)  # время окончания работы бота todo уменьшить время до 1800

        if morning < now < night:  # если день
            print("Бот работает") # проверка бота todo
            time.sleep(random.randint(60, 7200))  # c 7 до 9 самое популярное время для постов todo
            promo = random.choice(prom_list)  # реклама
            recipes = random_recipe()  # выбираем случайный список рецептов
            answer = random.choice(recipes)  # случайный рецепт
            answer += '\n\n' + promo
            # таймер работы бота (от 1 до 5 часов)
            bot.send_message(CHANNEL_NAME, answer)
            time.sleep(random.randint(16200, 32400)) # один-два поста в день достаточно для дзен todo


if __name__ == '__main__':
    # Запускаем два процесса параллельно
    # p1 = Process(target=first_process, daemon=True)
    p2 = Process(target=second_process, daemon=True)
    # p1.start()
    p2.start()
    # p1.join()
    p2.join()
