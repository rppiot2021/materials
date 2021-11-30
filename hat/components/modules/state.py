import hat.aio
import hat.event.server.common


json_schema_id = None
json_schema_repo = None


async def create(conf, engine):
    module = StateModule()

    module._subscription = hat.event.server.common.Subscription([
        ('gateway', 'gateway1', 'ammeter', 'ammeter1', 'gateway', '?')])
    module._async_group = hat.aio.Group()
    module._engine = engine
    module._state = {'I1': 0, 'I2': 0, 'I3': 0, 'I4': 0}

    return module


class StateModule(hat.event.server.common.Module):

    @property
    def async_group(self):
        return self._async_group

    @property
    def subscription(self):
        return self._subscription

    async def create_session(self):
        return StateModuleSession(self)

    def get_state_event(self, changes):
        event = changes[0]
        # dohvat zadnjeg elementa tipa dogadaja, za uparivanje s I1, I2, I3
        measurement_id = event.event_type[5]
        current = {'0': 'I1',
                   '1': 'I2',
                   '2': 'I3'}.get(measurement_id)
        if current is None:
            return None
        self._state[current] = event.payload.data
        self._state['I4'] = (self._state['I1']
                             + self._state['I2']
                             + self._state['I3'])

        register_event = hat.event.server.common.RegisterEvent(
            event_type=('state', ),
            source_timestamp=None,
            payload=hat.event.server.common.EventPayload(
                type=hat.event.server.common.EventPayloadType.JSON,
                data=self._state))

        return self._engine.create_process_event(
            hat.event.server.common.Source(
                type=hat.event.server.common.SourceType.MODULE,
                name='modules.state',
                id=1),
            register_event)


class StateModuleSession(hat.event.server.common.ModuleSession):

    def __init__(self, module):
        self._module = module
        self._group = hat.aio.Group()

    @property
    def async_group(self):
        return self._group

    async def process(self, changes):
        # delegacija obrade dogadaja nazad modulu
        state_event = self._module.get_state_event(changes)
        if state_event is None:
            return []
        return [state_event]
