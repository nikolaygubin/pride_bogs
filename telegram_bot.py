from aiogram import executor, types
from create_bot import dp, bot
from handlers import client, admin
from data_base import sqlite_db
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from work_with_pairs import *
import logging
import os

scheduler = AsyncIOScheduler()

admin.register_handlers_admin(dp)
client.register_handlers_client(dp)

logging.basicConfig(level=logging.INFO)
    
async def on_startup(dp):
    sqlite_db.start_sql()
    # scheduler.add_job(del_promo, 'cron', hour='9', minute='0', timezone='Europe/Moscow')
    scheduler.add_job(make_pairs, 'cron', day_of_week='0', hour='10', minute='0', timezone='Europe/Moscow')
    scheduler.add_job(ask_impress, 'cron', day_of_week='3,5', hour='12', minute='0', timezone='Europe/Moscow')
    scheduler.add_job(is_active, 'cron', day_of_week='6', hour='10', minute='0', timezone='Europe/Moscow')
    # scheduler.add_job(update_paid, 'cron', day_of_week='6', hour='8', minute='0', timezone='Europe/Moscow')
    scheduler.start()
    await bot.set_webhook(os.getenv('URL'))

async def on_shutdown(dp):
    await sqlite_db.close_db()
    await bot.delete_webhook()


async def on_startup_polling(dp):
    sqlite_db.start_sql()
    scheduler.add_job(make_pairs, 'cron', day_of_week='0', hour='10', minute='0', timezone='Europe/Moscow')
    scheduler.add_job(ask_impress, 'cron', day_of_week='3,5', hour='12', minute='0', timezone='Europe/Moscow')
    scheduler.add_job(is_active, 'cron', day_of_week='6', hour='10', minute='0', timezone='Europe/Moscow')
    scheduler.start()

async def on_shutdown_polling(dp):
    await sqlite_db.close_db()

    

if __name__ == "__main__" :
    # executor.start_webhook(
    #     dispatcher = dp,
    #     webhook_path = '',
    #     skip_updates = True,
    #     on_startup = on_startup,
    #     on_shutdown = on_shutdown,
    #     host = "0.0.0.0",
    #     port = int(os.environ.get("PORT", 5000))
    # )
    # sqlite_db.start_sql()
    executor.start_polling(dp, skip_updates=False, on_startup=on_startup_polling, on_shutdown=on_shutdown_polling)

