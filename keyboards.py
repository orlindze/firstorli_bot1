# from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
# from database import get_all_fighters

# # ---------------- Главная клавиатура ----------------
# def main_keyboard_inline() -> InlineKeyboardMarkup:
#     """
#     Главная клавиатура бота.
#     Содержит кнопки: Добавить, Удалить, Список, Начать бой, Информация
#     """
#     return InlineKeyboardMarkup(inline_keyboard=[
#         [InlineKeyboardButton(text="Добавить бойца", callback_data="add_fighter")],
#         [InlineKeyboardButton(text="Удалить бойца", callback_data="delete_fighter")],
#         [InlineKeyboardButton(text="Список бойцов", callback_data="list_fighters")],
#         [InlineKeyboardButton(text="Начать бой", callback_data="start_fight")],
#         [InlineKeyboardButton(text="Информация", callback_data="info")]  # новая кнопка
#     ])

# # ---------------- Клавиатура Отмена ----------------
# def cancel_keyboard_inline() -> InlineKeyboardMarkup:
#     """
#     Клавиатура с одной кнопкой отмены.
#     """
#     return InlineKeyboardMarkup(inline_keyboard=[
#         [InlineKeyboardButton(text="Отмена", callback_data="cancel")]
#     ])

# # ---------------- Клавиатура списка бойцов ----------------
# def build_fighters_keyboard() -> InlineKeyboardMarkup:
#     """
#     Создает клавиатуру с бойцами из базы.
#     """
#     fighters = get_all_fighters()
#     buttons = []
#     for f in fighters:
#         name = f.get("name", str(f))
#         buttons.append([InlineKeyboardButton(text=name, callback_data=name)])
#     return InlineKeyboardMarkup(inline_keyboard=buttons)

# # ---------------- Клавиатура выбора стиля боя ----------------
# def styles_keyboard() -> InlineKeyboardMarkup:
#     """
#     Меню выбора стиля боя.
#     """
#     return InlineKeyboardMarkup(inline_keyboard=[
#         [InlineKeyboardButton(text="🥋 Карате", callback_data="karate")],
#         [InlineKeyboardButton(text="🥊 Бокс", callback_data="boxing")],
#         [InlineKeyboardButton(text="💥 MMA", callback_data="mma")],
#         [InlineKeyboardButton(text="🦵 Кикбоксинг", callback_data="kickboxing")],
#         [InlineKeyboardButton(text="⬅ Назад", callback_data="info")]  # возвращаемся в меню Информация
#     ])

# # ---------------- Клавиатуры бойцов для каждого стиля ----------------
# def karate_fighters_keyboard() -> InlineKeyboardMarkup:
#     return InlineKeyboardMarkup(inline_keyboard=[
#         [InlineKeyboardButton(text="Lyoto Machida", callback_data="machida")],
#         [InlineKeyboardButton(text="Stephen Thompson", callback_data="thompson")],
#         [InlineKeyboardButton(text="Georges St-Pierre", callback_data="gsp")],
#         [InlineKeyboardButton(text="⬅ Назад", callback_data="info")]
#     ])

# def boxing_fighters_keyboard() -> InlineKeyboardMarkup:
#     return InlineKeyboardMarkup(inline_keyboard=[
#         [InlineKeyboardButton(text="Mike Tyson", callback_data="tyson")],
#         [InlineKeyboardButton(text="Muhammad Ali", callback_data="ali")],
#         [InlineKeyboardButton(text="Floyd Mayweather", callback_data="mayweather")],
#         [InlineKeyboardButton(text="⬅ Назад", callback_data="info")]
#     ])

# def mma_fighters_keyboard() -> InlineKeyboardMarkup:
#     return InlineKeyboardMarkup(inline_keyboard=[
#         [InlineKeyboardButton(text="Conor McGregor", callback_data="mcgregor")],
#         [InlineKeyboardButton(text="Khabib Nurmagomedov", callback_data="khabib")],
#         [InlineKeyboardButton(text="Jon Jones", callback_data="jones")],
#         [InlineKeyboardButton(text="⬅ Назад", callback_data="info")]
#     ])

