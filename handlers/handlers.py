# -- Обработчики (handlers) --
# Все обработчики должны быть подключены к маршрутизатору (или диспетчеру)
# Обработчики (handlers) — обработчик сообщений, который будет возвращать другое сообщение, указанное в функции

__all__ = [
    "register_message_handler"
]

# Установить общий уровень логирования и создали экземпляр лога
import logging
from aiogram import Router, types, filters, F
from db import async_session, User, Dir
from sqlalchemy import select, insert, update, delete
from .keyboards import *
from .callbacks import *
from .log import logger
from .replyes import *
import yadisk_async
from datetime import datetime, timezone




async def command_help_handler(message: types.Message) -> None:
    """Команда справки /help"""
    async with async_session() as session:
        await message.answer(help_string)

async def command_start_handler(message: types.Message) -> None:
    """Команда регистрации /start"""

    async with async_session() as session:
        query = select(User).where(message.from_user.id == User.user_id)
        user_exists = await session.execute(query)

        if user_exists.scalars().all():
            await message.answer(f"{registered_string} {message.from_user.username}")
        else:
            #print(message.text)
            await message.answer(register_string, reply_markup=keyboard_roles)
            """
            if 'tutor' in message.text and 'student' in message.text:
                await message.answer(err_role_string)
                await message.answer(register_string) #, reply_markup=main_kb(message.from_user.id))
            elif 'tutor' in message.text:
                new_user = {
                    'user_id': message.from_user.id,
                    'username': message.from_user.username,
                    'user_role': True,
                }
                insert_query = insert(User).values(**new_user)
                await session.execute(insert_query)
                await session.commit()
                logger.info(f"register new user {message.from_user.id}")
                #await message.answer('Вы зарегистрированы как преподаватель')
                await message.answer(f"{register_success_string} Преподаватель")
            elif 'student' in message.text:
                new_user = {
                    'user_id': message.from_user.id,
                    'username': message.from_user.username,
                    'user_role': False,
                }
                insert_query = insert(User).values(**new_user)
                await session.execute(insert_query)
                await session.commit()
                logger.info(f"register new user {message.from_user.id}")
                #await message.answer('Вы зарегистрированы как студент')
                await message.answer(f"{register_success_string} Студент")
            else:
                await message.answer(err_role_string)
                await message.answer(register_string)
            """

async def command_status_handler(message: types.Message) -> None:
    """Команда информации о пользователе /status"""

    async with async_session() as session:
        query = select(User).where(message.from_user.id == User.user_id)
        user_exists = await session.execute(query)
        print ('exist')
        if user_exists.scalars().all():
            print ('exists')
            query = select(User).where(message.from_user.id == User.user_id)
            result = await session.execute(query)
            user = result.scalar()
            info = (f"<b>UserId</b>: <i>{user.user_id}</i>\n"
                    f"<b>UserName</b>: <i>{user.username}</i>\n"
                    f"<b>UserRole</b>: <i>{'tutor' if user.user_role else 'student'}</i>\n"
                    f"<b>Registration Date</b>: <i>{user.reg_date}</i>")
            await message.answer(info, parse_mode="HTML")
            logger.info(f"user {message.from_user.id} asks for status!")
        else:
            print ('existnot')
            #print(message.text)
            await message.answer(NOTaUser_string)

    #await message.reply("Хотите продолжить?", reply_markup=keyboard_continue)

async def command_register_handler(message: types.Message) -> None:
    async with async_session() as session:
        query = select(User).where(message.from_user.id == User.user_id)
        user_exists = await session.execute(query)
        if user_exists.scalars().all():
            query = select(User).where(message.from_user.id == User.user_id)
            user_exists = await session.execute(query)
            if user_exists.scalar().user_role:
                data = message.text.split()
                if len(data) == 1:
                    await message.answer(instruction_string)
                    await message.answer(step1_string)
                    await message.answer(step2_string)
                    await message.answer(step3_string)
                    await message.answer(step4_string)
                elif len(data) == 2:
                    await message.answer(f"{clientID_string}{data[1].strip()}")
                else:
                    await message.answer(unknownErr_string)
            else:
                data = message.text.split()
                if len(data) == 1:
                    await message.answer(instruction_string_student)
                else:
                    await message.answer(unknownErr_string)
        else:
            #print(message.text)
            await message.answer(NOTaUser_string)

async def command_token_handler(message: types.Message) -> None:
    async with async_session() as session:
        query = select(User).where(message.from_user.id == User.user_id)
        user_exists = await session.execute(query)
        #print ('exist', *user_exists)    

        if user_exists.scalars().all():
            query = select(User).where(message.from_user.id == User.user_id)
            user_exists = await session.execute(query)
            if user_exists.scalar().user_role:
                data = message.text.split()
                if len(data) == 1:
                    await message.answer(enterToken_string)
                elif len(data) == 2:
                    print ('inserting token')
                    Disk = yadisk_async.YaDisk(token=data[1].strip())
                    answer=False
                    print('Disk')
                    try:
                        answer = await Disk.check_token()
                        
                        await Disk.close()
                    except:
                        await Disk.close()
                        answer=False
                    print(answer)
                    if answer:
                        query = update(User).where(message.from_user.id == User.user_id).values(user_token=data[1].strip())
                        await session.execute(query)
                        await session.commit()
                        await message.answer(successToken_string)
                    else:
                        await message.answer(incorrectToken_string)
                else:
                    await message.answer(unknownErr_string)
            else:
                data = message.text.split()
                if len(data) == 1:
                    await message.answer(enterToken_string_student)
                elif len(data) == 2:
                    print ('inserting token')
                    query = select(User).where(data[1].strip() == User.user_id).where(True==User.user_role)
                    user_exists = await session.execute(query)

                    if user_exists.scalars().all():
                        query = update(User).where(message.from_user.id == User.user_id).values(referer_id = data[1].strip())
                        await session.execute(query)
                        await session.commit()
                        await message.answer(successToken_string_student)
                    else:
                        await message.answer(incorrectToken_string_student)
                else:
                    await message.answer(unknownErr_string)
        else:
            await message.answer(NOTaUser_string)

