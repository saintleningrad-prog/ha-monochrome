"""Генератор тем Monochrome для Home Assistant (интеграция custom_components/monochrome).

Палитра: текст/данные — зелёный, активное — ярко-жёлтый, неактивное — светло-серый, тревога — красный.
Смысловые токены --ha-color-* задаются напрямую (не через палитру), поэтому тема одинаково
выглядит при светлом и тёмном режиме интерфейса.
"""

# шрифт всех тем Monochrome — IBM VGA 8x16 (с кириллицей); JetBrains Mono — запасной для отсутствующих символов
FONT = ("'Matrix VGA', 'Matrix Mono', 'JetBrains Mono', 'Courier New', monospace, "
        "'Segoe UI Emoji', 'Apple Color Emoji', 'Noto Color Emoji'")

G = "#00ff41"      # основной зелёный (текст, данные)
G2 = "#39ff14"     # яркий зелёный (заголовки, ссылки, акцент)
G_DIM = "#00b32c"  # вторичный текст
G_DARK = "#0b3d12" # разделители
Y = "#ffea00"      # активное
GR = "#c8c8c8"     # неактивное
GR_D = "#8a8a8a"   # недоступно / disabled
R = "#ff2a2a"      # тревога
BLACK = "#000000"


def semantic():
    t = {}
    # заливки: quiet (едва заметная) / normal (средняя) / loud (яркая); resting / hover / active
    fills = {
        "primary": (("#00230a", "#00331a", "#004420"), ("#005a1a", "#007a24", "#009a2e"), (G, G2, "#00cc34")),
        "success": (("#00230a", "#00331a", "#004420"), ("#005a1a", "#007a24", "#009a2e"), (G, G2, "#00cc34")),
        "neutral": (("#001004", "#002108", "#003010"), ("#0a2a10", "#103a18", "#164a20"), (GR, "#dcdcdc", "#b0b0b0")),
        "warning": (("#1f1c00", "#2e2a00", "#3d3800"), ("#6b5f00", "#8a7a00", "#a89400"), (Y, "#fff04d", "#e6d200")),
        "danger":  (("#2a0505", "#3a0808", "#4a0b0b"), ("#6b0f0f", "#8a1515", "#a81c1c"), (R, "#ff5555", "#e01e1e")),
        "disabled": (("#141414", "#1c1c1c", "#1c1c1c"), ("#262626", "#2e2e2e", "#2e2e2e"), ("#4a4a4a", "#555555", "#555555")),
    }
    for kind, levels in fills.items():
        for lvl, vals in zip(("quiet", "normal", "loud"), levels):
            for st, v in zip(("resting", "hover", "active"), vals):
                t[f"ha-color-fill-{kind}-{lvl}-{st}"] = v
    # текст/иконки поверх заливок
    on = {"primary": G2, "success": G, "neutral": G, "warning": Y, "danger": "#ff5555", "disabled": GR_D}
    for kind, v in on.items():
        t[f"ha-color-on-{kind}-quiet"] = v
        t[f"ha-color-on-{kind}-normal"] = v if kind != "disabled" else GR_D
        t[f"ha-color-on-{kind}-loud"] = BLACK if kind != "disabled" else GR
    # рамки
    borders = {"primary": (G_DARK, "#00802b", G), "success": (G_DARK, "#00802b", G),
               "neutral": (G_DARK, "#1f5f2a", GR), "warning": ("#4d4600", "#b3a300", Y),
               "danger": ("#4d0f0f", "#b31d1d", R)}
    for kind, (q, n, l) in borders.items():
        t[f"ha-color-border-{kind}-quiet"] = q
        t[f"ha-color-border-{kind}-normal"] = n
        t[f"ha-color-border-{kind}-loud"] = l
    t["ha-color-border-normal"] = "#00802b"
    # текст и поверхности
    t.update({
        "ha-color-text-primary": G, "ha-color-text-secondary": G_DIM, "ha-color-text-disabled": GR_D,
        "ha-color-text-link": G2, "ha-color-text-primary-inverted": BLACK, "ha-color-text-secondary-inverted": "#1a1a1a",
        "ha-color-surface-default": "#000000", "ha-color-surface-low": "#020a03", "ha-color-surface-lower": "#041206",
        "ha-color-surface-default-inverted": G, "ha-color-surface-low-inverted": G_DIM,
        "ha-color-surface-lower-inverted": "#00802b", "ha-color-on-surface-default": G,
        "ha-color-focus": Y, "ha-color-form-background": "#020d04",
        "ha-color-form-background-hover": "#061a09", "ha-color-form-background-disabled": "#141414",
        "ha-color-shadow-scrollable-fade": "rgba(0, 255, 65, 0.15)",
        "ha-color-black": BLACK, "ha-color-white": "#e6ffe8",
    })
    # палитра primary (на случай мест, где она используется напрямую) — зелёная
    for step, v in zip(("05", "10", "20", "30", "40", "50", "60", "70", "80", "90", "95"),
                       ("#001a06", "#00290a", "#004d13", "#00801f", "#00b32c", "#00e63a", G2,
                        "#66ff73", "#99ffa3", "#ccffd1", "#e6ffe8")):
        t[f"ha-color-primary-{step}"] = v
    return t


