# import logging
# import asyncio
# import random

# from aiogram import Bot, Dispatcher, F
# from aiogram.types import Message, CallbackQuery
# from aiogram.filters import CommandStart
# from aiogram.fsm.context import FSMContext
# from aiogram.enums import ParseMode
# from aiogram.client.default import DefaultBotProperties

# from config import TOKEN
# from database import add_fighter, get_all_fighters, delete_fighter
# from keyboards import (
#     main_keyboard_inline,
#     cancel_keyboard_inline,
#     build_fighters_keyboard,
#     styles_keyboard,
#     karate_fighters_keyboard,
#     boxing_fighters_keyboard,
#     mma_fighters_keyboard,
#     kickboxing_fighters_keyboard
# )
# from states_machine import AddFighter, DeleteFighter, FightStates
# from commands import set_commands
# from aiogram.types import Message, CallbackQuery, URLInputFile

# # --------------------------------------------------
# # Logging configuration
# # --------------------------------------------------
# logging.basicConfig(
#     level=logging.INFO,
#     format="%(asctime)s - %(levelname)s - %(message)s",
#     handlers=[
#         logging.FileHandler("botlogger.log", encoding="utf-8"),
#         logging.StreamHandler()
#     ]
# )

# # --------------------------------------------------
# # Bot initialization
# # --------------------------------------------------
# bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
# dp = Dispatcher()

# # --------------------------------------------------
# # Helper functions
# # --------------------------------------------------
# def fighter_exists(name: str) -> bool:
#     """
#     Проверяет, существует ли боец с указанным именем.
#     """
#     fighters = get_all_fighters()
#     return any(name.lower() == f["name"].lower() for f in fighters)

# # --------------------------------------------------
# # Start command
# # --------------------------------------------------
# @dp.message(CommandStart())
# async def start_handler(message: Message):
#     """
#     Обрабатывает команду /start и показывает главное меню.
#     """
#     await message.answer(
#         "👋 Добро пожаловать!\nВыберите действие:",
#         reply_markup=main_keyboard_inline()
#     )


# # --------------------------------------------------
# # Cancel handler
# # --------------------------------------------------
# @dp.callback_query(F.data == "cancel")
# async def cancel_handler(query: CallbackQuery, state: FSMContext):
#     """
#     Отменяет текущее действие пользователя и сбрасывает состояние FSM.
#     """
#     await state.clear()
#     await query.message.answer(
#         "❌ Действие отменено.",
#         reply_markup=main_keyboard_inline()
#     )
#     await query.answer()

# # --------------------------------------------------
# # Add fighter
# # --------------------------------------------------
# @dp.callback_query(F.data == "add_fighter")
# async def add_fighter_start(query: CallbackQuery, state: FSMContext):
#     """
#     Начинает процесс добавления бойца.
#     """
#     await state.set_state(AddFighter.waiting_for_name)
#     await query.message.answer(
#         "Введите имя бойца:",
#         reply_markup=cancel_keyboard_inline()
#     )
#     await query.answer()

# @dp.message(AddFighter.waiting_for_name)
# async def process_name(message: Message, state: FSMContext):
#     """
#     Получает имя бойца и проверяет, не существует ли он уже.
#     """
#     name = message.text.strip()
#     if fighter_exists(name):
#         await message.answer("❌ Боец с таким именем уже существует.")
#         return
#     await state.update_data(name=name)
#     await message.answer("Введите стиль бойца:")
#     await state.set_state(AddFighter.waiting_for_style)

# @dp.message(AddFighter.waiting_for_style)
# async def process_style(message: Message, state: FSMContext):
#     """
#     Получает стиль бойца.
#     """
#     await state.update_data(style=message.text.strip())
#     await message.answer("Введите возраст бойца:")
#     await state.set_state(AddFighter.waiting_for_age)

# @dp.message(AddFighter.waiting_for_age)
# async def process_age(message: Message, state: FSMContext):
#     """
#     Получает возраст бойца и добавляет бойца в базу.
#     """
#     try:
#         age = int(message.text)
#     except ValueError:
#         await message.answer("Возраст должен быть числом.")
#         return
#     if age < 10 or age > 100:
#         await message.answer("Введите возраст от 10 до 100.")
#         return
#     data = await state.get_data()
#     fighter = {
#         "name": data["name"],
#         "style": data["style"],
#         "age": age
#     }
#     add_fighter(fighter)
#     logging.info(f"Fighter added: {fighter}")
#     await state.clear()
#     await message.answer(
#         "✅ Боец добавлен!",
#         reply_markup=main_keyboard_inline()
#     )

# # --------------------------------------------------
# # Delete fighter
# # --------------------------------------------------
# @dp.callback_query(F.data == "delete_fighter")
# async def delete_start(query: CallbackQuery, state: FSMContext):
#     """
#     Начинает процесс удаления бойца.
#     """
#     fighters = get_all_fighters()
#     if not fighters:
#         await query.message.answer("Список бойцов пуст.")
#         await query.answer()
#         return
#     await state.set_state(DeleteFighter.waiting_for_name)
#     await query.message.answer(
#         "Выберите бойца для удаления:",
#         reply_markup=build_fighters_keyboard()
#     )
#     await query.answer()

