import random

from string import ascii_letters, digits


symbols = ascii_letters + digits


async def generate_payload_deeplink() -> str:
     return "".join([random.choice(symbols) for _ in range(10)])


async def generate_processid() -> str:
     # aaaaa-aaaaa-aaaaa
     return "-".join(["".join([random.choice(symbols) for _ in range(5)]) for _ in range(3)])


def sync_generate_id() -> int:
     return int("".join([random.choice(digits) for _ in range(10)]))


async def async_generate_id() -> int:
     return int("".join([random.choice(digits) for _ in range(10)]))