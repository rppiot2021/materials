import hat.event.client
import hat.event.common
import asyncio
import random
import sys


async def async_main():
    client = await hat.event.client.connect(
        'tcp+sbs://127.0.0.1:23012', [
            ('measurement1', 'change', 'abc')])

    while True:
        events = await client.receive()
        print(events)


def main():
    asyncio.run(async_main())


if __name__ == '__main__':
    sys.exit(main())