def legacy(lite):
    card_bg = "rgba(0, 12, 2, 0.87)"  # карточки прозрачны на 13% во всех темах (и в Lite)
    return {
        # фон и шапки
        # фон: строки развёртки + виньетка + живой узор (matrix-bg.js кладёт его в --matrix-bg-img)
        "lovelace-background": "#000" if lite else (
            "repeating-linear-gradient(0deg, rgba(0,0,0,0.30) 0px, rgba(0,0,0,0.30) 1px, transparent 1px, transparent 3px) fixed, "
            "radial-gradient(ellipse at center, rgba(0,0,0,0) 55%, rgba(0,0,0,0.80) 100%) fixed, "
            "var(--matrix-bg-img, linear-gradient(#000, #000)) center / cover no-repeat fixed, #000"),
        "primary-background-color": BLACK, "secondary-background-color": "#020802",
        "app-header-background-color": BLACK, "app-header-text-color": G,
        "app-header-border-bottom": f"1px solid {G_DARK}", "app-header-selection-bar-color": Y,
        "sidebar-background-color": BLACK, "sidebar-text-color": "#00c832", "sidebar-icon-color": "#00c832",
        "sidebar-selected-text-color": Y, "sidebar-selected-icon-color": Y,
        "sidebar-menu-button-text-color": G, "sidebar-menu-button-background-color": BLACK,
        # текст и шрифт
        "primary-text-color": G, "secondary-text-color": G_DIM, "disabled-text-color": "#9e9e9e",
        "text-primary-color": BLACK, "text-light-primary-color": G,
        "primary-font-family": FONT, "ha-font-family-body": FONT, "ha-font-family-heading": FONT,
        "ha-font-family-code": FONT, "paper-font-common-base_-_font-family": FONT,
        "rgb-primary-text-color": "0, 255, 65", "rgb-secondary-text-color": "0, 179, 44",
        # акценты
        "primary-color": G, "rgb-primary-color": "0, 255, 65", "dark-primary-color": "#00b32c",
        "light-primary-color": "#99ffa3", "accent-color": G2, "rgb-accent-color": "57, 255, 20",
        "divider-color": G_DARK, "outline-color": "#0b5a1d", "outline-hover-color": G,
        "scrollbar-thumb-color": "#0b5a1d",
        # карточки
        "card-background-color": card_bg,
        "ha-card-background": card_bg if lite else (
            "repeating-linear-gradient(0deg, rgba(0,0,0,0.22) 0px, rgba(0,0,0,0.22) 1px, transparent 1px, transparent 3px), "
            + card_bg),
        "rgb-card-background-color": "3, 13, 5",
        "ha-card-border-color": G, "ha-card-border-width": "1px", "ha-card-border-radius": "4px",
        # двойная рамка (рамка карточки + зазор + вторая линия) и свечение
        "ha-card-box-shadow": "none" if lite else
            "0 0 0 3px #000, 0 0 0 4px rgba(0, 255, 65, 0.85), 0 0 12px rgba(0, 255, 65, 0.35)",
        # эффекты модуля matrix-bg.js: свечение текста, заставка, узор фона
        "matrix-glow": "none" if lite else "0 0 3px currentColor",
        # глич-эффект: 1 — вкл, 0 — выкл; every — среднее число секунд между «сбоями»
        "matrix-glitch": "0" if lite else "1", "matrix-glitch-every": "25",
        "matrix-boot": "0" if lite else "1",
        "matrix-pattern": "0" if lite else "1",
        "matrix-bg-tint": "0 1 0.18",
        "ha-card-header-color": G2, "ha-card-header-font-family": FONT,
        # заголовки на чёрной подложке (стиль вставляет /local/matrix/matrix-bg.js); откат — убрать эти 5 строк
        "matrix-title-bg": BLACK, "matrix-title-clip": "content-box", "matrix-title-lh": "1.25",
        "matrix-title-ring": "none", "matrix-title-shadow": "0 0 6px rgba(57, 255, 20, 0.7)",
        "matrix-title-width": "fit-content", "matrix-title-radius": "2px",
        # верхняя панель в режиме редактирования дашборда (по умолчанию HA — серо-синяя #455a64)
        "matrix-tile-follow-icon": "1",  # текст плитки = цвет её иконки (правило вставляет matrix-bg.js)
        "app-header-edit-background-color": "#062b0d", "app-header-edit-text-color": G,  # жёлтый — только выбранная вкладка
        "ha-heading-card-title-color": G2, "ha-heading-card-subtitle-color": "#00c832",
        "markdown-code-background-color": "#001a05",
        "table-header-background-color": "#031a07",
        "table-row-background-color": "rgba(0, 20, 4, 0.6)",
        "table-row-alternative-background-color": "rgba(0, 40, 8, 0.6)",
        # диалоги и меню
        "ha-dialog-surface-background": "#020a03", "mdc-theme-surface": "#020a03",
        "mdc-theme-background": BLACK, "mdc-theme-primary": G, "mdc-theme-secondary": G2,
        "mdc-theme-on-primary": BLACK, "mdc-theme-on-secondary": BLACK, "mdc-theme-on-surface": G,
        "mdc-theme-error": R,
        "mdc-theme-text-primary-on-background": G, "mdc-theme-text-secondary-on-background": G_DIM,
        "mdc-theme-text-hint-on-background": G_DIM, "mdc-theme-text-icon-on-background": G,
        "mdc-theme-text-disabled-on-light": GR_D,
        "material-body-text-color": G, "material-background-color": "#020a03",
        "material-secondary-background-color": "#041206", "material-secondary-text-color": G_DIM,
        "mdc-dialog-scrim-color": "rgba(0, 0, 0, 0.7)",
        "ha-assist-chip-filled-container-color": "#00230a", "ha-assist-chip-active-container-color": "#005a1a",
        # поля ввода
        "input-fill-color": "rgba(0, 30, 6, 0.8)", "input-ink-color": G, "input-label-ink-color": G_DIM,
        "input-idle-line-color": "#0b5a1d", "input-hover-line-color": G, "input-dropdown-icon-color": G,
        "input-disabled-fill-color": "#141414", "input-disabled-ink-color": GR_D, "input-disabled-line-color": "#333333",
        "input-outlined-idle-border-color": "#0b5a1d", "input-outlined-hover-border-color": G,
        "input-outlined-disabled-border-color": "#333333",
        "mdc-text-field-fill-color": "rgba(0, 30, 6, 0.8)", "mdc-text-field-ink-color": G,
        "mdc-text-field-label-ink-color": G_DIM, "mdc-text-field-idle-line-color": "#0b5a1d",
        "mdc-text-field-hover-line-color": G, "mdc-text-field-disabled-fill-color": "#141414",
        "mdc-text-field-disabled-ink-color": GR_D, "mdc-text-field-disabled-line-color": "#333333",
        "mdc-text-field-outlined-idle-border-color": "#0b5a1d",
        "mdc-text-field-outlined-hover-border-color": G,
        "mdc-text-field-outlined-disabled-border-color": "#333333",
        "mdc-select-fill-color": "rgba(0, 30, 6, 0.8)", "mdc-select-ink-color": G,
        "mdc-select-label-ink-color": G_DIM, "mdc-select-idle-line-color": "#0b5a1d",
        "mdc-select-hover-line-color": G, "mdc-select-dropdown-icon-color": G,
        "mdc-select-disabled-fill-color": "#141414", "mdc-select-disabled-ink-color": GR_D,
        "mdc-select-disabled-dropdown-icon-color": GR_D,
        "mdc-select-outlined-idle-border-color": "#0b5a1d", "mdc-select-outlined-hover-border-color": G,
        "mdc-select-outlined-disabled-border-color": "#333333",
        # редактор кода (YAML, шаблоны)
        "code-editor-background-color": "#000000",
        "codemirror-keyword": Y, "codemirror-atom": G2, "codemirror-number": "#99ffa3",
        "codemirror-def": G2, "codemirror-variable": G, "codemirror-variable-2": "#66ff73",
        "codemirror-variable-3": "#66ff73", "codemirror-type": Y, "codemirror-comment": "#5f8a66",
        "codemirror-string": "#ccffd1", "codemirror-string-2": "#ccffd1", "codemirror-meta": G_DIM,
        "codemirror-qualifier": G2, "codemirror-builtin": Y, "codemirror-tag": G2,
        "codemirror-attribute": "#66ff73", "codemirror-property": G, "codemirror-operator": GR,
        # иконки и состояния: активное — жёлтый, неактивное — светло-серый
        "state-icon-color": G, "paper-item-icon-color": G, "paper-item-icon-active-color": Y,
        "state-icon-active-color": Y, "state-active-color": Y, "state-on-color": Y,
        "state-inactive-color": GR, "state-off-color": GR, "state-unavailable-color": GR_D,
        "state-light-active-color": Y, "state-light-on-color": Y,
        "state-switch-active-color": Y, "state-switch-on-color": Y,
        "state-binary_sensor-active-color": Y, "state-binary_sensor-on-color": Y,
        "state-binary_sensor-inactive-color": GR,
        "state-input_boolean-active-color": Y, "state-automation-active-color": Y,
        "state-media_player-active-color": Y, "state-fan-active-color": Y,
        "switch-checked-color": Y, "switch-checked-button-color": Y, "switch-checked-track-color": "#8a7f00",
        "switch-unchecked-button-color": GR, "switch-unchecked-track-color": "#5a5a5a",
        # стрелки, графики, статусы
        "success-color": G, "warning-color": Y, "error-color": R, "info-color": "#00c832",
        "gauge-color": G,
        "graph-color-1": G, "graph-color-2": Y, "graph-color-3": "#7dff9e", "graph-color-4": "#00a82b",
        "graph-color-5": "#e6d200", "graph-color-6": "#ccffd1",
        "history-unavailable-color": "#333333",
        "energy-grid-consumption-color": G, "energy-grid-return-color": Y,
        "energy-solar-color": Y, "energy-non-fossil-color": "#00a82b",
        "energy-battery-out-color": "#7dff9e", "energy-battery-in-color": "#00b32c",
        "energy-gas-color": "#e6d200", "energy-water-color": "#66ff73",
    }


