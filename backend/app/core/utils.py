import random

from string import ascii_letters, digits


symbols = ascii_letters + digits


async def id_with_symbols() -> str:
     return "".join([random.choice(symbols) for _ in range(10)])