import hypercorn
import hypercorn.logging
import trio
from hypercorn.trio import serve

from src.core.app import app as application


async def app(scope, receive, send):
    await application(scope=scope, receive=receive, send=send)


async def main():
    hypercorn_config = hypercorn.Config()
    hypercorn_config.bind = ["localhost:8080"]
    hypercorn_config.use_reloader = True
    await serve(app, hypercorn_config)


if __name__ == "__main__":
    trio.run(main)
