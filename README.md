# Monochrome: retro monochrome-monitor themes for Home Assistant

Four themes in the style of old monochrome CRT terminals, plus effects that make the whole
Home Assistant UI feel like a phosphor screen.

> I had wanted to build something like this for Home Assistant for a long time. Thanks to the modern
> world of 04.10.2026, it did not take me long, and the result turned out better than I expected.

## Highlights

1. **Glitch effect, also triggered by events.** Short CRT "signal loss" bursts appear at random
   intervals, and any automation can fire one on demand with the `monochrome.glitch` service:
   a door opening, a doorbell or an alarm makes every open dashboard flicker.
2. **Random background made with generative art.** Every page load grows a brand new pattern with
   the Fractogenesis "2D Convolution" algorithm, dithered and tinted to the current phosphor.
   No two backgrounds are ever the same.
3. **Authentic CRT look.** IBM VGA 8x16 font with full Cyrillic, scanlines, vignette, phosphor glow,
   double card frames and a BIOS-style boot screen.
4. **Four phosphors** in one package, installed with a single HACS integration.

| Theme | Look |
|---|---|
| **Monochrome Green** | green P1 phosphor on black, active items in yellow |
| **Monochrome Amber** | amber P3 phosphor (IBM/Wyse terminals); active items glow bright orange |
| **Monochrome Paperblack** | white P4 phosphor on black, pure monochrome, hierarchy by brightness only |
| **Monochrome Paperwhite** | light: dark text on white, black double frames |

### Green
![Monochrome Green](https://raw.githubusercontent.com/saintleningrad-prog/ha-monochrome/main/images/green.png?v=2)

### Amber
![Monochrome Amber](https://raw.githubusercontent.com/saintleningrad-prog/ha-monochrome/main/images/amber.png?v=2)

### Paperblack
![Monochrome Paperblack](https://raw.githubusercontent.com/saintleningrad-prog/ha-monochrome/main/images/paperblack.png?v=2)

### Paperwhite
![Monochrome Paperwhite](https://raw.githubusercontent.com/saintleningrad-prog/ha-monochrome/main/images/paperwhite.png?v=2)

### Boot screen
![Boot screen](https://raw.githubusercontent.com/saintleningrad-prog/ha-monochrome/main/images/boot.png)

## Features

- Font **IBM VGA 8x16** (with full Cyrillic) everywhere, JetBrains Mono as fallback
- Scanlines, vignette, double card frames, phosphor text glow
- **Live generated background** (“2D Convolution”, new pattern on every load, tinted to the phosphor)
- Boot screen, rare short **glitch** effect, also on demand from automations (`monochrome.glitch`)
- Card titles on a solid backing, tile text follows the icon state color
- No polling of the UI: effects run only on page load, navigation and theme change
- Works in light and dark UI mode; respects “reduce motion”

## Installation (HACS)

1. HACS → ⋮ → **Custom repositories** → add `https://github.com/saintleningrad-prog/ha-monochrome`, category **Integration**.
2. Install **Monochrome**, restart Home Assistant.
3. **Settings → Devices & services → Add integration → Monochrome**.
4. Profile → **Theme** → pick a Monochrome theme. Reload the page (Ctrl+F5).

Options (gear on the integration): background pattern, boot screen, glitch on/off, glitch frequency.
Changes apply after reloading the browser page.

The integration copies the themes to `<config>/themes/monochrome.yaml`. Your `configuration.yaml` should
contain the default themes include (present in new installations):

```yaml
frontend:
  themes: !include_dir_merge_named themes
```

## Glitch effect in YAML

### Options in configuration.yaml

Instead of the gear dialog, the effect options can be set in `configuration.yaml`:

```yaml
monochrome:
  glitch: true        # random glitches on/off
  glitch_every: 60    # average seconds between random glitches (5 to 600)
  boot: true          # boot screen on first open
  pattern: true       # live generated background
```

All keys are optional; missing ones use the defaults shown above (`glitch_every` defaults to 25).
If the `monochrome:` block is present, it is the source of truth: the integration is added automatically
if needed, its options are overwritten on every restart and the gear dialog is disabled.
Remove the block to manage the options in the UI again. Restart Home Assistant after editing, then
reload the browser page.

### Triggering a glitch from automations

The `monochrome.glitch` service runs a glitch right away on every open Home Assistant tab that uses
a Monochrome theme. It works even when random glitches are turned off.

| Field | Default | Range | Meaning |
|---|---|---|---|
| `intensity` | 3 | 1 to 10 | number of distorted strips and how far they shift |
| `duration` | 0.3 | 0.05 to 5 | how long the glitch lasts, in seconds |

Glitch when the front door opens:

```yaml
automation:
  - alias: "Glitch on door open"
    triggers:
      - trigger: state
        entity_id: binary_sensor.front_door
        to: "on"
    actions:
      - action: monochrome.glitch
        data:
          intensity: 8
          duration: 1
```

A dashboard button:

```yaml
type: button
name: Glitch
icon: mdi:television-classic-off
tap_action:
  action: perform-action
  perform_action: monochrome.glitch
  data:
    intensity: 5
```

Tabs that are in the background, and browsers with "reduce motion" enabled, skip the glitch.
The service is pushed to the browser over the existing Home Assistant connection, nothing is polled.

## Tinting your own images

Images in picture cards are tinted to the current phosphor only if their URL ends with `#monochrome-tint`,
e.g. `/local/logo.svg#monochrome-tint`. Camera snapshots and photos are never altered.

## Credits & licenses

- Code and themes: MIT (see `LICENSE`); third-party components: see `THIRD_PARTY_NOTICES.md`
- PxPlus IBM VGA 8x16: Ultimate Oldschool PC Font Pack by VileR, https://int10h.org, CC BY-SA 4.0
- JetBrains Mono: SIL Open Font License 1.1
- Background algorithm: Fractogenesis by Serhii Herasymov, https://github.com/xcontcom/fractogenesis, MIT