# @dp.callback_query(DeleteFighter.waiting_for_name)
# async def delete_by_name(query: CallbackQuery, state: FSMContext):
#     """
#     Удаляет выбранного бойца.
#     """
#     fighter_name = query.data
#     if fighter_exists(fighter_name):
#         delete_fighter(fighter_name)
#         logging.info(f"Deleted fighter: {fighter_name}")
#         await query.message.answer(
#             f"🗑 Боец {fighter_name} удалён.",
#             reply_markup=main_keyboard_inline()
#         )
#     else:
#         await query.message.answer(
#             "❌ Боец не найден.",
#             reply_markup=main_keyboard_inline()
#         )
#     await state.clear()
#     await query.answer()

# # --------------------------------------------------
# # List fighters
# # --------------------------------------------------
# @dp.callback_query(F.data == "list_fighters")
# async def list_fighters(query: CallbackQuery):
#     """
#     Показывает список всех бойцов.
#     """
#     fighters = get_all_fighters()
#     if not fighters:
#         await query.message.answer("Список бойцов пуст.")
#     else:
#         text = "🥊 <b>Список бойцов</b>\n\n"
#         for i, f in enumerate(fighters, start=1):
#             text += (
#                 f"{i}. <b>{f['name']}</b>\n"
#                 f"Стиль: {f['style']}\n"
#                 f"Возраст: {f['age']}\n\n"
#             )
#         await query.message.answer(text)
#     await query.answer()

# # --------------------------------------------------
# # Fight system
# # --------------------------------------------------
# @dp.callback_query(F.data == "start_fight")
# async def start_fight(query: CallbackQuery, state: FSMContext):
#     """
#     Начинает процесс выбора бойцов для боя.
#     """
#     fighters = get_all_fighters()
#     if len(fighters) < 2:
#         await query.message.answer("Недостаточно бойцов.")
#         await query.answer()
#         return
#     await state.set_state(FightStates.waiting_for_first)
#     await query.message.answer(
#         "Выберите первого бойца:",
#         reply_markup=build_fighters_keyboard()
#     )
#     await query.answer()

# @dp.callback_query(FightStates.waiting_for_first)
# async def get_first_fighter(query: CallbackQuery, state: FSMContext):
#     """
#     Сохраняет первого выбранного бойца.
#     """
#     await state.update_data(first=query.data)
#     await state.set_state(FightStates.waiting_for_second)
#     await query.message.answer(
#         "Выберите второго бойца:",
#         reply_markup=build_fighters_keyboard()
#     )
#     await query.answer()

# @dp.callback_query(FightStates.waiting_for_second)
# async def get_second_fighter(query: CallbackQuery, state: FSMContext):
#     """
#     Проводит бой между двумя бойцами с учётом возраста.
#     """
#     data = await state.get_data()
#     first_name = data.get("first")
#     second_name = query.data
#     if first_name == second_name:
#         await query.answer("Нельзя выбрать одного бойца!", show_alert=True)
#         return
#     fighters = get_all_fighters()
#     f1 = next((f for f in fighters if f["name"] == first_name), None)
#     f2 = next((f for f in fighters if f["name"] == second_name), None)
#     if not f1 or not f2:
#         await query.message.answer("Ошибка: боец не найден.")
#         await state.clear()
#         await query.answer()
#         return
#     age1 = int(f1.get("age", 20))
#     age2 = int(f2.get("age", 20))
#     score1 = random.randint(1, 10) + age1 // 10
#     score2 = random.randint(1, 10) + age2 // 10
#     winner = first_name if score1 > score2 else second_name if score2 > score1 else "🤝 Ничья"
#     logging.info(f"Fight: {first_name} vs {second_name} | Winner: {winner}")
#     await query.message.answer(
#         f"🥊 <b>Бой</b>\n\n"
#         f"{first_name} ⚔ {second_name}\n\n"
#         f"🏆 Результат: {winner}",
#         reply_markup=main_keyboard_inline()
#     )
#     await state.clear()
#     await query.answer()

# # ---------------- Fighters Info ----------------
# fighters_info = {
#     # ---------------- Karate ----------------
#     "machida": {
#         "photo": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSGK0qbpUD18PugJ7UQ09WsyNJPnZss3eXSppXLd2o8xTaHesbBeMsI295Mc0ZU9DWYNjpi7po52ajlh7ISj6PPU5DlVYvo_G5b-CIgtPWD&s=10",
#         "text": (
#             "🥋 <b>Lyoto Machida</b>\n"
#             "Стиль: Карате / MMA\n"
#             "Национальность: Бразилия\n"
#             "Дата рождения: 30.05.1978\n"
#             "Место рождения: Сантус, Бразилия\n"
#             "Достижения: Бывший чемпион UFC\n"
#             "Сильные стороны: Контроль дистанции, техника карате\n"
#             "Рекорд MMA: 26 побед, 8 поражений"
#         )
#     },
#     "thompson": {
#         "photo": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRXeEIDjurdQTxpO2_RlI7IsiqbwNdYX4MdRsnSqbnJtsL8rx6aIEFxL8EDcvLCkKrM130_vv46TKYkgxct-LJj6O1bTE2bpWm58-qfCdHk&s=10",
#         "text": (
#             "🥋 <b>Stephen Thompson</b>\n"
#             "Стиль: Карате / Кикбоксинг\n"
#             "Национальность: США\n"
#             "Дата рождения: 11.02.1983\n"
#             "Место рождения: Смиттаун, США\n"
#             "Достижения: Претендент на титул UFC\n"
#             "Сильные стороны: Высокая скорость, точность ударов ногами\n"
#             "Рекорд MMA: 16 побед, 6 поражений"
#         )
#     },
#     "gsp": {
#         "photo": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcR6tiZQqqKJ-z1ucIhIo-4mrkmQ8GSMRlRJYHYV1tgVw7IJnpGHXBVIQH091HRfyuleWmS_s7x-hkP3CdfCMEFDmwavwxeNSGnAqD9DlNBIOA&s=10",
#         "text": (
#             "🥋 <b>Georges St-Pierre</b>\n"
#             "Стиль: MMA / Карате\n"
#             "Национальность: Канада\n"
#             "Дата рождения: 19.05.1981\n"
#             "Место рождения: Монреаль, Канада\n"
#             "Достижения: Многократный чемпион UFC\n"
#             "Сильные стороны: Борьба, стратегия, техника ударов\n"
#             "Рекорд MMA: 26 побед, 2 поражения"
#         )
#     },

