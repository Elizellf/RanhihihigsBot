from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

button_continue = InlineKeyboardButton(
    text="Далее",
    callback_data="continue_button_pressed"
)

keyboard_continue = InlineKeyboardMarkup(inline_keyboard=[[button_continue]])


kb_roles_list = [
    [InlineKeyboardButton(text="Преподаватель", callback_data='tutor'), InlineKeyboardButton(text="Студент",  callback_data='student')]
]
keyboard_roles = InlineKeyboardMarkup(
    inline_keyboard=kb_roles_list
)