def theme(lite):
    t = legacy(lite)
    t.update(semantic())
    return t


def dump(name, vars_):
    lines = [f"{name}:"]
    for k, v in vars_.items():
        lines.append(f'  {k}: "{v}"')
    return "\n".join(lines)


import re

# ---- варианты люминофора: перекраска «зелёных» цветов в цвет люминофора ----
def _recolor(r, g, b, tgt):
    if not (g > r + 20 and g > b + 20):        # не зелёный (серые, красные, жёлтые) — оставить
        return r, g, b
    k = g / 255.0                              # яркость
    w = min(r, b) / g if g else 0              # «белёсость» (светло-зелёные → светлые тона)
    out = [k * ((1 - w) * c + w * 1.0) for c in tgt]
    return tuple(max(0, min(255, round(v * 255))) for v in out)

def recolor_value(v, tgt):
    def hexrep(m):
        h = m.group(1)
        r, g, b = int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)
        return "#%02x%02x%02x" % _recolor(r, g, b, tgt)
    v = re.sub(r"#([0-9a-fA-F]{6})\b", hexrep, v)
    def rgbrep(m):
        r, g, b = int(m.group(1)), int(m.group(2)), int(m.group(3))
        return "%d, %d, %d" % _recolor(r, g, b, tgt)
    return re.sub(r"\b(\d{1,3}),\s*(\d{1,3}),\s*(\d{1,3})\b", rgbrep, v)