#     # ---------------- Boxing ----------------
#     "tyson": {
#         "photo": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRLPcJdNZ6B3kEg98pw6UfF4-_ye43yXQvDaqF2NlpJH9WZaGEPkMyVJ7kMWajRNP2Dn1-Vpb8uT7RIKDAYId1YOaFpza5PLWnSGanGxh29fA&s=10",
#         "text": (
#             "🥊 <b>Mike Tyson</b>\n"
#             "Стиль: Бокс\n"
#             "Национальность: США\n"
#             "Дата рождения: 30.06.1966\n"
#             "Место рождения: Бруклин, Нью-Йорк\n"
#             "Достижения: Абсолютный чемпион мира\n"
#             "Сильные стороны: Мощные нокауты, агрессия\n"
#             "Рекорд бокса: 50 побед, 6 поражений"
#         )
#     },
#     "ali": {
#         "photo": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQJY8WqsQ88KH9XDV8vmHFY8saYXvTjMse3mINcfguBfQVMzwkc-OePuyJVZVTNaxBfHKb_LTl2_W3dNLl8Scp6IGAyBAO5ccu8zGmZH02t&s=10",
#         "text": (
#             "🥊 <b>Muhammad Ali</b>\n"
#             "Стиль: Бокс\n"
#             "Национальность: США\n"
#             "Дата рождения: 17.01.1942\n"
#             "Место рождения: Луисвилл, Кентукки\n"
#             "Достижения: Трёхкратный чемпион мира\n"
#             "Сильные стороны: Подвижность, техника, харизма\n"
#             "Рекорд бокса: 56 побед, 5 поражений"
#         )
#     },
#     "mayweather": {
#         "photo": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSOXFbCP4jbCrZKsbES5gZp9tx_NpZ3nZXWGz2qYjF37rYtTs2sAWW05FBloRR5n05budr1zoFW53USvcS_yIhHi8OFQkOtEltZGyXxKZ3N&s=10",
#         "text": (
#             "🥊 <b>Floyd Mayweather</b>\n"
#             "Стиль: Бокс\n"
#             "Национальность: США\n"
#             "Дата рождения: 24.02.1977\n"
#             "Место рождения: Гранд-Рапидс, Мичиган\n"
#             "Достижения: Чемпион мира в 5 весовых категориях\n"
#             "Сильные стороны: Защита, тактика, скорость рук\n"
#             "Рекорд бокса: 50 побед, 0 поражений"
#         )
#     },

#     # ---------------- MMA ----------------
#     "mcgregor": {
#         "photo": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQJsnjJnOD0D8qq_ckBunmdTw3M4TORQsL-clvTjwGrUq2MHe2vRW97qYXk0h6pHdayTDwAWCmXb1T_PqqOQJK3N5baAECCCBLfADuhksMmYw&s=10",
#         "text": (
#             "💥 <b>Conor McGregor</b>\n"
#             "Стиль: MMA\n"
#             "Национальность: Ирландия\n"
#             "Дата рождения: 14.07.1988\n"
#             "Место рождения: Дублин, Ирландия\n"
#             "Достижения: Бывший чемпион UFC\n"
#             "Сильные стороны: Мощные удары руками, харизма\n"
#             "Рекорд MMA: 22 победы, 6 поражений"
#         )
#     },
#     "khabib": {
#         "photo": "https://encrypted-tbn0.gstatic.com/licensed-image?q=tbn:ANd9GcTwME5apG1TNmSh_i4ua-S5IAPoV0ubdbP89eWYLjEgBqNa7uq4ySIjkUFtRJbJ9FA3feGFicUfY8zpb5JQY1MUYvJ7fMUMPBYZohRhjavwaqywKxIoyg5aeW5L0kOuxE4Ms9NlJfLCUKPF&s=19",
#         "text": (
#             "💥 <b>Khabib Nurmagomedov</b>\n"
#             "Стиль: MMA / Самбо\n"
#             "Национальность: Россия\n"
#             "Дата рождения: 20.09.1988\n"
#             "Место рождения: Сильди, Дагестан\n"
#             "Достижения: Бывший чемпион UFC, непобеждённый\n"
#             "Сильные стороны: Борьба, контроль на земле\n"
#             "Рекорд MMA: 29 побед, 0 поражений"
#         )
#     },
#     "jones": {
#         "photo": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQoAhZfsg_rFHvFgZexaxQSdOZqgS_9JXAfz1joZKQOh2mcQ9kqrPh8bmiRif3YKXQz6SrF7zHV_Ed5G8v4HGSF5kf5NM5J-xNE8DDw2pF7Ow&s=10",
#         "text": (
#             "💥 <b>Jon Jones</b>\n"
#             "Стиль: MMA\n"
#             "Национальность: США\n"
#             "Дата рождения: 19.07.1987\n"
#             "Место рождения: Рочестер, Нью-Йорк\n"
#             "Достижения: Бывший чемпион UFC\n"
#             "Сильные стороны: Универсальная техника, длинные руки\n"
#             "Рекорд MMA: 27 побед, 1 поражение, 1 несостоявшийся бой"
#         )
#     },

