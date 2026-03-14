import logging

logger = logging.getLogger(__name__)

from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram.fsm.state import State, StatesGroup



class AddFighter(StatesGroup):
    waiting_for_name = State()
    waiting_for_style = State()
    waiting_for_age = State()

class DeleteFighter(StatesGroup):
    waiting_for_name = State()

class FightStates(StatesGroup):
    waiting_for_first = State()
    waiting_for_second = State()
    