VGA = ("'Matrix VGA', 'Matrix Mono', 'Courier New', monospace, "
       "'Segoe UI Emoji', 'Apple Color Emoji', 'Noto Color Emoji'")
FONT_KEYS = ("primary-font-family", "ha-font-family-body", "ha-font-family-heading", "ha-font-family-code",
             "paper-font-common-base_-_font-family", "ha-card-header-font-family")
ACTIVE_KEYS = [k for k, v in theme(False).items() if v == Y and k.startswith(("state-", "switch-checked", "paper-item-icon-active",
                                                                               "app-header-selection", "sidebar-selected", "ha-color-focus"))]

def variant(tgt, tint, active=None, track=None, font=None, image_filter="none"):
    t = {k: recolor_value(v, tgt) for k, v in theme(False).items()}
    t["matrix-bg-tint"] = tint
    t["matrix-image-filter"] = image_filter   # перекраска зелёного логотипа в цвет люминофора
    if active:
        for k in ACTIVE_KEYS:
            t[k] = active
        t["switch-checked-track-color"] = track
    if font:
        for k in FONT_KEYS:
            t[k] = font
    return t

def _yellow_to_grey(v):
    """жёлтые/оранжевые цвета → серые той же яркости (для монохромной Paperwhite)"""
    def rep(m):
        h = m.group(1)
        r, g, b = int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)
        if r > 120 and g > 90 and r - b > 80 and abs(r - g) < 90:
            y = round((r + g) / 2)
            return "#%02x%02x%02x" % (y, y, y)
        return "#" + h
    return re.sub(r"#([0-9a-fA-F]{6})\b", rep, v)


