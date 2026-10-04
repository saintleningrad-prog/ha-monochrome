"""Monochrome: retro monochrome-monitor themes and effects for Home Assistant.

On setup the integration
  * copies the four Monochrome themes into <config>/themes and reloads themes,
  * serves the effects module and fonts under /monochrome_static,
  * registers the effects module for the whole frontend (like ``frontend: extra_module_url``),
  * provides the ``monochrome.glitch`` service, delivered to open browser tabs over the HA websocket.

Effect options can also be set in configuration.yaml (``monochrome:``); YAML then overrides the UI options.
"""

from __future__ import annotations

import filecmp
import logging
import shutil
from pathlib import Path

import voluptuous as vol

from homeassistant.components import frontend, websocket_api
from homeassistant.components.frontend import add_extra_js_url, remove_extra_js_url
from homeassistant.components.http import StaticPathConfig
from homeassistant.config_entries import SOURCE_IMPORT, ConfigEntry
from homeassistant.core import HomeAssistant, ServiceCall, callback
from homeassistant.helpers import config_validation as cv
from homeassistant.helpers.dispatcher import async_dispatcher_connect, async_dispatcher_send
from homeassistant.helpers.typing import ConfigType
from homeassistant.util.yaml import load_yaml

from .const import (
    CONF_BOOT,
    CONF_GLITCH,
    CONF_GLITCH_EVERY,
    CONF_PATTERN,
    DEFAULTS,
    ATTR_DURATION,
    ATTR_INTENSITY,
    SERVICE_GLITCH,
    SIGNAL_GLITCH,
    DOMAIN,
    MODULE_FILE,
    THEME_NAMES,
    THEMES_SOURCE,
    THEMES_TARGET_NAME,
    URL_BASE,
    VERSION,
    WWW_DIR,
)

_LOGGER = logging.getLogger(__name__)

DATA_THEMES = getattr(frontend, "DATA_THEMES", "frontend_themes")
EVENT_THEMES_UPDATED = getattr(frontend, "EVENT_THEMES_UPDATED", "themes_updated")


CONFIG_SCHEMA = vol.Schema(
    {
        DOMAIN: vol.Any(
            None,
            vol.Schema(
                {
                    vol.Optional(CONF_PATTERN): cv.boolean,
                    vol.Optional(CONF_BOOT): cv.boolean,
                    vol.Optional(CONF_GLITCH): cv.boolean,
                    vol.Optional(CONF_GLITCH_EVERY): vol.All(vol.Coerce(int), vol.Range(min=5, max=600)),
                }
            ),
        )
    },
    extra=vol.ALLOW_EXTRA,
)

GLITCH_SCHEMA = vol.Schema(
    {
        vol.Optional(ATTR_INTENSITY, default=3): vol.All(vol.Coerce(int), vol.Range(min=1, max=10)),
        vol.Optional(ATTR_DURATION, default=0.3): vol.All(vol.Coerce(float), vol.Range(min=0.05, max=5)),
    }
)


async def async_setup(hass: HomeAssistant, config: ConfigType) -> bool:
    """Register the glitch service and websocket command; apply options from configuration.yaml."""

    async def _glitch(call: ServiceCall) -> None:
        async_dispatcher_send(hass, SIGNAL_GLITCH, dict(call.data))

    hass.services.async_register(DOMAIN, SERVICE_GLITCH, _glitch, schema=GLITCH_SCHEMA)
    websocket_api.async_register_command(hass, _ws_subscribe)

    if DOMAIN in config:
        options = {**DEFAULTS, **(config[DOMAIN] or {})}
        hass.data.setdefault(DOMAIN, {})["yaml"] = True
        entries = hass.config_entries.async_entries(DOMAIN)
        if not entries:
            hass.async_create_task(
                hass.config_entries.flow.async_init(DOMAIN, context={"source": SOURCE_IMPORT}, data=options)
            )
        elif dict(entries[0].options) != options:
            hass.config_entries.async_update_entry(entries[0], options=options)
    return True


