from hat.drivers import iec104
import asyncio
import sys


async def async_main():
    connection = await iec104.connect(
        iec104.Address('127.0.0.1', 9999))
    state = {'I1': 0, 'I2': 0, 'I3': 0, 'I4': 0}
    while True:
        data = await connection.receive()
        meter = {0: 'I1', 1: 'I2', 2: 'I3'}[data[0].asdu_address]
        state[meter] = round(data[0].value.value, 2)
        state['I4'] = round(state['I1'] + state['I2'] + state['I3'], 2)
        print(state)


def main():
    asyncio.run(async_main())


# standardna dobra praksa za definiranje ulazne tocke
# u Python program
if __name__ == '__main__':
    sys.exit(main())
