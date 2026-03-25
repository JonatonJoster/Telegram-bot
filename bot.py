import asyncio
import datetime as dt

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.jobstores.base import ConflictingIdError

from config import config
from database import db
from handlers import user, admin


async def restore_reminder_jobs(bot: Bot, scheduler: AsyncIOScheduler) -> None:
    """
    Відновлює задачі нагадувань при старті бота
    на основі записів у базі даних.
    """
    rows = db.get_future_bookings_for_reminders()
    now = dt.datetime.now()

    for row in rows:
        booking_id = row["booking_id"]
        appointment_dt = dt.datetime.fromisoformat(row["appointment_datetime"])
        user_tg_id = row["tg_id"]

        delta = appointment_dt - now
        reminder_time = appointment_dt - dt.timedelta(hours=24)
        if delta <= dt.timedelta(hours=24):
            continue
        if reminder_time <= now:
            continue

        try:
            scheduler.add_job(
                user.send_reminder_job,
                "date",
                run_date=reminder_time,
                args=[bot.token, user_tg_id, appointment_dt.isoformat()],
                id=f"booking_{booking_id}",
                replace_existing=True,
            )
            db.set_booking_reminder_job(booking_id, f"booking_{booking_id}")
        except ConflictingIdError:
            continue


async def main() -> None:
    """
    Точка входу в додаток.
    """
    db.init_db()

    bot = Bot(token=config.BOT_TOKEN)

    storage = MemoryStorage()
    dp = Dispatcher(storage=storage)

    scheduler = AsyncIOScheduler(timezone="Europe/Kiev")
    scheduler.start()
    # Зберігаємо посилання на планувальник усередині об'єкта бота
    bot.scheduler = scheduler

    dp.include_router(user.router)
    dp.include_router(admin.router)

    await restore_reminder_jobs(bot, scheduler)

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
