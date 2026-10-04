"""Config and options flow for Monochrome."""

from __future__ import annotations

from typing import Any

import voluptuous as vol

from homeassistant.config_entries import ConfigEntry, ConfigFlow, ConfigFlowResult, OptionsFlow
from homeassistant.core import callback

from .const import CONF_BOOT, CONF_GLITCH, CONF_GLITCH_EVERY, CONF_PATTERN, DEFAULTS, DOMAIN


class MonochromeConfigFlow(ConfigFlow, domain=DOMAIN):
    """Single-instance setup: nothing to ask, just confirm."""

    VERSION = 1

    async def async_step_user(self, user_input: dict[str, Any] | None = None) -> ConfigFlowResult:
        await self.async_set_unique_id(DOMAIN)
        self._abort_if_unique_id_configured()
        if user_input is not None:
            return self.async_create_entry(title="Monochrome", data={})
        return self.async_show_form(step_id="user")

    @staticmethod
    @callback
    def async_get_options_flow(config_entry: ConfigEntry) -> OptionsFlow:
        return MonochromeOptionsFlow()


class MonochromeOptionsFlow(OptionsFlow):
    """Effects settings."""

    async def async_step_init(self, user_input: dict[str, Any] | None = None) -> ConfigFlowResult:
        if user_input is not None:
            return self.async_create_entry(data=user_input)

        opts = {**DEFAULTS, **self.config_entry.options}
        schema = vol.Schema(
            {
                vol.Required(CONF_PATTERN, default=opts[CONF_PATTERN]): bool,
                vol.Required(CONF_BOOT, default=opts[CONF_BOOT]): bool,
                vol.Required(CONF_GLITCH, default=opts[CONF_GLITCH]): bool,
                vol.Required(CONF_GLITCH_EVERY, default=opts[CONF_GLITCH_EVERY]): vol.All(
                    vol.Coerce(int), vol.Range(min=5, max=600)
                ),
            }
        )
        return self.async_show_form(step_id="init", data_schema=schema)