async def command_add_handler(message: types.Message) -> None:
    async with async_session() as session:
        query = select(User).where(message.from_user.id == User.user_id)
        user_exists = await session.execute(query)

        if user_exists.scalars().all():
            query = select(User).where(message.from_user.id == User.user_id)
            user_exists = await session.execute(query)
            if user_exists.scalar().user_role:
                query = select(User).where(message.from_user.id == User.user_id)
                print('execute')
                token = (await session.execute(query)).scalar()
                print('executed')
                print(token.user_token)
                Disk = yadisk_async.YaDisk(token=token.user_token)
                answer=False
                try:
                    answer = await Disk.check_token()
                except:
                    await Disk.close()
                    answer=False
                if answer:
                    data = message.text
                    print(len(data))
                    if len(data.strip()) < 5:
                        await message.answer(enterPath_string)
                    else:
                        result = False
                        path = data[5:] if data[-1] == '/' else data[5:] + '/'
                        print('path', path)
                        try:
                            if [i async for i in await Disk.listdir(f"disk:{path}")]:
                                result =  True
                        except:
                            await Disk.close()
                            result =  False
                        if result:
                            new_dir = {
                                'user_id': message.from_user.id,
                                'Dir_name': path,
                            }
                            try:
                                print ('new')
                                print(*new_dir)
                                insert_query = insert(Dir).values(**new_dir)
                                print('execute')
                                await session.execute(insert_query)
                                print('executed')
                                await session.commit()
                                print('commited')
                                await message.answer(successPath_string)
                            except:
                                await message.answer(unknownErr_string)
                        else:
                            await message.answer(incorrectPath_string)
                else:
                    await message.answer(incorrectToken_string)
            else:
                await message.answer(no_rights_string)
        else:
            await message.answer(NOTaUser_string)

async def command_delete_handler(message: types.Message) -> None:
    async with async_session() as session:
        query = select(User).where(message.from_user.id == User.user_id)
        user_exists = await session.execute(query)

        if user_exists.scalars().all():
            query = select(User).where(message.from_user.id == User.user_id)
            user_exists = await session.execute(query)
            if user_exists.scalar().user_role:
                data = message.text
                if len(data.strip()) < 8:
                    await message.answer(enterPath_string)
                else:
                    result = False
                    path = data[8:] if data[-1] == '/' else data[8:] + '/'
                    query = select(Dir).where(message.from_user.id == Dir.user_id).where(path == Dir.Dir_name)
                    print ('query', query)
                    Dir_exists = await session.execute(query)
                    if Dir_exists.scalars().all():
                        query = select(Dir).where(message.from_user.id == Dir.user_id).where(path == Dir.Dir_name)
                        Dir_exists = await session.execute(query)
                        for i in Dir_exists:
                            print('Dir to delete: ', i[0].Dir_name)
                        try:
                            print('delete')
                            delete_query = delete(Dir).where(message.from_user.id == Dir.user_id).where(path == Dir.Dir_name)
                            print('execute')
                            await session.execute(delete_query)
                            print('executed')
                            await session.commit()
                            print('commited')
                            await message.answer(successDelete_string)
                        except:
                            await message.answer(unknownErr_string)
                    else:
                        await message.answer(incorrectPath_string)
            else:
                await message.answer(no_rights_string)
        else:
            await message.answer(NOTaUser_string)



async def process_unknown_command(message: types.Message) -> None:
    """эхо-ответ"""
    await message.reply(text="Неподдерживаемая команда. Введите /help для справки.")
    logger.info(f"user {message.from_user.id} send unknown message or command!")


async def register_message_handler(router: Router):
    """Маршрутизация"""
    router.message.register(command_help_handler, filters.Command(commands=["help"]))
    router.message.register(command_start_handler, filters.Command(commands=["start"]))
    router.message.register(command_status_handler, filters.Command(commands=["status"]))
    router.message.register(command_register_handler, filters.Command(commands=["register"]))
    router.message.register(command_token_handler, filters.Command(commands=["token"]))
    router.message.register(command_add_handler, filters.Command(commands=["add"]))
    router.message.register(command_delete_handler, filters.Command(commands=["delete"]))
    router.callback_query.register(callback_continue, F.data.startswith("continue_"))
    router.callback_query.register(callback_reg_tutor, F.data.startswith("tutor"))
    router.callback_query.register(callback_reg_student, F.data.startswith("student"))
    router.message.register(process_unknown_command)