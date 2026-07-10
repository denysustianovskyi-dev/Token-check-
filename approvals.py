import aiohttp
from config import CHAINS, DEFAULT_CHAIN

GOPLUS_APPROVAL_URL = "https://api.gopluslabs.io/api/v1/approval_security/{chain_id}"


async def check_wallet_approvals(wallet_address: str, chain: str = DEFAULT_CHAIN) -> dict:
    """
    Отримує активні token approvals для гаманця з GoPlus Security API.
    Документація: https://docs.gopluslabs.io/reference/approval-security-api
    Примітка: перед продакшн-використанням звірте точні назви параметрів
    з актуальною документацією GoPlus — API іноді оновлюється.
    """
    chain_id = CHAINS.get(chain, CHAINS[DEFAULT_CHAIN])
    url = GOPLUS_APPROVAL_URL.format(chain_id=chain_id)
    params = {"addresses": wallet_address.lower()}

    async with aiohttp.ClientSession() as session:
        async with session.get(url, params=params, timeout=15) as resp:
            data = await resp.json()

    return data.get("result", {})


def format_approvals_report(result: dict, wallet_address: str) -> str:
    if not result:
        return f"⚠️ Не вдалося отримати дозволи для `{wallet_address}`, або активних дозволів немає."

    risky = []
    total = 0

    for token_addr, token_data in result.items():
        for appr in token_data.get("approved_list", []):
            total += 1
            is_risky = (
                appr.get("risky_types")
                or appr.get("is_contract_owner_risky") == "1"
                or appr.get("is_contract_upgradeable") == "1"
            )
            if is_risky:
                spender = appr.get("approved_contract", "невідомо")
                risky.append(f"🚨 Токен `{token_addr[:10]}…` → дозвіл контракту `{spender[:10]}…`")

    if total == 0:
        return f"ℹ️ Активних дозволів для `{wallet_address}` не знайдено в цій мережі."

    if not risky:
        return (
            f"✅ Перевірено {total} активних дозволів для `{wallet_address}`.\n"
            "Явних ризиків не знайдено.\n\n"
            "_Рекомендуємо періодично перевіряти повторно та відкликати невикористовувані "
            "дозволи через revoke.cash_"
        )

    text = f"⚠️ Знайдено {len(risky)} потенційно ризикованих дозволів з {total} загалом:\n\n"
    text += "\n".join(risky[:15])
    if len(risky) > 15:
        text += f"\n... і ще {len(risky) - 15}"
    text += "\n\n👉 Відкликати дозволи можна тут: https://revoke.cash"
    return text
