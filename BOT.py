#!/usr/bin/env python3

#=================================================================
# v1.0   Бот работает, принимает и отвечает на базовые сообщения
# v1.1   Добавлена тестовая функция с запросом к сайту погоды
# v1.2   Добавлена возможность взаимодействия с postgresql14
# v1.2.1 Bugfix
# v1.3   Регистрация без выдачи прав, /stop bot убийством процесса на хосте
#
#
#
#
#Текущие задачи:
#=================================================================
#Добавить возможность создания пользователя в бд с нужными правами
#Добавить выдачу прав на бота для пользователя при регистрации
#Добавить возможность удаления пользователя бота
#Добавить мониторинги графаны
#Добавить возможность запуска с параметрами командной строки
#Добавить возможнсть использования переменных окружения
#Добавить логирование
#Добавить лог ошибок отдельно




import random
import pyrogram
import aiogram
import aiohttp
import requests
import sys
import os
#import json
#import time
import platform
import logging
import psycopg2

TOKEN = '5449810276:AAGWm4kJ6FAWtNqZ2Y-VZxsPwEtSHXgWWGs'
PID = str(os.system("lsof -t /LOGS/BOT/TG_BOT.log"))
THIS_BOT_CHAT_ID = 800772053
UserAgents = [
    'Mozilla/5.0 (Linux; U) Opera 6.02 [en]',
    'Mozilla/4.0 (compatible; MSIE 5.0; Windows NT 4.0) Opera 6.02 [en]',
    'Mozilla/4.0 (compatible; MSIE 5.0; Windows 95) Opera 6.02 [en]',
    'Mozilla/4.0 (compatible; MSIE 5.0; Windows 95) Opera 6.02 [de]',
    'Mozilla/4.0 (compatible; MSIE 5.0; Windows 2000) Opera 6.02 [en]',
    'Mozilla/4.0 (compatible; MSIE 5.0; Linux 2.4.20-686 i686) Opera 6.02 [en]',
    'Mozilla/4.0 (compatible; MSIE 5.0; Linux 2.4.18-4GB i686) Opera 6.02 [en]',
    'Opera/6.02 (Windows NT 4.0; U) [de]',
    'Opera/6.01 (X11; U; nn)',
    'Opera/6.01 (Windows XP; U) [de]',
    'Opera/6.01 (Windows 98; U) [en]',
    'Opera/6.01 (Windows 98; U) [de]',
    'Opera/6.01 (Windows 2000; U) [en]',
    'Opera/6.01 (Windows 2000; U) [de]',
    'Mozilla/5.0 (Windows 2000; U) Opera 6.01 [en]',
    'Mozilla/5.0 (Windows 2000; U) Opera 6.01 [de]',
    'Mozilla/4.78 (Windows 2000; U) Opera 6.01 [en]',
    'Mozilla/4.0 (compatible; MSIE 5.0; Windows XP) Opera 6.01 [it]',
    'Mozilla/4.0 (compatible; MSIE 5.0; Windows XP) Opera 6.01 [et]',
    'Mozilla/4.0 (compatible; MSIE 5.0; Windows XP) Opera 6.01 [de]',
    'Mozilla/4.0 (compatible; MSIE 5.0; Windows NT 4.0) Opera 6.01 [en]',
    'Mozilla/4.0 (compatible; MSIE 5.0; Windows NT 4.0) Opera 6.01 [de]',
    'Mozilla/4.0 (compatible; MSIE 5.0; Windows ME) Opera 6.01 [en]',
    'Mozilla/4.0 (compatible; MSIE 5.0; Windows ME) Opera 6.01 [de]',
    'Mozilla/4.0 (compatible; MSIE 5.0; Windows 98) Opera 6.01 [it]',
    'Mozilla/4.0 (compatible; MSIE 5.0; Windows 98) Opera 6.01 [fr]',
    'Mozilla/4.0 (compatible; MSIE 5.0; Windows 98) Opera 6.01 [en]',
    'Mozilla/4.0 (compatible; MSIE 5.0; Windows 98) Opera 6.01 [de]'
]
Proxies = [
    '203.30.191.202	80',
    '203.13.32.221	80',
    '203.24.102.56      80',
    '185.162.230.228    80',
    '203.23.104.37	80',
    '45.14.174.140	80',
    '173.245.49.118	80',
    '45.12.31.206	80',
    '172.67.254.148	80',
    '172.67.181.40	80'
]


try:
    BOT = aiogram.Bot(token=TOKEN,
                      connections_limit=10,
                      validate_token=True,
                      timeout=50,
                      )
except Exception as ex:
    print("Error while initializing BOT\n", ex)
    if ex == 'aiogram.utils.exceptions.ValidationError':
        print('ERROR IN TOKEN')
DISPATCHER = aiogram.Dispatcher(BOT)
logging.basicConfig(level=logging.INFO)
MINIMAL_PY_VERSION = (3, 7)
if sys.version_info < MINIMAL_PY_VERSION:
    raise RuntimeError('aiogram works only with Python {}+'.format('.'.join(map(str, MINIMAL_PY_VERSION))))


