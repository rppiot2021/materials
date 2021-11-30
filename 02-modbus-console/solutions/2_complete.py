from hat.drivers import modbus, tcp
import asyncio
import sys


async def async_main():
    master = await modbus.create_tcp_master(
        modbus.ModbusType.TCP,
        tcp.Address('161.53.17.239', 8502))
    while True:
        data = await master.read(
            device_id=1,
            data_type=modbus.DataType.HOLDING_REGISTER,
            start_address=4003)
        print(data)
        await asyncio.sleep(5)


def main():
    asyncio.run(async_main())


if __name__ == '__main__':
    sys.exit(main())
