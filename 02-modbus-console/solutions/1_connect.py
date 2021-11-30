from hat.drivers import modbus, tcp
import asyncio
import sys


async def async_main():
    master = await modbus.create_tcp_master(
        modbus.ModbusType.TCP,
        tcp.Address('127.0.0.1', 9999))


def main():
    asyncio.run(async_main())


if __name__ == '__main__':
    sys.exit(main())
