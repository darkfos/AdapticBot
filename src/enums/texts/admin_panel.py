from datetime import datetime


async def admin_panel_text(user_name: str) -> str:
    return (
        f"Добро пожаловать в админ панель {user_name}!"
        f"\n\nСегодня: {datetime.now().date()}"
    )
