from hat.drivers import iec104
import asyncio
import sys


class Communication:

    def __init__(self, processing):
        self._connection = None
        self._processing = processing

    async def connect(self):
        self._connection = await iec104.connect(
            iec104.Address('127.0.0.1', 9999))

    async def receive_loop(self):
        while True:
            data = await self._connection.receive()
            self._processing.process(data)


class Processing:

    def __init__(self):
        self._state = {'I1': 0, 'I2': 0, 'I3': 0, 'I4': 0}

    def process(self, iec104_data):
        meter = {0: 'I1',
                 1: 'I2',
                 2: 'I3'}[iec104_data[0].asdu_address]
        self._state[meter] = round(iec104_data[0].value.value, 2)
        self._state['I4'] = round(self._state['I1']
                                  + self._state['I2']
                                  + self._state['I3'], 2)
        print(self._state)


async def async_main():
    processing = Processing()
    communication = Communication(processing)
    await communication.connect()
    await communication.receive_loop()


def main():
    asyncio.run(async_main())


# standardna dobra praksa za definiranje ulazne tocke
# u Python program
if __name__ == '__main__':
    sys.exit(main())
