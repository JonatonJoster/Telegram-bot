from dataclasses import dataclass


@dataclass
class Config:
    """
    Основна конфігурація бота.

    ОБОВ'ЯЗКОВО:
    - Заповніть BOT_TOKEN
    - Вкажіть ADMIN_ID (ціле число)
    - Вкажіть CHANNEL_ID та CHANNEL_LINK для перевірки підписки
    - Вкажіть SCHEDULE_CHANNEL_ID для каналу з розкладом
    """

    # Токен бота від BotFather
    BOT_TOKEN: str = "8589415869:AAFpXZE4fhzvbzkmlfy_dfyE9IBQpr_pWoU"

    # Telegram ID адміністратора (int)
    ADMIN_ID: int = 1419772420

    # Канал для обов'язкової підписки
    CHANNEL_ID: int = -1003739979311  # ID каналу з мінусом, як у Telegram
    CHANNEL_LINK: str = "https://t.me/asdadsafasfasf"

    # Канал, куди надсилати повідомлення з розкладом
    SCHEDULE_CHANNEL_ID: int = -1003739979311


config = Config()
