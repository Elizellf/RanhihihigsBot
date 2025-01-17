## Этап 2. Переменные окружения, логирование и маршрутизация

# Дополнительный гайд по aiogram3 https://mastergroosha.github.io/aiogram-3-guide/
# Документация по aiogram3 https://docs.aiogram.dev/en/latest/
# Ссылка на форум aiogram в тг: https://t.me/aiogram

# 0. Установить зависимости
# pip install aiogram
# pip install python-dotenv

# 1. Импорт
import logging  # чтобы отследить состояние бота, используем логи
import asyncio  # асинхронный ввод-вывод
from aiogram import Bot, Dispatcher, types, filters  # класс бота и диспетчера
from config import TOKEN
from handlers import register_message_handler, commands_for_bot
from db import async_session, async_create_table, User, Dir
from threading import Thread
from sqlalchemy import select, insert, update, delete
import yadisk_async
from datetime import datetime, timezone

bot = Bot(TOKEN)
dp = Dispatcher()

def loop_in_thread(loop):
    print('loop')
    asyncio.set_event_loop(loop)
    asyncio.run(check_new_files())

async def on_startup(dp):
    print('init')
    loop = asyncio.get_event_loop()
    t = Thread(target=loop_in_thread, args=(loop,))
    t.start()


async def main() -> None:
    """polling-запуск проекта"""

    # Установить общий уровень логирования
    logging.basicConfig(level=logging.DEBUG)
    print ('TOKEN:', TOKEN)
    # Экзампляры бота и диспетчера
    
    
    

    # Функция для вызова обработчиков
    await register_message_handler(dp)

    # Загрузка команд
    await bot.set_my_commands(commands=commands_for_bot)
    await on_startup(dp)
    # polling-запуск
    await dp.start_polling(bot)#, on_startup=on_startup)

async def check_new_files() -> None: # проверка дисков на новые файлы
    bot = Bot(TOKEN)
    print('async')
    while True:
        await asyncio.sleep(90) # задержка
        async with async_session() as session:
            query = select(Dir).where(True)
            print('dir')
            Dir_exists = await session.execute(query)
            print('dir ok')
            for i in Dir_exists:
                #print ('thread', i)
                user_id = int(i[0].user_id) # получаем id владельца папки
                query = select(User).where(user_id == User.user_id)
                print('token')
                token = (await session.execute(query)).scalar()
                print('token ok')
                Disk = yadisk_async.YaDisk(token=token.user_token) # подключаемся к диску
                try:
                    folder_data = [i async for i in (await Disk.listdir(f"disk:{i[0].Dir_name}"))] # пытаемся достать информацию о файлах в папке
                except:
                    folder_data = None # если не получилось, ставим значение None
                #print(*folder_data)
                if folder_data is None: # если файлов нет, то пропускаем папку
                    pass
                else: # иначе начинаем проверку
                    for x in folder_data: # берём файлы последовательно
                        if x['file'] is None: # если это папка, то пропускаем
                            pass
                        else: # иначе начинаем проверку
                            #mod = x['modified'][0:x['modified'].find('+')]
                            print('file', x['name'])
                            print('time ', x['modified'], x['modified'].timestamp(), i[0].check_date, i[0].check_date.timestamp())
                            if x['modified'].timestamp() >= i[0].check_date.timestamp():
                                print ('modified')
                                #print ( f"Файл {x['name']} был обновлен {x['modified']}")
                                #print(x['name'], x['modified'], datetime.now(timezone.utc))
                                query = select(User).where(token.user_id == User.referer_id)
                                print('ref')
                                refs = (await session.execute(query))
                                print('ref ok')
                                for ref in refs:
                                    await bot.send_message(ref[0].user_id, text = f"Файл {x['name']} был обновлен {x['modified']}") # вызываем функцию для отправки сообщений
                print('update')
                query = update(Dir).where(int(i[0].Dir_id) == Dir.Dir_id).values(check_date=datetime.now())
                await session.execute(query)
                await session.commit()
                await asyncio.sleep(1)
                print('updated')    
                await Disk.close() # закрываем соединение с диском


# 5. Запуск
if __name__ == "__main__":
    try:
        asyncio.run(async_create_table())
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logging.info("GoodBye!")
