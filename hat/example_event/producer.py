import hat.event.client
import hat.event.common
import asyncio
import random
import sys


async def async_main():
    client = await hat.event.client.connect(
        'tcp+sbs://127.0.0.1:23012', [])

    while True:
        client.register([hat.event.common.RegisterEvent(
            event_type=('measurement1', 'change', 'abc'),
            source_timestamp=None,
            payload=hat.event.common.EventPayload(
                type=hat.event.common.EventPayloadType.JSON,
                data={'value': random.randint(0, 10)}))])
        await asyncio.sleep(3)


def main():
    asyncio.run(async_main())


if __name__ == '__main__':
    sys.exit(main())