class SysInfo:
    @property
    def os(self) -> str:
        return platform.platform()

    @property
    def python_implementation(self) -> str:
        return platform.python_implementation()

    @property
    def python(self) -> str:
        return sys.version.replace('\n', '')

    @property
    def aiogram(self) -> str:
        return aiogram.__version__

    @property
    def api(self) -> str:
        return aiogram.__api_version__

    @property
    def aiohttp(self) -> str:
        return aiohttp.__version__

    @property
    def requests(self) -> str:
        return requests.__version__

    @property
    def sys(self) -> str:
        return requests.__version__

    def collect(self) -> str:
        yield "Версии установленный пакетов и информация о хосте: \n"
        yield f'aiohttp: {self.aiohttp}'
        yield f'api: {self.api}'
        yield f'aiogram: {self.aiogram}'
        yield f'python: {self.python}'
        yield f'os: {self.os}'
        yield f'python_implementation: {self.python_implementation}'
        yield f'sys: {self.sys}'
        yield f'requests: {self.requests}'

    def __str__(self) -> str:
        return '\n'.join(self.collect())


@DISPATCHER.message_handler(
    aiogram.dispatcher.filters.Command(['help'], ignore_case=True, ignore_mention=False, ignore_caption=True))
async def get_help(message: aiogram.dispatcher.filters.Command) -> None:
    """ Команда /help дает описание допустимых команд """

    print("DEBUG_MESSAGE_FROM_HELP")
    await message.answer("Допустимые команды: \n "
                         "1) weather (CITY) \n "
                         "2) /система \n "
                         "3) /delete - удаляет последнее сообщение \n"
                         "4) /__all_users \n"
                         "5) /stop \n"
                         "6) /reg - регистрация пользователя \n"
                         "7) /alert \n"
                         "8) /postgres - тест запрос к БД")


async def send_alert_message(message: aiogram.dispatcher.filters.Command) -> None:
    """ Отправляет сообщение в чат + контакт для связи """

    await BOT.send_message(THIS_BOT_CHAT_ID, 'TEST_ALERT_MESSAGE')
    await BOT.send_contact(THIS_BOT_CHAT_ID, '89163345378', 'first_name', 'last_name')


@DISPATCHER.message_handler(
    aiogram.dispatcher.filters.Command(['stop'], ignore_case=True, ignore_mention=False, ignore_caption=True))
async def stop_bot(message: aiogram.dispatcher.filters.Command) -> None:
    """ Команда /stop останавливает бота """

    await message.answer(f"DEBUG_MESSAGE_FROM_STOP_BOT, PID: {PID}, PID_TYPE: {type(PID)}")
    try:
        if BOT:
            await message.answer(f"Бот \n {await BOT.get_me()} \n будет отстановлен!")
            #await BOT.close()
            await os.system(f"kill -9 {PID}")
            if not os.system(f"ps -ef | grep {PID}"):
                await message.answer(f"Процесс {PID} успешно остановлен \n")
                await message.answer("Бот остановлен")
            else:
                await message.answer(f"Процесс {PID} НЕ остановлен, проверьте на хосте и при необходимости остановите вручную")
        else:
            print("BOT STOPPED ALREADY")
    except Exception as ex:
        await message.answer(f"EXCEPTION {ex} OCCURED!!!")


# !!!!!! Подразумевается что при первом входе пользователя в бота, ему доступна только команда регистрации в нем, реализуем через проверку в обработчике сообщений !!!!!!!
@DISPATCHER.message_handler(commands=['reg'], commands_prefix='!/')
async def registrating_user_for_tg_bot(message: aiogram.types.Message) -> None:
    """ Функция регистарции и выдачи прав новому пользователю. Записывает его информацию в таблицу в БД postgresql """

    # Пользователь должен создаваться только на БОЕВОЙ БД, для этого нужна дополнительная проверка
    INSERT_NEW_USER_QUERY_WITH_DEFAULT_GRANTS = f"insert into bot_users (user_id,can_send_media_messages,can_send_other_messages,can_send_polls,can_add_web_page_prage_previews,can_change_info,can_invite_users,date_created) values ({message.from_user.id}, 'YES', 'NO', 'YES', 'NO', 'NO', 'NO', '2022-12-03' );"


    SELECT_USER_QUERY = f'SELECT user_id from bot_users where user_id = {message.from_user.id};'
    count = 0
    #SELECT_USER_QUERY = 'SELECT user_id from bot_users;'
    print("DEBUG_MESSAGE_FROM_registrating_user_for_tg_bot")
    connection = connect_postgres('192.168.56.113')
    try:
        with connection.cursor() as cursor:
            # Проверям есть ли юзер
            cursor.execute(SELECT_USER_QUERY)
            for is_user_in_allowed in cursor:
                count += 1
                await message.answer(f'{is_user_in_allowed}')
                print("DEBUG AFTER SELECT ", is_user_in_allowed)
            # Если пользователя нет в таблице, т.e. нам вернули пустой кортеж
            try:
                if count == 0:
                    # То добавляем его с дефолтынми правами
                    cursor.execute(INSERT_NEW_USER_QUERY_WITH_DEFAULT_GRANTS)
                    connection.commit()
                    await BOT.restrict_chat_member(message.chat.id, message.from_user.id, pyrogram.types.ChatPermissions(can_send_messages=True,
                                                                                                                         can_send_media_messages=False,
                                                                                                                         can_send_other_messages=True,
                                                                                                                         can_send_polls=False,
                                                                                                                         can_add_web_page_previews=False,
                                                                                                                         can_change_info=False,
                                                                                                                         can_invite_users=False,
                                                                                                                         can_pin_messages=False))
                    # Проверяем что юзер добавлен
                    cursor.execute(SELECT_USER_QUERY)
                    for is_user_in_allowed in cursor:
                        count += 1
                    if count != 0:
                        await message.reply(f'Я бот. Приятно познакомиться,{message.from_user.first_name} \n '
                                            f'Доступ к отправке сообщений предоставлен \n'
                                            f'Напиши /help чтобы увидеть команды')
                    else:
                        await message.reply(f'Ошибка при добавлении пользователя {message.from_user.first_name}')
                # Если юзер есть то кидаем привет
                else:
                    await message.reply(f'Привет {message.from_user.first_name} \n '
                                       f'Напиши /help чтобы увидеть команды')
                    count = 0
            except Exception as reg_INSERT_NEW_USER_QUERY_exception:
                print(f"Ошибка при выполнени вставки значений в таблицу postgres.telegram_users: {reg_INSERT_NEW_USER_QUERY_exception}")
    except Exception as reg_SELECT_USER_QUERY_exception:
        print(f"Ошибка при выполнении запроса SELECT_USER: {reg_SELECT_USER_QUERY_exception}")
    finally:
        connection.close()