def paperwhite():
    t = variant(PAPER_DIM, "1 1 1", active="#ffffff", track="#6e6e6e", font=VGA,
                image_filter="grayscale(1) brightness(1.2)")
    t = {k: _yellow_to_grey(v) for k, v in t.items()}
    t.update({
        # акценты и выделение — белым
        "ha-card-header-color": "#e6ecff", "accent-color": "#ffffff", "primary-color": "#e6ecff",
        "app-header-selection-bar-color": "#ffffff", "sidebar-selected-text-color": "#ffffff",
        "sidebar-selected-icon-color": "#ffffff", "ha-color-focus": "#ffffff",
        # шкалы: низко — тёмно-серый, середина — серый, высоко — белый
        "success-color": "#5a5a5a", "warning-color": "#a8a8a8", "error-color": "#ffffff",
        "info-color": "#8c8c8c", "gauge-color": "#ffffff",
        # графики и энергия — оттенки серого от белого к тёмному
        "graph-color-1": "#ffffff", "graph-color-2": "#a8a8a8", "graph-color-3": "#d4d4d4",
        "graph-color-4": "#7a7a7a", "graph-color-5": "#bdbdbd", "graph-color-6": "#5a5a5a",
        "energy-grid-consumption-color": "#ffffff", "energy-grid-return-color": "#a8a8a8",
        "energy-solar-color": "#d4d4d4", "energy-non-fossil-color": "#7a7a7a",
        "energy-battery-out-color": "#bdbdbd", "energy-battery-in-color": "#8c8c8c",
        "energy-gas-color": "#a8a8a8", "energy-water-color": "#d4d4d4",
        # нейтрально-чёрные карточки (без зеленоватого оттенка базовой темы)
        "card-background-color": "rgba(8, 8, 8, 0.87)", "rgb-card-background-color": "8, 8, 8",
        "ha-card-background": "repeating-linear-gradient(0deg, rgba(0,0,0,0.22) 0px, rgba(0,0,0,0.22) 1px, "
                              "transparent 1px, transparent 3px), rgba(8, 8, 8, 0.87)",
        "secondary-background-color": "#080808", "ha-dialog-surface-background": "#080808",
        "mdc-theme-surface": "#080808", "material-background-color": "#080808",
        "material-secondary-background-color": "#101010", "table-header-background-color": "#0c0c0c",
        "ha-color-surface-low": "#080808", "ha-color-surface-lower": "#101010",
        "table-row-background-color": "rgba(16, 16, 16, 0.6)",
        "table-row-alternative-background-color": "rgba(32, 32, 32, 0.6)",
        # неактивное «гаснет»: темнее обычного текста (иерархия яркости: активное > текст > неактивное)
        "state-inactive-color": "#6e6e6e", "state-off-color": "#6e6e6e",
        "state-binary_sensor-inactive-color": "#6e6e6e", "switch-unchecked-button-color": "#6e6e6e",
        "switch-unchecked-track-color": "#3a3a3a", "state-unavailable-color": "#4a4a4a",
        # подсветка кода без жёлтого
        "codemirror-keyword": "#ffffff", "codemirror-type": "#ffffff", "codemirror-builtin": "#ffffff",
    })
    return t


