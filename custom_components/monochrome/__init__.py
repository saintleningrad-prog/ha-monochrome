"""Monochrome: retro monochrome-monitor themes and effects for Home Assistant.

On setup the integration
  * copies the four Monochrome themes into <config>/themes and reloads themes,
  * serves the effects module and fonts under /monochrome_static,
  * registers the effects module for the whole frontend (like ``frontend: extra_module_url``).
"""

from __future__ import annotations

import filecmp
import logging
import shutil
from pathlib import Path

from homeassistant.components import frontend
from homeassistant.components.frontend import add_extra_js_url, remove_extra_js_url
from homeassistant.components.http import StaticPathConfig
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.util.yaml import load_yaml

from .const import (
    CONF_BOOT,
    CONF_GLITCH,
    CONF_GLITCH_EVERY,
    CONF_PATTERN,
    DEFAULTS,
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
