from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.enums import ChatAction
from app.generators import MistralAI
from app.states import ModelGenerationState
from app.msg_constants import MessageConstants

import app.flat_db as db
from aiogram.types import WebAppInfo
from aiogram import types
from dotenv import load_dotenv
import re
import os

load_dotenv()
AI_MODEL = MistralAI(os.getenv('MISTRAL_API_KEY'))
user = Router()


def escape_markdown_v2(text: str) -> str:
    special_characters = r'_*[]()~>#+-=|{}.!'
    return re.sub(f"([{re.escape(special_characters)}])", r"\\\1", text)

    

@user.message(Command('start'))
async def cmd_start(message: Message):
    await message.answer(escape_markdown_v2(MessageConstants.STARTING_MESSAGE))



@user.message(ModelGenerationState.active)
async def active_generation_handler(message: Message):
    await message.answer(escape_markdown_v2(MessageConstants.DO_NOT_INTERRUPT))
    await message.bot.send_chat_action(
        chat_id=message.from_user.id, action=ChatAction.TYPING
    )


@user.message()
async def any_msg(message: Message, state: FSMContext):
    await state.set_state(ModelGenerationState.active)
    db.update_user_history(message.from_user.id, 'user', escape_markdown_v2(message.text))
    await message.bot.send_chat_action(
        chat_id=message.from_user.id, action=ChatAction.TYPING
    )
    res = await AI_MODEL.generate(
       db.get_history(message.from_user.id)
    )
    content = escape_markdown_v2(res.choices[0].message.content)
    db.update_user_history(message.from_user.id, 'assistant', content)
    await message.answer(content)
    await state.clear()