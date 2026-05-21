from homeassistant.components.sensor import SensorEntity
from homeassistant.helpers.restore_state import RestoreEntity
from .modbus_handler import ModbusHandler
from .const import DOMAIN
from .models import MODELS

async def async_setup_entry(hass, config_entry, async_add_entities):
    data = hass.data[DOMAIN][config_entry.entry_id]
    model_key = data["model"]
    handler = ModbusHandler(data["host"], data["port"], data["unit_id"])

    sensors = []
    for sensor_conf in MODELS[model_key]["sensors"]:
        sensors.append(PoolSensor(
            hass,
            sensor_conf,
            handler,
            config_entry.entry_id,
            MODELS[model_key]["name"]
        ))

    async_add_entities(sensors)

    controller = hass.data[DOMAIN][config_entry.entry_id]["controller"]

    async def update_sensors(now):
        if controller.should_skip_poll():
            return
        for sensor in sensors:
            sensor.update()
            sensor.async_write_ha_state()

    controller._update_callback = update_sensors

class PoolSensor(SensorEntity, RestoreEntity):
    def __init__(self, hass, config, handler, entry_id, model_label):
        self.hass = hass
        self._config = config
        self._handler = handler
        self._entry_id = entry_id
        self._model_label = model_label
        self._state = None

        self._attr_translation_key = config.get("translation_key")
        self._attr_has_entity_name = True
        self._attr_icon = config.get("icon", "mdi:water")
        self._attr_native_unit_of_measurement = config.get("unit", "")
        self._attr_unique_id = config["unique_id"]
        self._attr_should_poll = True

        self._attr_device_class = config.get("device_class")

    @property
    def state(self):
        return self._state

    @property
    def device_info(self):
        return {
            "identifiers": {(DOMAIN, self._entry_id)},
            "name": self._model_label,
            "manufacturer": "Pool Technologie",
            "model": self._model_label
        }

    async def async_added_to_hass(self):
        last_state = await self.async_get_last_state()
        if last_state and self._state is None:
            try:
                self._state = float(last_state.state)
            except ValueError:
                pass
                
    def update(self):
        controller = self.hass.data[DOMAIN][self._entry_id]["controller"]
        result = self._handler.read_register(self._config["address"])

        if result:
            self._state = round(result[0] * self._config.get("scale", 1), self._config.get("precision", 0))
            controller.notify_modbus_success()
        else:
            controller.notify_modbus_failure()
