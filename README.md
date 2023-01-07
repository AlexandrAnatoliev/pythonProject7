# pythonProject7

[Ru] БОТ, ВЕДУЩИЙ TELEGRAM-КАНАЛ С РЕЦЕПТАМИ

## Описание

Бот получает список рецептов из файла и случайный рецепт (с рекламой!!!) через случайные период времени постит в канал. Желает "Доброе
утро"
читателям канала

## Требования

* Установить внешние зависимости
* $ pip install -r requirements.txt
* Создать свой канал в Telegram, добавить в подписчики канала нашего бота и назначить его администратором канала с
  правом публиковать сообщения.
* Создать файл с рецептами recipes.txt и размесить в папке со скриптом бота.
* Создать файл morning_text.txt со списком утренних приветствий
* Создать файл config.py, в котором будут храниться токен для доступа к боту и адрес телеграм-канала (начинается с @) в
  виде

```python
token = "1234567890:ASDFGHH..."
channel = '@topjokes...'
```

## Где взять токен?

* https://xakep.ru/2021/11/28/python-telegram-bots/

## Подключаем модули

```python
import telebot
import random
import time
import datetime
import schedule
from multiprocessing import Process
from config import token, channel
```

## Примеры использования

#### Загружаем список рекламы, рецептов, утренних приветствий

Указываем название текстового файла с рецептами, 'r' - чтение текста, кодировку текта 'UTF-8'
Рецепты в текстовом файле разделены двумя пустыми строками (\n\n\n)

```python
# Загружаем список с рекламными объявлениями из файла promotions.txt
p = open('promotions.txt', 'r', encoding='UTF-8')
prom_list = p.read().split('\n\n\n')
p.close()

# Загружаем список рецептов
f = open('recipes1.txt', 'r', encoding='UTF-8')
recipes = f.read().split('\n\n\n')
f.close()

# Загружаем список утренних приветствий
m = open('morning_text.txt', 'r', encoding='UTF-8')
good_morning = m.read().split('\n\n')
m.close()
```

#### Выдает случайный список рецептов из заданных

```python
def random_recipe():
    lst_nomber = random.randint(1, 2)
    if lst_nomber == 1:
        return recipes1
    else:
        return recipes2
```

#### Выставляем время начала работы бота "morning" и окончания "night", чтобы сообщения не будили по ночам

```python
work_bot_fl = True
while work_bot_fl:
    current_date_time = datetime.datetime.now()
    now = current_date_time.time()  # текущее время
    morning = datetime.time(7, 3, 0)  # время начала работы бота
    night = datetime.time(22, 45, 0)  # время окончания работы бота
```

#### Посылаем случайную фразу из списка good_morning в канал CHANNEL_NAME

```python
def wish_morning():
    bot.send_message(CHANNEL_NAME, random.choice(good_morning))
```

#### Каждое утро "07:08" посылать сообщение в чат. ВАЖНО! формат времени "07:08", а не "7:08"!

```python
def first_process():
    schedule.every().day.at("07:08").do(wish_morning)
    # каждый вечер посылать сообщение в чат
    schedule.every().day.at("23:49").do(wish_evening)
    while True:
        schedule.run_pending()
        time.sleep(1)
```

#### Посылаются случайные рецепты через случайные периоды времени в диапазоне от 1  до 5 часов

```python
def second_process():
    work_bot_fl = True
    while work_bot_fl:
        current_date_time = datetime.datetime.now()
        now = current_date_time.time()  # текущее время
        morning = datetime.time(7, 32, 0)  # время начала работы бота
        night = datetime.time(22, 45, 0)  # время окончания работы бота

        if morning < now < night:  # если день
            promo = random.choice(prom_list)  # реклама
            recipes = random_recipe()  # выбираем случайный список рецептов
            answer = random.choice(recipes)  # случайный рецепт
            answer += '\n\n' + promo
            # таймер работы бота (от 1 до 5 часов)
            bot.send_message(CHANNEL_NAME, answer)
            time.sleep(random.randint(3600, 18000))
```

#### Запускаем два процесса параллельно

```python
if __name__ == '__main__':
    # Запускаем два процесса параллельно
    p1 = Process(target=first_process, daemon=True)
    p2 = Process(target=second_process, daemon=True)
    p1.start()
    p2.start()
    p1.join()
    p2.join()
```