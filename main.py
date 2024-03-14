import asyncio
import logging
import sys

from bot import *
from dispatcher import dp, bot


async def main():
    await dp.start_polling(bot)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