@websocket_api.websocket_command({vol.Required("type"): "monochrome/subscribe"})
@callback
def _ws_subscribe(hass: HomeAssistant, connection: websocket_api.ActiveConnection, msg: dict) -> None:
    """Browser tabs subscribe here; every monochrome.glitch call is forwarded to them."""

    @callback
    def forward(data: dict) -> None:
        connection.send_message(websocket_api.event_message(msg["id"], data))

    connection.subscriptions[msg["id"]] = async_dispatcher_connect(hass, SIGNAL_GLITCH, forward)
    connection.send_result(msg["id"])


def _option(entry: ConfigEntry, key: str):
    return entry.options.get(key, DEFAULTS[key])


def _module_url(entry: ConfigEntry) -> str:
    flag = lambda key: "1" if _option(entry, key) else "0"  # noqa: E731
    return (
        f"{URL_BASE}/{MODULE_FILE}?v={VERSION}"
        f"&glitch={flag(CONF_GLITCH)}&every={int(_option(entry, CONF_GLITCH_EVERY))}"
        f"&boot={flag(CONF_BOOT)}&pattern={flag(CONF_PATTERN)}"
    )


def _install_themes(themes_dir: Path) -> bool:
    """Copy the themes file into <config>/themes. Returns True if the file changed."""
    themes_dir.mkdir(parents=True, exist_ok=True)
    target = themes_dir / THEMES_TARGET_NAME
    if target.exists() and filecmp.cmp(THEMES_SOURCE, target, shallow=False):
        return False
    shutil.copyfile(THEMES_SOURCE, target)
    return True


def _remove_themes(themes_dir: Path) -> None:
    target = themes_dir / THEMES_TARGET_NAME
    if target.exists():
        target.unlink()


async def _ensure_themes_loaded(hass: HomeAssistant) -> None:
    """Reload themes; if <config>/themes is not included in configuration.yaml, inject them directly."""
    await hass.services.async_call("frontend", "reload_themes", blocking=True)
    loaded = hass.data.get(DATA_THEMES) or {}
    if all(name in loaded for name in THEME_NAMES):
        return
    themes = await hass.async_add_executor_job(load_yaml, str(THEMES_SOURCE))
    if isinstance(loaded, dict):
        loaded.update(themes)
        hass.bus.async_fire(EVENT_THEMES_UPDATED)
    _LOGGER.warning(
        "Monochrome themes were added for this session only. To keep them after "
        "'Reload themes', add to configuration.yaml:  frontend: themes: !include_dir_merge_named themes"
    )


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up Monochrome from a config entry."""
    data = hass.data.setdefault(DOMAIN, {})

    if not data.get("static_registered"):
        await hass.http.async_register_static_paths(
            [StaticPathConfig(URL_BASE, str(WWW_DIR), cache_headers=True)]
        )
        data["static_registered"] = True

    url = _module_url(entry)
    add_extra_js_url(hass, url)
    data["module_url"] = url

    await hass.async_add_executor_job(_install_themes, Path(hass.config.path("themes")))
    await _ensure_themes_loaded(hass)

    entry.async_on_unload(entry.add_update_listener(_async_update_listener))
    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload: stop serving the effects module to newly opened browser tabs."""
    url = hass.data.get(DOMAIN, {}).pop("module_url", None)
    if url:
        remove_extra_js_url(hass, url)
    return True


async def async_remove_entry(hass: HomeAssistant, entry: ConfigEntry) -> None:
    """Integration removed: delete the themes file and reload themes."""
    await hass.async_add_executor_job(_remove_themes, Path(hass.config.path("themes")))
    await hass.services.async_call("frontend", "reload_themes", blocking=True)


async def _async_update_listener(hass: HomeAssistant, entry: ConfigEntry) -> None:
    """Options changed: re-register the module with new parameters."""
    await hass.config_entries.async_reload(entry.entry_id)
