from dishka.integrations.fastapi import FastapiProvider
from dishka import make_async_container

from .provider import MainProvider


container = make_async_container(MainProvider(), FastapiProvider())