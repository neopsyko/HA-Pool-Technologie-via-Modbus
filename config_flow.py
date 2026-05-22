import voluptuous as vol
from homeassistant import config_entries
from .const import (
    DOMAIN,
    CONF_HOST,
    CONF_PORT,
    CONF_UNIT_ID,
    CONF_MODEL,
)
from .models import MODELS

class PoolTechnologieConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    async def async_step_user(self, user_input=None):
        if user_input is not None:
            model_name = MODELS[user_input[CONF_MODEL]]["name"]
            return self.async_create_entry(
                title=model_name,
                data={
                    CONF_HOST: user_input[CONF_HOST],
                    CONF_PORT: user_input[CONF_PORT],
                    CONF_UNIT_ID: user_input[CONF_UNIT_ID],
                    CONF_MODEL: user_input[CONF_MODEL],
                }
            )

        schema = vol.Schema({
            vol.Required(CONF_HOST): str,
            vol.Required(CONF_PORT, default=502): int,
            vol.Required(CONF_UNIT_ID, default=1): int,
            vol.Required(CONF_MODEL): vol.In({k: v["name"] for k, v in MODELS.items()}),
        })

        return self.async_show_form(step_id="user", data_schema=schema)

    async def async_step_reconfigure(self, user_input=None):
        entry = self._get_reconfigure_entry()
        if user_input is not None:
            model_name = MODELS[user_input[CONF_MODEL]]["name"]
            return self.async_update_reload_and_abort(
                entry,
                title=model_name,
                data={
                    CONF_HOST: user_input[CONF_HOST],
                    CONF_PORT: user_input[CONF_PORT],
                    CONF_UNIT_ID: user_input[CONF_UNIT_ID],
                    CONF_MODEL: user_input[CONF_MODEL],
                },
            )

        schema = vol.Schema({
            vol.Required(CONF_HOST, default=entry.data.get(CONF_HOST, "")): str,
            vol.Required(CONF_PORT, default=entry.data.get(CONF_PORT, 502)): int,
            vol.Required(CONF_UNIT_ID, default=entry.data.get(CONF_UNIT_ID, 1)): int,
            vol.Required(CONF_MODEL, default=entry.data.get(CONF_MODEL)): vol.In(
                {k: v["name"] for k, v in MODELS.items()}
            ),
        })

        return self.async_show_form(step_id="reconfigure", data_schema=schema)

    @staticmethod
    def async_get_options_flow(config_entry):
        return PoolTechnologieOptionsFlow()


class PoolTechnologieOptionsFlow(config_entries.OptionsFlow):
    async def async_step_init(self, user_input=None):
        entry = self.config_entry
        if user_input is not None:
            self.hass.config_entries.async_update_entry(
                entry,
                title=MODELS[user_input[CONF_MODEL]]["name"],
                data={
                    CONF_HOST: user_input[CONF_HOST],
                    CONF_PORT: user_input[CONF_PORT],
                    CONF_UNIT_ID: user_input[CONF_UNIT_ID],
                    CONF_MODEL: user_input[CONF_MODEL],
                },
            )
            await self.hass.config_entries.async_reload(entry.entry_id)
            return self.async_create_entry(title="", data={})

        schema = vol.Schema({
            vol.Required(CONF_HOST, default=entry.data.get(CONF_HOST, "")): str,
            vol.Required(CONF_PORT, default=entry.data.get(CONF_PORT, 502)): int,
            vol.Required(CONF_UNIT_ID, default=entry.data.get(CONF_UNIT_ID, 1)): int,
            vol.Required(CONF_MODEL, default=entry.data.get(CONF_MODEL)): vol.In(
                {k: v["name"] for k, v in MODELS.items()}
            ),
        })

        return self.async_show_form(step_id="init", data_schema=schema)