def _invert_luma(v):
    """светлая тема из тёмной монохромной: яркость каждого цвета инвертируется в нейтральный серый;
    насыщенные цвета (красный для ошибок) не трогаются"""
    def conv(r, g, b):
        if max(r, g, b) - min(r, g, b) > 90:
            return r, g, b
        y = 255 - round(0.299 * r + 0.587 * g + 0.114 * b)
        return y, y, y
    def hexrep(m):
        h = m.group(1)
        return "#%02x%02x%02x" % conv(int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16))
    v = re.sub(r"#([0-9a-fA-F]{6})\b", hexrep, v)
    def rgbrep(m):
        return "%d, %d, %d" % conv(int(m.group(1)), int(m.group(2)), int(m.group(3)))
    return re.sub(r"\b(\d{1,3}),\s*(\d{1,3}),\s*(\d{1,3})\b", rgbrep, v)


def paperblack():
    """Paperblack — тёмная монохромная (белый люминофор на чёрном), двойные рамки со свечением, как в Green/Amber"""
    return paperwhite()


def paperwhite_light():
    """Paperwhite — светлая монохромная: белый фон, тёмный текст, без рамок и свечения"""
    t = {k: _invert_luma(v) for k, v in paperwhite().items()}
    t.update({
        "lovelace-background":
            "repeating-linear-gradient(0deg, rgba(0,0,0,0.05) 0px, rgba(0,0,0,0.05) 1px, transparent 1px, transparent 3px) fixed, "
            "radial-gradient(ellipse at center, rgba(0,0,0,0) 60%, rgba(0,0,0,0.10) 100%) fixed, "
            "var(--matrix-bg-img, linear-gradient(#fff, #fff)) center / cover no-repeat fixed, #ffffff",
        "primary-background-color": "#ffffff",
        "card-background-color": "rgba(255, 255, 255, 0.87)", "ha-card-background": "rgba(255, 255, 255, 0.87)",
        "rgb-card-background-color": "255, 255, 255",
        # чёрная двойная рамка (рамка карточки + белый зазор + вторая линия), без свечения
        "ha-card-border-width": "1px", "ha-card-border-color": "#000000",
        "ha-card-box-shadow": "0 0 0 3px #ffffff, 0 0 0 4px #000000",
        "matrix-glow": "none", "matrix-title-bg": "#ffffff", "matrix-title-shadow": "none",
        # узор фона: светлый (едва заметные серые разводы на белом)
        "matrix-bg-tint": "1 1 1", "matrix-bg-mode": "light",
        "matrix-image-filter": "grayscale(1) brightness(0)",   # логотип — чёрный
        "mdc-dialog-scrim-color": "rgba(0, 0, 0, 0.35)",
        "ha-color-black": "#000000", "ha-color-white": "#ffffff",
        "text-primary-color": "#ffffff",                       # текст на тёмных (чёрных) кнопках
        "mdc-theme-on-primary": "#ffffff", "mdc-theme-on-secondary": "#ffffff",
    })
    return t


