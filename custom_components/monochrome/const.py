"""Constants for the Monochrome integration."""

from __future__ import annotations

from pathlib import Path

DOMAIN = "monochrome"
VERSION = "0.2.3"

URL_BASE = "/monochrome_static"
MODULE_FILE = "monochrome-effects.js"

COMPONENT_DIR = Path(__file__).parent
WWW_DIR = COMPONENT_DIR / "www"
THEMES_SOURCE = COMPONENT_DIR / "themes" / "monochrome.yaml"
THEMES_TARGET_NAME = "monochrome.yaml"
THEME_NAMES = (
    "Monochrome Green",
    "Monochrome Amber",
    "Monochrome Paperblack",
    "Monochrome Paperwhite",
)

CONF_GLITCH = "glitch"
CONF_GLITCH_EVERY = "glitch_every"
CONF_BOOT = "boot"
CONF_PATTERN = "pattern"

DEFAULTS = {
    CONF_GLITCH: True,
    CONF_GLITCH_EVERY: 25,
    CONF_BOOT: True,
    CONF_PATTERN: True,
}

SERVICE_GLITCH = "glitch"
ATTR_INTENSITY = "intensity"
ATTR_DURATION = "duration"
SIGNAL_GLITCH = f"{DOMAIN}_glitch"