#     # ---------------- Kickboxing ----------------
#     "petrosyan": {
#         "photo": "https://encrypted-tbn0.gstatic.com/licensed-image?q=tbn:ANd9GcTHVsNIKuFRKnA9J08oRBasfiyLiqP2hanonNCguvyL1Owr_sPwH0ERZNcyo9T6_aJkI0r_aHFa0vytns9Wd4EWx649m5V3dvSXFRQXpBp46nhsIOn6cMyTHPlB5ygOWtKSQFpcjvOcuHxx&s=19",
#         "text": (
#             "🦵 <b>Giorgio Petrosyan</b>\n"
#             "Стиль: Кикбоксинг\n"
#             "Национальность: Италия / Армения\n"
#             "Дата рождения: 10.12.1985\n"
#             "Место рождения: Ереван\n"
#             "Достижения: Многократный чемпион мира\n"
#             "Сильные стороны: Скорость, точность ударов ногами\n"
#             "Рекорд: 105 побед, 2 поражения"
#         )
#     },
#     "verhoeven": {
#         "photo": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQ-5bS8L4v6zoxOHUOVMwJzDWBjoEcfW0yoNDbFMRJEQPDpXErYv1zwUiNy8HPOjHFzX8ISGucynjI-InnQB-3XKbXwOlwNzJlkX2ohWYjmUg&s=10",
#         "text": (
#             "🦵 <b>Rico Verhoeven</b>\n"
#             "Стиль: Кикбоксинг\n"
#             "Национальность: Нидерланды\n"
#             "Дата рождения: 10.04.1989\n"
#             "Место рождения: Ден Бош, Нидерланды\n"
#             "Достижения: Чемпион Glory\n"
#             "Сильные стороны: Мощь, выносливость, стратегия\n"
#             "Рекорд: 61 победа, 11 поражений"
#         )
#     },
#     "hari": {
#         "photo": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcS2u2BS89YZ6OhAxFR0x28pb4q3sA-KwB58_ra4vTPfN03b72zydtPG8mxOYREqI5MQqQQvTrmNqdiuHqfHed9vK80yxfcFE6JNgOk_kmQ7&s=10",
#         "text": (
#             "🦵 <b>Badr Hari</b>\n"
#             "Стиль: Кикбоксинг\n"
#             "Национальность: Марокко\n"
#             "Дата рождения: 08.12.1984\n"
#             "Место рождения: Амстердам, Нидерланды\n"
#             "Достижения: Многократный чемпион мира\n"
#             "Сильные стороны: Агрессивный стиль, мощные удары\n"
#             "Рекорд: 106 побед, 22 поражения"
#         )
#     }
# }
# # Info menu handler
# @dp.callback_query(F.data == "info")
# async def info_menu(query: CallbackQuery):
#     """
#     Показывает меню выбора стиля боя.
#     """
#     await query.message.answer(
#         "Выберите стиль боя:",
#         reply_markup=styles_keyboard()
#     )
#     await query.answer()

# # Style selection handlers
# @dp.callback_query(F.data == "karate")
# async def karate_menu(query: CallbackQuery):
#     await query.message.answer(
#         "🥋 Популярные бойцы карате:",
#         reply_markup=karate_fighters_keyboard()
#     )
#     await query.answer()

# @dp.callback_query(F.data == "boxing")
# async def boxing_menu(query: CallbackQuery):
#     await query.message.answer(
#         "🥊 Популярные боксёры:",
#         reply_markup=boxing_fighters_keyboard()
#     )
#     await query.answer()

# @dp.callback_query(F.data == "mma")
# async def mma_menu(query: CallbackQuery):
#     await query.message.answer(
#         "💥 Популярные бойцы MMA:",
#         reply_markup=mma_fighters_keyboard()
#     )
#     await query.answer()

# @dp.callback_query(F.data == "kickboxing")
# async def kickboxing_menu(query: CallbackQuery):
#     await query.message.answer(
#         "🦵 Популярные бойцы кикбоксинга:",
#         reply_markup=kickboxing_fighters_keyboard()
#     )
#     await query.answer()

