from hat.drivers import iec104
import asyncio
import sys


async def async_main():
    connection = await iec104.connect(
        iec104.Address('127.0.0.1', 9999))
    while True:
        data = await connection.receive()
        print(data)


def main():
    asyncio.run(async_main())


# standardna dobra praksa za definiranje ulazne tocke
# u Python program
if __name__ == '__main__':
    sys.exit(main())
