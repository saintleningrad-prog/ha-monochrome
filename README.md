# Monochrome — retro monochrome-monitor themes for Home Assistant

Four themes in the style of old monochrome CRT terminals, plus effects that make the whole
Home Assistant UI feel like a phosphor screen.

| Theme | Look |
|---|---|
| **Monochrome Green** | green P1 phosphor on black, active items in yellow |
| **Monochrome Amber** | amber P3 phosphor (IBM/Wyse terminals); active items glow bright orange |
| **Monochrome Paperblack** | white P4 phosphor on black, pure monochrome — hierarchy by brightness only |
| **Monochrome Paperwhite** | light: dark text on white, black double frames |

<!-- Screenshots: put images into images/ and reference them here -->

## Features

- Font **IBM VGA 8x16** (with full Cyrillic) everywhere, JetBrains Mono as fallback
- Scanlines, vignette, double card frames, phosphor text glow
- **Live generated background** (“2D Convolution”, new pattern on every load, tinted to the phosphor)
- Boot screen, rare short **glitch** effect
- Card titles on a solid backing, tile text follows the icon state color
- No polling of the UI: effects run only on page load, navigation and theme change
- Works in light and dark UI mode; respects “reduce motion”

## Installation (HACS)

1. HACS → ⋮ → **Custom repositories** → add `https://github.com/saintleningrad-prog/ha-monochrome`, category **Integration**.
2. Install **Monochrome**, restart Home Assistant.
3. **Settings → Devices & services → Add integration → Monochrome**.
4. Profile → **Theme** → pick a Monochrome theme. Reload the page (Ctrl+F5).

Options (gear on the integration): background pattern, boot screen, glitch on/off, glitch frequency.

The integration copies the themes to `<config>/themes/monochrome.yaml`. Your `configuration.yaml` should
contain the default themes include (present in new installations):

```yaml
frontend:
  themes: !include_dir_merge_named themes
```

### Tinting your own images

Images in picture cards are tinted to the current phosphor only if their URL ends with `#monochrome-tint`,
e.g. `/local/logo.svg#monochrome-tint`. Camera snapshots and photos are never altered.

## Credits & licenses

- Code and themes: MIT (see `LICENSE`)
- PxPlus IBM VGA 8x16 — Ultimate Oldschool PC Font Pack by VileR, https://int10h.org — CC BY-SA 4.0
- JetBrains Mono — SIL Open Font License 1.1
- Background algorithm — Fractogenesis by Serhii Herasymov, https://github.com/xcontcom/fractogenesis — MIT

---

## По-русски

Четыре темы в стиле старых монохромных мониторов и эффекты: шрифт IBM VGA с кириллицей, строки развёртки,
виньетка, двойные рамки, свечение текста, живой узор фона, заставка и редкий глич-эффект.

**Установка:** HACS → ⋮ → «Пользовательские репозитории» → URL этого репозитория, категория «Интеграция» →
установить → перезапустить HA → «Настройки → Устройства и службы → Добавить интеграцию → Monochrome» →
в профиле выбрать тему Monochrome → Ctrl+F5.

Параметры эффектов — шестерёнка у интеграции. Картинки в picture-карточках перекрашиваются в цвет
люминофора, только если в конце адреса есть `#monochrome-tint`.