# # Fighter info handler
# @dp.callback_query(lambda c: c.data in fighters_info.keys())
# async def fighter_info(query: CallbackQuery):
#     """
#     Показывает фото и информацию о выбранном бойце.
#     """
#     fighter = fighters_info.get(query.data)
#     if not fighter:
#         await query.message.answer("Информация недоступна.")
#         await query.answer()
#         return
#     await query.message.answer_photo(
#         photo=URLInputFile(fighter["photo"]),
#         caption=fighter["text"],
#         parse_mode="HTML"
#     )
#     await query.answer()

# # --------------------------------------------------
# # Main
# # --------------------------------------------------
# async def main():
#     """
#     Запускает Telegram-бота.
#     """
#     await set_commands(bot)
#     logging.info("Bot started")
#     await dp.start_polling(bot)

# if __name__ == "__main__":
#     asyncio.run(main())

import logging
import asyncio
import random

from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties

from config import TOKEN
from database import add_fighter, get_all_fighters, delete_fighter
from keyboards import (
    main_keyboard_inline,
    cancel_keyboard_inline,
    build_fighters_keyboard,
    styles_keyboard,
    karate_fighters_keyboard,
    boxing_fighters_keyboard,
    mma_fighters_keyboard,
    kickboxing_fighters_keyboard
)
from states_machine import AddFighter, DeleteFighter, FightStates
from commands import set_commands
from aiogram.types import Message, CallbackQuery, URLInputFile

# --------------------------------------------------
# Налаштування логування
# --------------------------------------------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("botlogger.log", encoding="utf-8"),
        logging.StreamHandler()
    ]
)

# --------------------------------------------------
# Ініціалізація бота
# --------------------------------------------------
bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher()

# --------------------------------------------------
# Допоміжні функції
# --------------------------------------------------
def fighter_exists(name: str) -> bool:
    """
    Перевіряє, чи існує боєць із вказаним ім'ям.
    """
    fighters = get_all_fighters()
    return any(name.lower() == f["name"].lower() for f in fighters)

# --------------------------------------------------
# Команда Start
# --------------------------------------------------
@dp.message(CommandStart())
async def start_handler(message: Message):
    """
    Обробляє команду /start та показує головне меню.
    """
    await message.answer(
        "👋 Ласкаво просимо!\nОберіть дію:",
        reply_markup=main_keyboard_inline()
    )


# --------------------------------------------------
# Обробник скасування
# --------------------------------------------------
@dp.callback_query(F.data == "cancel")
async def cancel_handler(query: CallbackQuery, state: FSMContext):
    """
    Скасовує поточну дію користувача та скидає стан FSM.
    """
    await state.clear()
    await query.message.answer(
        "❌ Дію скасовано.",
        reply_markup=main_keyboard_inline()
    )
    await query.answer()

# --------------------------------------------------
# Додавання бійця
# --------------------------------------------------
@dp.callback_query(F.data == "add_fighter")
async def add_fighter_start(query: CallbackQuery, state: FSMContext):
    """
    Починає процес додавання бійця.
    """
    await state.set_state(AddFighter.waiting_for_name)
    await query.message.answer(
        "Введіть ім'я бійця:",
        reply_markup=cancel_keyboard_inline()
    )
    await query.answer()

@dp.message(AddFighter.waiting_for_name)
async def process_name(message: Message, state: FSMContext):
    """
    Отримує ім'я бійця та перевіряє, чи не існує він уже.
    """
    name = message.text.strip()
    if fighter_exists(name):
        await message.answer("❌ Боєць із таким ім'ям уже існує.")
        return
    await state.update_data(name=name)
    await message.answer("Введіть стиль бійця:")
    await state.set_state(AddFighter.waiting_for_style)

@dp.message(AddFighter.waiting_for_style)
async def process_style(message: Message, state: FSMContext):
    """
    Отримує стиль бійця.
    """
    await state.update_data(style=message.text.strip())
    await message.answer("Введіть вік бійця:")
    await state.set_state(AddFighter.waiting_for_age)

@dp.message(AddFighter.waiting_for_age)
async def process_age(message: Message, state: FSMContext):
    """
    Отримує вік бійця та додає бійця до бази.
    """
    try:
        age = int(message.text)
    except ValueError:
        await message.answer("Вік має бути числом.")
        return
    if age < 10 or age > 100:
        await message.answer("Введіть вік від 10 до 100.")
        return
    data = await state.get_data()
    fighter = {
        "name": data["name"],
        "style": data["style"],
        "age": age
    }
    add_fighter(fighter)
    logging.info(f"Fighter added: {fighter}")
    await state.clear()
    await message.answer(
        "✅ Бійця додано!",
        reply_markup=main_keyboard_inline()
    )

# --------------------------------------------------
# Видалення бійця
# --------------------------------------------------
@dp.callback_query(F.data == "delete_fighter")
async def delete_start(query: CallbackQuery, state: FSMContext):
    """
    Починає процес видалення бійця.
    """
    fighters = get_all_fighters()
    if not fighters:
        await query.message.answer("Список бійців порожній.")
        await query.answer()
        return
    await state.set_state(DeleteFighter.waiting_for_name)
    await query.message.answer(
        "Оберіть бійця для видалення:",
        reply_markup=build_fighters_keyboard()
    )
    await query.answer()