AMBER = (1.0, 0.69, 0.0)          # P3, #ffb000
PAPER_DIM = (0.70, 0.73, 0.80)    # приглушённый бело-голубой для обычного текста (#b3bacc), активное — чистый белый
AMBER_DIM = (0.78, 0.54, 0.0)     # приглушённый янтарь для обычного текста (#c78900), чтобы активное выделялось яркостью
PAPER = (0.875, 0.91, 1.0)        # P4, бело-голубой

header = """# Темы «Monochrome» для Home Assistant (сгенерировано скриптом gen_theme.py, 2026-10-04)
# Стиль старых монохромных мониторов. Иерархия: цвет люминофора — текст и данные; активное выделяется
# (в Green — жёлтым, в Amber — ярким оранжевым, в Paper* — максимальной яркостью/контрастом); неактивное — серым.
# Monochrome Green — зелёный люминофор P1; Monochrome Amber — янтарный P3;
# Monochrome Paperblack — белый люминофор P4 на чёрном, двойные рамки;
# Monochrome Paperwhite — светлая: тёмный текст на белом, чёрные двойные рамки.
# Шрифт во всех темах — IBM VGA 8x16.
# Эффекты: строки развёртки, виньетка, двойная рамка, свечение текста, заставка, живой узор фона —
# через переменные matrix-* и модуль /local/matrix/matrix-bg.js (frontend: extra_module_url).
# Шрифты: «Matrix Mono» — JetBrains Mono (OFL); «Matrix VGA» — PxPlus IBM VGA 8x16
# (Ultimate Oldschool PC Font Pack, VileR / int10h.org, CC BY-SA 4.0).
"""
themes = {
    "Monochrome Green": theme(False),
    "Monochrome Amber": variant(AMBER_DIM, "1 0.69 0", active="#ffa200", track="#8a5a00",
                                image_filter="hue-rotate(-95deg) saturate(1.4) brightness(0.85)"),
    "Monochrome Paperblack": paperblack(),
    "Monochrome Paperwhite": paperwhite_light(),
}
out = header + "\n" + "\n\n".join(dump(n, v) for n, v in themes.items()) + "\n"
# публикуемые имена: переменные monochrome-*, шрифты «Monochrome VGA» / «Monochrome Mono»
out = (out.replace("matrix-", "monochrome-").replace("'Matrix VGA'", "'Monochrome VGA'")
          .replace("'Matrix Mono'", "'Monochrome Mono'")
          .replace("/local/matrix/monochrome-bg.js (frontend: extra_module_url)", "monochrome-effects.js из интеграции monochrome")
          .replace("«Matrix Mono»", "«Monochrome Mono»").replace("«Matrix VGA»", "«Monochrome VGA»"))
import os
dst = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "custom_components", "monochrome", "themes", "monochrome.yaml")
open(dst, "w").write(out)
print({n: len(v) for n, v in themes.items()}, "| bytes:", len(out))
