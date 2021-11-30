import hat.event.client
import hat.event.common
import asyncio
import random
import sys


async def async_main():
    client = await hat.event.client.connect(
        'tcp+sbs://127.0.0.1:23012', [])

    events = await client.query(
        hat.event.common.QueryData(
            event_types=[
                ('measurement1', 'change', 'abc')]))
    print(events)


def main():
    asyncio.run(async_main())


if __name__ == '__main__':
    sys.exit(main())