@dp.callback_query(DeleteFighter.waiting_for_name)
async def delete_by_name(query: CallbackQuery, state: FSMContext):
    """
    Видаляє обраного бійця.
    """
    fighter_name = query.data
    if fighter_exists(fighter_name):
        delete_fighter(fighter_name)
        logging.info(f"Deleted fighter: {fighter_name}")
        await query.message.answer(
            f"🗑 Бійця {fighter_name} видалено.",
            reply_markup=main_keyboard_inline()
        )
    else:
        await query.message.answer(
            "❌ Бійця не знайдено.",
            reply_markup=main_keyboard_inline()
        )
    await state.clear()
    await query.answer()

# --------------------------------------------------
# Список бійців
# --------------------------------------------------
@dp.callback_query(F.data == "list_fighters")
async def list_fighters(query: CallbackQuery):
    """
    Показує список усіх бійців.
    """
    fighters = get_all_fighters()
    if not fighters:
        await query.message.answer("Список бійців порожній.")
    else:
        text = "🥊 <b>Список бійців</b>\n\n"
        for i, f in enumerate(fighters, start=1):
            text += (
                f"{i}. <b>{f['name']}</b>\n"
                f"Стиль: {f['style']}\n"
                f"Вік: {f['age']}\n\n"
            )
        await query.message.answer(text)
    await query.answer()

# --------------------------------------------------
# Система боїв
# --------------------------------------------------
@dp.callback_query(F.data == "start_fight")
async def start_fight(query: CallbackQuery, state: FSMContext):
    """
    Починає процес вибору бійців для бою.
    """
    fighters = get_all_fighters()
    if len(fighters) < 2:
        await query.message.answer("Недостатньо бійців.")
        await query.answer()
        return
    await state.set_state(FightStates.waiting_for_first)
    await query.message.answer(
        "Оберіть першого бійця:",
        reply_markup=build_fighters_keyboard()
    )
    await query.answer()

@dp.callback_query(FightStates.waiting_for_first)
async def get_first_fighter(query: CallbackQuery, state: FSMContext):
    """
    Зберігає першого обраного бійця.
    """
    await state.update_data(first=query.data)
    await state.set_state(FightStates.waiting_for_second)
    await query.message.answer(
        "Оберіть другого бійця:",
        reply_markup=build_fighters_keyboard()
    )
    await query.answer()

@dp.callback_query(FightStates.waiting_for_second)
async def get_second_fighter(query: CallbackQuery, state: FSMContext):
    """
    Проводить бій між двома бійцями з урахуванням віку.
    """
    data = await state.get_data()
    first_name = data.get("first")
    second_name = query.data
    if first_name == second_name:
        await query.answer("Не можна обрати одного бійця!", show_alert=True)
        return
    fighters = get_all_fighters()
    f1 = next((f for f in fighters if f["name"] == first_name), None)
    f2 = next((f for f in fighters if f["name"] == second_name), None)
    if not f1 or not f2:
        await query.message.answer("Помилка: бійця не знайдено.")
        await state.clear()
        await query.answer()
        return
    age1 = int(f1.get("age", 20))
    age2 = int(f2.get("age", 20))
    score1 = random.randint(1, 10) + age1 // 10
    score2 = random.randint(1, 10) + age2 // 10
    winner = first_name if score1 > score2 else second_name if score2 > score1 else "🤝 Нічия"
    logging.info(f"Fight: {first_name} vs {second_name} | Winner: {winner}")
    await query.message.answer(
        f"🥊 <b>Бій</b>\n\n"
        f"{first_name} ⚔ {second_name}\n\n"
        f"🏆 Результат: {winner}",
        reply_markup=main_keyboard_inline()
    )
    await state.clear()
    await query.answer()

