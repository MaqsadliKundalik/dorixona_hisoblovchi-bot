from aiogram.filters import Filter
from config import MAIN_ADMIN, ADMIN
from aiogram.types import Message

class IsMainAdmin(Filter):
    async def __call__(self, message: Message):
        return message.from_user.id == MAIN_ADMIN

class IsAdmin(Filter):
    async def __call__(self, message: Message):
        return message.from_user.id == ADMIN