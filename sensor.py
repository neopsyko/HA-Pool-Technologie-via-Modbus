from homeassistant.components.sensor import SensorEntity
from homeassistant.helpers.restore_state import RestoreEntity
from .const import DOMAIN
from .models import MODELS

async def async_setup_entry(hass, config_entry, async_add_entities):
    data = hass.data[DOMAIN][config_entry.entry_id]
    model_key = data["model"]
    handler = data["controller"].handler

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
        any_success = False
        for sensor in sensors:
            ok = await hass.async_add_executor_job(sensor.update)
            if ok:
                any_success = True
            sensor.async_write_ha_state()
        if any_success:
            controller.notify_modbus_success()
        else:
            controller.notify_modbus_failure()

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
        self._attr_unique_id = f"{entry_id}_{config['unique_id']}"
        self._attr_should_poll = False

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
                
    def update(self) -> bool:
        result = self._handler.read_register(self._config["address"])
        if result:
            self._state = round(result[0] * self._config.get("scale", 1), self._config.get("precision", 0))
            self._attr_available = True
            return True
        self._attr_available = False
        return False
