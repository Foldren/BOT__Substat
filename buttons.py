from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton


# Клавиатуры
keyboard_start_admin = [[KeyboardButton(text="Добавить/Изменить пользователя"),
                         KeyboardButton(text="Забрать доступ")
                         ]]

keyboard_start_analysts = [[KeyboardButton(text="Cтатистика за день"),
                            KeyboardButton(text="Cтатистика за неделю"),
                            KeyboardButton(text="Cтатистика за месяц")
                            ]]


# Конфигурации
keyboard_start_admin_configured = ReplyKeyboardMarkup(
    keyboard=keyboard_start_admin,
    resize_keyboard=True,  # меняем размер клавиатуры
)

keyboard_start_analysts_configured = ReplyKeyboardMarkup(
    keyboard=keyboard_start_analysts,
    resize_keyboard=True,
)


# Методы генерации клавиатур
def generate_cols_btns_keyboard(list_params, callback_str: str, number_cols: int):
    keyboard: list = [[]]

    number_str_keyboard = 0
    for i in range(0, len(list_params)):
        if i % number_cols == 0:
            number_str_keyboard += 1
            keyboard.append([])
        keyboard[number_str_keyboard].append(InlineKeyboardButton(
            text=list_params[i],
            callback_data=f"{callback_str}:{list_params[i]}"))

    return InlineKeyboardMarkup(inline_keyboard=keyboard)

