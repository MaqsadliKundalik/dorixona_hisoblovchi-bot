from . import start, drugs, users
from aiogram import Router

router = Router()

router.include_router(start.router)
router.include_router(drugs.router)
router.include_router(users.router)