from .controller import PoolController
from .const import DOMAIN, SCAN_INTERVAL
from .modbus_handler import ModbusHandler

PLATFORMS = ["sensor", "number", "binary_sensor", "switch"]

async def async_setup_entry(hass, entry):
    hass.data.setdefault(DOMAIN, {})

    data = dict(entry.data)

    host = data["host"]
    port = data["port"]
    unit_id = data["unit_id"]
    handler = ModbusHandler(host, port, unit_id)

    async def _noop(now): pass
    controller = PoolController(hass, _noop, SCAN_INTERVAL, handler)

    hass.data[DOMAIN][entry.entry_id] = {
        **data,
        "controller": controller,
        "scan_interval": SCAN_INTERVAL,
    }

    await controller.start()
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    return True

async def async_unload_entry(hass, entry):
    unloaded = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
    if unloaded:
        entry_data = hass.data[DOMAIN].pop(entry.entry_id, {})
        controller = entry_data.get("controller")
        if controller and controller._remove_listener:
            controller._remove_listener()
    return unloaded