@DISPATCHER.message_handler(content_types=['text'])
async def get_text_messages(message: aiogram.types.Message) -> None:
    """ ОБРАБОТЧИК СООБЩЕНИЙ """

    if message.text.lower() == '/система':
        sysinfo = SysInfo()
        await message.answer(str(sysinfo))
    elif message.text.lower() == '/delete':
        await delete_chat_message(message)
    elif message.text.lower() == 'alert':
        await message.answer(await send_alert_message(message))
    elif message.text.lower() == '/__all_users':
        if ALLOWED_USERS:
            for user in ALLOWED_USERS:
                await message.reply(user)
        else:
            await message.answer("No registred users")
    elif message.text.lower() in ['weather moscow', 'weather kazan', 'weather paris', 'weather tokio']:
        await message.answer(str(get_weather(message)))
    else:
        await message.answer('Не понимаю, что это значит.')


def get_weather(where: aiogram.types.Message) -> str:
    """ Сообщает погоду обращаясь через API к OPENWEATHER"""

    open_weather_token = '934e44d95e12cbe09164de7bc73f02f6'
    fake_user = random.choice(UserAgents)
    proxy = random.choice(Proxies)
    where = where["text"][7:]
    try:
        r = requests.get(
            f"https://api.openweathermap.org/data/2.5/weather?q={where}&appid={open_weather_token}&units=metric",
            headers={'User-Agent': fake_user}, proxies={'Proxy': proxy})

        data = r.json()
        city = data["name"]
        cur_weather = data["main"]["temp"]
        humidity = data["main"]["humidity"]
        pressure = data["main"]["pressure"]
        return f"Город: {city} \n" \
               f"Температура: {cur_weather}\nВлажность: {humidity}\n Давление: {pressure}\n "
    except Exception as exc:
        return f"Exception {exc} occurred!\n STATUS: {r.status_code}\n REQUEST: {where}"


def get_primary_database_ip() -> str:
    """ Возвращает IP текущего боевого сервера БД """


def connect_postgres(ip: str):
    """ Коннект к БД, возвращает обьект connection """
    DBNAME = 'postgres'
    HOST = ip
    try:
        connection = psycopg2.connect(dbname=DBNAME,
                                user='postgres',
                                password='pg',
                                port='5432',
                                host=HOST)
        return connection
    except Exception as exception:
        print(f"Ошибка соединения: {exception} ")
    #finally:
    #    connection.close()


@DISPATCHER.message_handler(
    aiogram.dispatcher.filters.Command(['postgres'], ignore_case=True, ignore_mention=False, ignore_caption=True))
async def connect_postgresdb(message: aiogram.dispatcher.filters.Command) -> None:
    dbname = 'postgres'
    host = '192.168.56.113'
    try:
        conn = psycopg2.connect(dbname=dbname, user='postgres', password='pg', host=host)
        with conn.cursor() as cursor:
            cursor.execute('SELECT datname, datistemplate, datallowconn, datconnlimit FROM pg_database;')
            for row in cursor:
                await message.answer(row)
    except Exception as exception:
        print(f"Ошибка при выполнении запроса: {exception}")


async def delete_chat_message(message: aiogram.types.Message):
    await BOT.delete_message(message.chat.id, message.message_id)


if __name__ == '__main__':
    aiogram.executor.start_polling(DISPATCHER, skip_updates=True)