# ---------------- Інформація про бійців ----------------
fighters_info = {
    # ---------------- Карате ----------------
    "machida": {
        "photo": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSGK0qbpUD18PugJ7UQ09WsyNJPnZss3eXSppXLd2o8xTaHesbBeMsI295Mc0ZU9DWYNjpi7po52ajlh7ISj6PPU5DlVYvo_G5b-CIgtPWD&s=10",
        "text": (
            "🥋 <b>Lyoto Machida</b>\n"
            "Стиль: Карате / MMA\n"
            "Національність: Бразилія\n"
            "Дата народження: 30.05.1978\n"
            "Місце народження: Сантус, Бразилія\n"
            "Досягнення: Колишній чемпіон UFC\n"
            "Сильні сторони: Контроль дистанції, техніка карате\n"
            "Рекорд MMA: 26 перемог, 8 поразок"
        )
    },
    "thompson": {
        "photo": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRXeEIDjurdQTxpO2_RlI7IsiqbwNdYX4MdRsnSqbnJtsL8rx6aIEFxL8EDcvLCkKrM130_vv46TKYkgxct-LJj6O1bTE2bpWm58-qfCdHk&s=10",
        "text": (
            "🥋 <b>Stephen Thompson</b>\n"
            "Стиль: Карате / Кікбоксинг\n"
            "Національність: США\n"
            "Дата народження: 11.02.1983\n"
            "Місце народження: Сміттаун, США\n"
            "Досягнення: Претендент на титул UFC\n"
            "Сильні сторони: Висока швидкість, точність ударів ногами\n"
            "Рекорд MMA: 16 перемог, 6 поразок"
        )
    },
    "gsp": {
        "photo": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcR6tiZQqqKJ-z1ucIhIo-4mrkmQ8GSMRlRJYHYV1tgVw7IJnpGHXBVIQH091HRfyuleWmS_s7x-hkP3CdfCMEFDmwavwxeNSGnAqD9DlNBIOA&s=10",
        "text": (
            "🥋 <b>Georges St-Pierre</b>\n"
            "Стиль: MMA / Карате\n"
            "Національність: Канада\n"
            "Дата народження: 19.05.1981\n"
            "Місце народження: Монреаль, Канада\n"
            "Досягнення: Багаторазовий чемпіон UFC\n"
            "Сильні сторони: Боротьба, стратегія, техніка ударів\n"
            "Рекорд MMA: 26 перемог, 2 поразки"
        )
    },

    # ---------------- Бокс ----------------
    "tyson": {
        "photo": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRLPcJdNZ6B3kEg98pw6UfF4-_ye43yXQvDaqF2NlpJH9WZaGEPkMyVJ7kMWajRNP2Dn1-Vpb8uT7RIKDAYId1YOaFpza5PLWnSGanGxh29fA&s=10",
        "text": (
            "🥊 <b>Mike Tyson</b>\n"
            "Стиль: Бокс\n"
            "Національність: США\n"
            "Дата народження: 30.06.1966\n"
            "Місце народження: Бруклін, Нью-Йорк\n"
            "Досягнення: Абсолютний чемпіон світу\n"
            "Сильні сторони: Потужні нокаути, агресія\n"
            "Рекорд боксу: 50 перемог, 6 поразок"
        )
    },
    "ali": {
        "photo": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQJY8WqsQ88KH9XDV8vmHFY8saYXvTjMse3mINcfguBfQVMzwkc-OePuyJVZVTNaxBfHKb_LTl2_W3dNLl8Scp6IGAyBAO5ccu8zGmZH02t&s=10",
        "text": (
            "🥊 <b>Muhammad Ali</b>\n"
            "Стиль: Бокс\n"
            "Національність: США\n"
            "Дата народження: 17.01.1942\n"
            "Місце народження: Луїсвілл, Кентуккі\n"
            "Досягнення: Триразовий чемпіон світу\n"
            "Сильні сторони: Рухливість, техніка, харизма\n"
            "Рекорд боксу: 56 перемог, 5 поразок"
        )
    },
    "mayweather": {
        "photo": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSOXFbCP4jbCrZKsbES5gZp9tx_NpZ3nZXWGz2qYjF37rYtTs2sAWW05FBloRR5n05budr1zoFW53USvcS_yIhHi8OFQkOtEltZGyXxKZ3N&s=10",
        "text": (
            "🥊 <b>Floyd Mayweather</b>\n"
            "Стиль: Бокс\n"
            "Національність: США\n"
            "Дата народження: 24.02.1977\n"
            "Місце народження: Гранд-Рапідс, Мічиган\n"
            "Досягнення: Чемпіон світу в 5 вагових категоріях\n"
            "Сильні сторони: Захист, тактика, швидкість рук\n"
            "Рекорд боксу: 50 перемог, 0 поразок"
        )
    },

    # ---------------- MMA ----------------
    "mcgregor": {
        "photo": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQJsnjJnOD0D8qq_ckBunmdTw3M4TORQsL-clvTjwGrUq2MHe2vRW97qYXk0h6pHdayTDwAWCmXb1T_PqqOQJK3N5baAECCCBLfADuhksMmYw&s=10",
        "text": (
            "💥 <b>Conor McGregor</b>\n"
            "Стиль: MMA\n"
            "Національність: Ірландія\n"
            "Дата народження: 14.07.1988\n"
            "Місце народження: Дублін, Ірландія\n"
            "Досягнення: Колишній чемпіон UFC\n"
            "Сильні сторони: Потужні удари руками, харизма\n"
            "Рекорд MMA: 22 перемоги, 6 поразок"
        )
    },
    "khabib": {
        "photo": "https://encrypted-tbn0.gstatic.com/licensed-image?q=tbn:ANd9GcTwME5apG1TNmSh_i4ua-S5IAPoV0ubdbP89eWYLjEgBqNa7uq4ySIjkUFtRJbJ9FA3feGFicUfY8zpb5JQY1MUYvJ7fMUMPBYZohRhjavwaqywKxIoyg5aeW5L0kOuxE4Ms9NlJfLCUKPF&s=19",
        "text": (
            "💥 <b>Хабіб Нурмагомедов</b>\n"
            "Стиль: MMA / Самбо\n"
            "Національність: Росія\n"
            "Дата народження: 20.09.1988\n"
            "Місце народження: Сільді, Дагестан\n"
            "Досягнення: Колишній чемпіон UFC, непереможний\n"
            "Сильні сторони: Боротьба, контроль на землі\n"
            "Рекорд MMA: 29 перемог, 0 поразок"
        )
    },
    "jones": {
        "photo": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQoAhZfsg_rFHvFgZexaxQSdOZqgS_9JXAfz1joZKQOh2mcQ9kqrPh8bmiRif3YKXQz6SrF7zHV_Ed5G8v4HGSF5kf5NM5J-xNE8DDw2pF7Ow&s=10",
        "text": (
            "💥 <b>Jon Jones</b>\n"
            "Стиль: MMA\n"
            "Національність: США\n"
            "Дата народження: 19.07.1987\n"
            "Місце народження: Рочестер, Нью-Йорк\n"
            "Досягнення: Колишній чемпіон UFC\n"
            "Сильні сторони: Універсальна техніка, довгі руки\n"
            "Рекорд MMA: 27 перемог, 1 поразка, 1 бій, що не відбувся"
        )
    },

    # ---------------- Кікбоксинг ----------------
    "petrosyan": {
        "photo": "https://encrypted-tbn0.gstatic.com/licensed-image?q=tbn:ANd9GcTHVsNIKuFRKnA9J08oRBasfiyLiqP2hanonNCguvyL1Owr_sPwH0ERZNcyo9T6_aJkI0r_aHFa0vytns9Wd4EWx649m5V3dvSXFRQXpBp46nhsIOn6cMyTHPlB5ygOWtKSQFpcjvOcuHxx&s=19",
        "text": (
            "🦵 <b>Giorgio Petrosyan</b>\n"
            "Стиль: Кікбоксинг\n"
            "Національність: Італія / Вірменія\n"
            "Дата народження: 10.12.1985\n"
            "Місце народження: Єреван\n"
            "Досягнення: Багаторазовий чемпіон світу\n"
            "Сильні сторони: Швидкість, точність ударів ногами\n"
            "Рекорд: 105 перемог, 2 поразки"
        )
    },
    "verhoeven": {
        "photo": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQ-5bS8L4v6zoxOHUOVMwJzDWBjoEcfW0yoNDbFMRJEQPDpXErYv1zwUiNy8HPOjHFzX8ISGucynjI-InnQB-3XKbXwOlwNzJlkX2ohWYjmUg&s=10",
        "text": (
            "🦵 <b>Rico Verhoeven</b>\n"
            "Стиль: Кікбоксинг\n"
            "Національність: Нідерланди\n"
            "Дата народження: 10.04.1989\n"
            "Місце народження: Ден Бош, Нідерланди\n"
            "Досягнення: Чемпіон Glory\n"
            "Сильні сторони: Потужність, витривалість, стратегія\n"
            "Рекорд: 61 перемога, 11 поразок"
        )
    },
    "hari": {
        "photo": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcS2u2BS89YZ6OhAxFR0x28pb4q3sA-KwB58_ra4vTPfN03b72zydtPG8mxOYREqI5MQqQQvTrmNqdiuHqfHed9vK80yxfcFE6JNgOk_kmQ7&s=10",
        "text": (
            "🦵 <b>Badr Hari</b>\n"
            "Стиль: Кікбоксинг\n"
            "Національність: Марокко\n"
            "Дата народження: 08.12.1984\n"
            "Місце народження: Амстердам, Нідерланди\n"
            "Досягнення: Багаторазовий чемпіон світу\n"
            "Сильні сторони: Агресивний стиль, потужні удари\n"
            "Рекорд: 106 перемог, 22 поразки"
        )
    }
}
# Обробник меню інформації
@dp.callback_query(F.data == "info")
async def info_menu(query: CallbackQuery):
    """
    Показує меню вибору стилю бою.
    """
    await query.message.answer(
        "Оберіть стиль бою:",
        reply_markup=styles_keyboard()
    )
    await query.answer()

