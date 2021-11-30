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

    def __init__(self, visual):
        self._state = {'I1': 0, 'I2': 0, 'I3': 0, 'I4': 0}
        self._visual = visual

    def process(self, iec104_data):
        meter = {0: 'I1',
                 1: 'I2',
                 2: 'I3'}[iec104_data[0].asdu_address]
        self._state[meter] = iec104_data[0].value.value
        self._state['I4'] = (self._state['I1']
                             + self._state['I2']
                             + self._state['I3'])
        self._visual.render(self._state)


class Visual:

    def render(self, state):
        for key, value in state.items():
            print(key, '=', round(value, 2))
        print()


async def async_main():
    visual = Visual()
    processing = Processing(visual)
    communication = Communication(processing)
    await communication.connect()
    await communication.receive_loop()


def main():
    asyncio.run(async_main())


# standardna dobra praksa za definiranje ulazne tocke
# u Python program
if __name__ == '__main__':
    sys.exit(main())
