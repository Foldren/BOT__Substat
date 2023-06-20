import asyncio
import logging
from aiogram import Bot, Dispatcher
from handlers.admins import add_user, remove_user, start_admin
from handlers.analysts import get_statistic, start_analysts
from config import TOKEN


# Запуск процесса поллинга новых апдейтов
async def main():
    # Включаем логирование, чтобы не пропустить важные сообщения
    logging.basicConfig(level=logging.INFO)
    # Объект бота
    bot = Bot(token=TOKEN)
    # Диспетчер
    dp = Dispatcher()
    dp.include_routers(start_admin.rt, add_user.rt, remove_user.rt, start_analysts.rt, get_statistic.rt)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
