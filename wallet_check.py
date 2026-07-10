from aiogram import Router, types
from aiogram.filters import Command

from services.approvals import check_wallet_approvals, format_approvals_report

router = Router()


@router.message(Command("wallet"))
async def cmd_wallet(message: types.Message):
    args = message.text.split()[1:]
    if not args:
        await message.answer(
            "Використання: /wallet <адреса гаманця> [мережа]\n"
            "Приклад: /wallet 0xabc...123 eth"
        )
        return

    address = args[0]
    chain = args[1] if len(args) > 1 else "eth"

    if not address.startswith("0x") or len(address) != 42:
        await message.answer("⚠️ Схоже, адреса гаманця некоректна. Перевірте формат (0x... 42 символи).")
        return

    status_msg = await message.answer("🔍 Перевіряю дозволи гаманця, зачекайте кілька секунд...")

    try:
        result = await check_wallet_approvals(address, chain)
        text = format_approvals_report(result, address)
    except Exception as e:
        text = f"❌ Помилка при перевірці: {e}"

    await status_msg.edit_text(text, parse_mode="Markdown", disable_web_page_preview=True)
