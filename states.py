import logging 

logger = logging.getLogger(__name__)


from aiogram.fsm.state import State, StatesGroup


class AddFighter(StatesGroup):
    name = State()
    style = State()
    age = State()