# Обробники вибору стилю
@dp.callback_query(F.data == "karate")
async def karate_menu(query: CallbackQuery):
    await query.message.answer(
        "🥋 Популярні бійці карате:",
        reply_markup=karate_fighters_keyboard()
    )
    await query.answer()

@dp.callback_query(F.data == "boxing")
async def boxing_menu(query: CallbackQuery):
    await query.message.answer(
        "🥊 Популярні боксери:",
        reply_markup=boxing_fighters_keyboard()
    )
    await query.answer()

@dp.callback_query(F.data == "mma")
async def mma_menu(query: CallbackQuery):
    await query.message.answer(
        "💥 Популярні бійці MMA:",
        reply_markup=mma_fighters_keyboard()
    )
    await query.answer()

@dp.callback_query(F.data == "kickboxing")
async def kickboxing_menu(query: CallbackQuery):
    await query.message.answer(
        "🦵 Популярні бійці кікбоксингу:",
        reply_markup=kickboxing_fighters_keyboard()
    )
    await query.answer()

# Обробник інформації про бійця
@dp.callback_query(lambda c: c.data in fighters_info.keys())
async def fighter_info(query: CallbackQuery):
    """
    Показує фото та інформацію про обраного бійця.
    """
    fighter = fighters_info.get(query.data)
    if not fighter:
        await query.message.answer("Інформація недоступна.")
        await query.answer()
        return
    await query.message.answer_photo(
        photo=URLInputFile(fighter["photo"]),
        caption=fighter["text"],
        parse_mode="HTML"
    )
    await query.answer()

# --------------------------------------------------
# Головна функція
# --------------------------------------------------
async def main():
    """
    Запускає Telegram-бота.
    """
    await set_commands(bot)
    logging.info("Bot started")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())