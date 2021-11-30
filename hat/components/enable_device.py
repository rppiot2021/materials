import hat.event.client
import hat.event.common
import asyncio
import random
import sys


async def async_main():
    client = await hat.event.client.connect(
        'tcp+sbs://127.0.0.1:23012', [])

    await client.register_with_response([
        hat.event.common.RegisterEvent(
            event_type=('gateway', 'gateway1', 'ammeter',
                        'ammeter1', 'system', 'enable'),
            source_timestamp=None,
            payload=hat.event.common.EventPayload(
                type=hat.event.common.EventPayloadType.JSON,
                data=True))])


def main():
    asyncio.run(async_main())


if __name__ == '__main__':
    sys.exit(main())