# def kickboxing_fighters_keyboard() -> InlineKeyboardMarkup:
#     return InlineKeyboardMarkup(inline_keyboard=[
#         [InlineKeyboardButton(text="Giorgio Petrosyan", callback_data="petrosyan")],
#         [InlineKeyboardButton(text="Rico Verhoeven", callback_data="verhoeven")],
#         [InlineKeyboardButton(text="Badr Hari", callback_data="hari")],
#         [InlineKeyboardButton(text="⬅ Назад", callback_data="info")]
#     ])
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from database import get_all_fighters

# ---------------- Головна клавіатура ----------------
def main_keyboard_inline() -> InlineKeyboardMarkup:
    """
    Головна клавіатура бота.
    Містить кнопки: Додати, Видалити, Список, Почати бій, Інформація
    """
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Додати бійця", callback_data="add_fighter")],
        [InlineKeyboardButton(text="Видалити бійця", callback_data="delete_fighter")],
        [InlineKeyboardButton(text="Список бійців", callback_data="list_fighters")],
        [InlineKeyboardButton(text="Почати бій", callback_data="start_fight")],
        [InlineKeyboardButton(text="Інформація", callback_data="info")]  
    ])

# ---------------- Клавіатура Скасування ----------------
def cancel_keyboard_inline() -> InlineKeyboardMarkup:
    """
    Клавіатура з однією кнопкою скасування.
    """
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Скасувати", callback_data="cancel")]
    ])

# ---------------- Клавіатура списку бійців ----------------
def build_fighters_keyboard() -> InlineKeyboardMarkup:
    """
    Створює клавіатуру з бійцями з бази.
    """
    fighters = get_all_fighters()
    buttons = []
    for f in fighters:
        name = f.get("name", str(f))
        buttons.append([InlineKeyboardButton(text=name, callback_data=name)])
    return InlineKeyboardMarkup(inline_keyboard=buttons)

# ---------------- Клавіатура вибору стилю бою ----------------
def styles_keyboard() -> InlineKeyboardMarkup:
    """
    Меню вибору стилю бою.
    """
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🥋 Карате", callback_data="karate")],
        [InlineKeyboardButton(text="🥊 Бокс", callback_data="boxing")],
        [InlineKeyboardButton(text="💥 MMA", callback_data="mma")],
        [InlineKeyboardButton(text="🦵 Кікбоксинг", callback_data="kickboxing")],
        [InlineKeyboardButton(text="⬅ Назад", callback_data="info")]  
    ])

# ---------------- Клавіатури бійців для кожного стилю ----------------
def karate_fighters_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Lyoto Machida", callback_data="machida")],
        [InlineKeyboardButton(text="Stephen Thompson", callback_data="thompson")],
        [InlineKeyboardButton(text="Georges St-Pierre", callback_data="gsp")],
        [InlineKeyboardButton(text="⬅ Назад", callback_data="info")]
    ])

def boxing_fighters_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Mike Tyson", callback_data="tyson")],
        [InlineKeyboardButton(text="Muhammad Ali", callback_data="ali")],
        [InlineKeyboardButton(text="Floyd Mayweather", callback_data="mayweather")],
        [InlineKeyboardButton(text="⬅ Назад", callback_data="info")]
    ])

def mma_fighters_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Conor McGregor", callback_data="mcgregor")],
        [InlineKeyboardButton(text="Khabib Nurmagomedov", callback_data="khabib")],
        [InlineKeyboardButton(text="Jon Jones", callback_data="jones")],
        [InlineKeyboardButton(text="⬅ Назад", callback_data="info")]
    ])

def kickboxing_fighters_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Giorgio Petrosyan", callback_data="petrosyan")],
        [InlineKeyboardButton(text="Rico Verhoeven", callback_data="verhoeven")],
        [InlineKeyboardButton(text="Badr Hari", callback_data="hari")],
        [InlineKeyboardButton(text="⬅ Назад", callback_data="info")]
    ])