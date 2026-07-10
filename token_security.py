import aiohttp
from config import CHAINS, DEFAULT_CHAIN

GOPLUS_TOKEN_SECURITY_URL = "https://api.gopluslabs.io/api/v1/token_security/{chain_id}"


async def check_token(address: str, chain: str = DEFAULT_CHAIN) -> dict:
    """
    Отримує звіт безпеки токена з GoPlus Security API (безкоштовний, публічний).
    Документація: https://docs.gopluslabs.io/reference/token-security-api
    """
    chain_id = CHAINS.get(chain, CHAINS[DEFAULT_CHAIN])
    url = GOPLUS_TOKEN_SECURITY_URL.format(chain_id=chain_id)
    params = {"contract_addresses": address.lower()}

    async with aiohttp.ClientSession() as session:
        async with session.get(url, params=params, timeout=15) as resp:
            data = await resp.json()

    result = data.get("result", {}).get(address.lower())
    if not result:
        return {"found": False}

    holders = result.get("holders", [])
    top_holder_percent = holders[0].get("percent") if holders else None

    return {
        "found": True,
        "is_honeypot": result.get("is_honeypot") == "1",
        "buy_tax": result.get("buy_tax"),
        "sell_tax": result.get("sell_tax"),
        "is_open_source": result.get("is_open_source") == "1",
        "is_proxy": result.get("is_proxy") == "1",
        "is_mintable": result.get("is_mintable") == "1",
        "owner_can_change_balance": result.get("owner_change_balance") == "1",
        "holder_count": result.get("holder_count"),
        "top_holder_percent": top_holder_percent,
        "lp_locked": result.get("lp_holders"),
    }


def format_token_report(report: dict, address: str) -> str:
    if not report.get("found"):
        return (
            f"⚠️ Не знайдено даних по адресі {address}.\n"
            "Перевірте адресу контракту або спробуйте вказати іншу мережу "
            "(eth, bsc, polygon, arbitrum, base)."
        )

    flags = []
    if report["is_honeypot"]:
        flags.append("🚨 ХАНІПОТ — продати цей токен, схоже, неможливо!")

    try:
        if report["buy_tax"] and float(report["buy_tax"]) > 0.1:
            flags.append(f"⚠️ Високий податок на купівлю: {float(report['buy_tax']) * 100:.1f}%")
        if report["sell_tax"] and float(report["sell_tax"]) > 0.1:
            flags.append(f"⚠️ Високий податок на продаж: {float(report['sell_tax']) * 100:.1f}%")
    except (TypeError, ValueError):
        pass

    if not report["is_open_source"]:
        flags.append("⚠️ Код контракту не верифікований — вищий ризик")
    if report["is_mintable"]:
        flags.append("⚠️ Власник контракту може довільно допемітити нові токени")
    if report["owner_can_change_balance"]:
        flags.append("🚨 Власник контракту може змінювати баланси холдерів!")
    if report["is_proxy"]:
        flags.append("⚠️ Контракт-проксі — логіку можна змінити пізніше")

    if not flags:
        flags.append("✅ Явних червоних прапорців не знайдено")

    text = f"📊 Звіт по токену `{address}`\n\n" + "\n".join(flags)

    if report.get("holder_count"):
        text += f"\n\n👥 Кількість холдерів: {report['holder_count']}"
    if report.get("top_holder_percent"):
        text += f"\n🔝 Частка найбільшого холдера: {report['top_holder_percent']}%"

    text += "\n\n_Дані: GoPlus Security API. Це не фінансова порада, робіть власний DYOR._"
    return text
