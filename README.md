# pythonProject1

[Ru] БОТ, ВЕДУЩИЙ TELEGRAM-КАНАЛ С АНЕКДОТАМИ

## Описание

Бот получает список анекдотов из файла и каждый час постит в канал один из этих анекдотов. Желает "Доброе утро" и "
спокойной ночи" читателям канала

## Требования

* Установить внешние зависимости
* $ pip install -r requirements.txt
* Создать свой канал в Telegram, добавить в подписчики канала нашего бота и назначить его администратором канала с
  правом публиковать сообщения.
* Создать файл с анекдотами fun.txt и размесить в папке со скриптом бота.
* Создать файл morning_text.txt со списком утренних приветствий
* Создать файл nigth_text.txt со списком вечерних пожеланий
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

#### Загружаем список шуток, утренних приветствий и вечерних пожеланий

Указываем название текстового файла с шутками, 'r' - чтение текста, кодировку текта 'UTF-8'

```python
# Загружаем список шуток
f = open('fun.txt', 'r', encoding='UTF-8')
jokes = f.read().split('\n')
f.close()

# Загружаем список утренних приветствий
m = open('morning_text.txt', 'r', encoding='UTF-8')
good_morning = m.read().split('\n')
m.close()

# Загружаем список вечерних пожеланий
n = open('nigth_text.txt', 'r', encoding='UTF-8')
good_night = n.read().split('\n')
n.close()
```

#### Выставляем время начала работы бота "morning" и окончания "night", чтобы сообщения не будили по ночам

```python
work_bot_fl = True
while work_bot_fl:
    current_date_time = datetime.datetime.now()
    now = current_date_time.time()  # текущее время
    morning = datetime.time(7, 3, 0)  # время начала работы бота
    night = datetime.time(23, 45, 0)  # время окончания работы бота
```

#### Посылаем случайную фразу из списка good_morning в канал CHANNEL_NAME

```python
def wish_morning():
    bot.send_message(CHANNEL_NAME, random.choice(good_morning))
```

#### Посылаем случайную фразу из списка good_night в канал CHANNEL_NAME

```python
def wish_evening():
    bot.send_message(CHANNEL_NAME, random.choice(good_night))
```

#### Каждое утро "07:08" и каждый вечер "23:49" посылать сообщение в чат. ВАЖНО! формат времени "07:08", а не "7:08"!

```python
def first_process():
    schedule.every().day.at("07:08").do(wish_morning)
    # каждый вечер посылать сообщение в чат
    schedule.every().day.at("23:49").do(wish_evening)
    while True:
        schedule.run_pending()
        time.sleep(1)
```

#### Посылаются случайные шутки через случайные периоды времени в диапазоне от 1 минуты до 4 часов

```python
def second_process():
    work_bot_fl = True
    while work_bot_fl:
        current_date_time = datetime.datetime.now()
        now = current_date_time.time()  # текущее время
        morning = datetime.time(7, 3, 0)  # время начала работы бота
        night = datetime.time(23, 45, 0)  # время окончания работы бота

        if morning < now < night:  # если день
            # таймер работы бота (от 1 до 3 часов)
            bot.send_message(CHANNEL_NAME, random.choice(jokes))
            time.sleep(random.randint(3600, 10800))
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