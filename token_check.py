from aiogram import Router, types
from aiogram.filters import Command

from services.token_security import check_token, format_token_report

router = Router()


@router.message(Command("token"))
async def cmd_token(message: types.Message):
    args = message.text.split()[1:]
    if not args:
        await message.answer(
            "Використання: /token <адреса контракту> [мережа]\n"
            "Приклад: /token 0xabc...123 eth"
        )
        return

    address = args[0]
    chain = args[1] if len(args) > 1 else "eth"

    if not address.startswith("0x") or len(address) != 42:
        await message.answer("⚠️ Схоже, адреса контракту некоректна. Перевірте формат (0x... 42 символи).")
        return

    status_msg = await message.answer("🔍 Перевіряю токен, зачекайте кілька секунд...")

    try:
        report = await check_token(address, chain)
        text = format_token_report(report, address)
    except Exception as e:
        text = f"❌ Помилка при перевірці: {e}"

    await status_msg.edit_text(text, parse_mode="Markdown", disable_web_page_preview=True)
