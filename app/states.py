from aiogram.fsm.state import State, StatesGroup

class ModelGenerationState(StatesGroup):
    active = State()
    completed = State()
    error = State()
