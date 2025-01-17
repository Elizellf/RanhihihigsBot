from aiogram.types import CallbackQuery
from db import async_session, User
from sqlalchemy import select, insert
import logging
from .log import logger

from .replyes import *

async def callback_continue(callback: CallbackQuery):
    """Ответ на кнопку продолжить"""

    async with async_session() as session:
        # Что-то проиходит
        await session.commit()
    await callback.message.answer("Успешно!")



async def callback_reg_tutor(callback: CallbackQuery):
    async with async_session() as session:
        query = select(User).where(callback.from_user.id == User.user_id)
        user_exists = await session.execute(query)

        if user_exists.scalars().all():
            await message.answer(f"{registered_string} {message.from_user.username}")
        else:
            new_user = {
                'user_id': callback.from_user.id,
                'username': callback.from_user.username,
                'user_role': True,
            }
            insert_query = insert(User).values(**new_user)
            await session.execute(insert_query)
            await session.commit()
            logger.info(f"register new user {callback.from_user.id}")
            await callback.message.answer(f"{register_success_string} преподаватель")
        
        
async def callback_reg_student(callback: CallbackQuery):
    async with async_session() as session:
        query = select(User).where(callback.from_user.id == User.user_id)
        user_exists = await session.execute(query)

        if user_exists.scalars().all():
            await message.answer(f"{registered_string} {message.from_user.username}")
        else:
            new_user = {
                'user_id': callback.from_user.id,
                'username': callback.from_user.username,
                'user_role': False,
            }
            insert_query = insert(User).values(**new_user)
            await session.execute(insert_query)
            await session.commit()
            logger.info(f"register new user {callback.from_user.id}")
            await callback.message.answer(f"{register_success_string} студент")