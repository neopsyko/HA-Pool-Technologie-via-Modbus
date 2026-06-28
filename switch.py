from homeassistant.components.switch import SwitchEntity
from homeassistant.exceptions import HomeAssistantError

from .const import DOMAIN
from .models import MODELS

_BOOST_DURATION_REG = 4188
_BOOST_FLAG_REG = 4182
_BOOST_DURATION_MINUTES = 1440  # 24h


async def async_setup_entry(hass, config_entry, async_add_entities):
    controller = hass.data[DOMAIN][config_entry.entry_id]["controller"]
    model_label = MODELS[config_entry.data["model"]]["name"]
    handler = controller.handler

    async_add_entities([
        BoostSwitch(hass, handler, config_entry.entry_id, model_label)
    ])


class BoostSwitch(SwitchEntity):
    def __init__(self, hass, handler, entry_id, model_label):
        self._hass = hass
        self._handler = handler
        self._entry_id = entry_id
        self._model_label = model_label
        self._controller = None

        self._attr_translation_key = "boost"
        self._attr_has_entity_name = True
        self._attr_icon = "mdi:rocket-launch"
        self._attr_unique_id = f"{entry_id}_boost"
        self._attr_is_on = False
        self._attr_should_poll = False

    @property
    def device_info(self):
        return {
            "identifiers": {(DOMAIN, self._entry_id)},
            "name": self._model_label,
            "manufacturer": "Pool Technologie",
            "model": self._model_label,
        }

    async def async_added_to_hass(self):
        result = await self._hass.async_add_executor_job(
            self._handler.read_register, _BOOST_DURATION_REG
        )
        if result is not None:
            self._attr_is_on = result[0] > 0
            self.async_write_ha_state()
        self._controller = self._hass.data[DOMAIN][self._entry_id]["controller"]
        self._controller.add_poll_listener(self._async_poll_refresh)

    async def async_will_remove_from_hass(self):
        if self._controller:
            self._controller.remove_poll_listener(self._async_poll_refresh)

    async def _async_poll_refresh(self):
        result = await self._hass.async_add_executor_job(
            self._handler.read_register, _BOOST_DURATION_REG
        )
        if result is not None:
            is_on = result[0] > 0
            if is_on != self._attr_is_on:
                self._attr_is_on = is_on
                self.async_write_ha_state()

    async def async_turn_on(self, **kwargs):
        ok1 = await self._hass.async_add_executor_job(
            self._handler.write_register, _BOOST_DURATION_REG, _BOOST_DURATION_MINUTES
        )
        ok2 = await self._hass.async_add_executor_job(
            self._handler.write_register, _BOOST_FLAG_REG, 256
        )
        if not ok1 or not ok2:
            raise HomeAssistantError("Échec de l'activation du mode boost")
        self._attr_is_on = True
        self.async_write_ha_state()

    async def async_turn_off(self, **kwargs):
        ok = await self._hass.async_add_executor_job(
            self._handler.write_register, _BOOST_DURATION_REG, 0
        )
        if not ok:
            raise HomeAssistantError("Échec de la désactivation du mode boost")
        self._attr_is_on = False
        self.async_write_ha_state()
