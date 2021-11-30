import asyncio
import sys


async def async_main():
    pass


def main():
    asyncio.run(async_main())


# standardna dobra praksa za definiranje ulazne tocke
# u Python program
if __name__ == '__main__':
    sys.exit(main())
