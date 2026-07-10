from aiogram import Router, types
from aiogram.filters import Command, CommandStart

router = Router()

WELCOME_TEXT = (
    "👋 Привіт! Я допоможу перевірити безпеку в крипті.\n\n"
    "Доступні команди:\n"
    "/token <адреса> [мережа] — перевірити токен на скам/хаунипот\n"
    "/wallet <адреса> [мережа] — перевірити активні дозволи (approvals) гаманця\n\n"
    "Мережі: eth, bsc, polygon, arbitrum, base (за замовчуванням eth)\n\n"
    "Приклад: /token 0x1234567890abcdef1234567890abcdef12345678 bsc"
)


@router.message(CommandStart())
async def cmd_start(message: types.Message):
    await message.answer(WELCOME_TEXT)


@router.message(Command("help"))
async def cmd_help(message: types.Message):
    await message.answer(WELCOME_TEXT)
