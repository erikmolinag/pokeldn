import flet as ft
import flet.canvas as cv

from gui.icons import icon as pixel_icon

# poke-app: the pause menu of a modern Pokemon game. A vivid orange and purple backdrop split on a slant,
# translucent dark-violet panels with white text over it, and the orange-red of the menu as the one accent.
ORANGE = "#FF6A1F"
ORANGE_DEEP = "#FF4E2A"
VIOLET = "#7B2FF7"
VIOLET_DEEP = "#5A1FD1"
NIGHT = "#1B0E4A"             # the solid tone behind popups and dialogs
BG = VIOLET_DEEP
PANEL = ft.Colors.with_opacity(0.58, "#140A3A")
CARD = ft.Colors.with_opacity(0.10, "#FFFFFF")
FIELD = ft.Colors.with_opacity(0.14, "#FFFFFF")
HOVER = ft.Colors.with_opacity(0.20, "#FFFFFF")
OUTLINE = ft.Colors.with_opacity(0.20, "#FFFFFF")
BORDER = ft.Colors.with_opacity(0.24, "#FFFFFF")
EDGE = ft.Colors.with_opacity(0.32, "#FFFFFF")
DIVIDER = ft.Colors.with_opacity(0.16, "#FFFFFF")
TEXT = "#FFFFFF"
SOFT = "#F0EBFF"
MUTED = "#CDC2F2"
FAINT = "#A496D6"
ACCENT = ORANGE_DEEP          # the menu's highlight
BLUE = ACCENT                 # upstream's name for the accent: selection, focus, the filled button
INFO = "#62CBFF"              # running and in-progress states
RED = "#FF7A7A"               # errors and Stop, readable on violet
GREEN = "#3DFFA0"
AMBER = "#FFC54D"
INK = "#FFFFFF"               # text on the accent
HIGHLIGHT = "#FFFFFF"         # the selected menu entry: white, with violet text
HIGHLIGHT_TEXT = "#2A1470"
SHADOW = ft.BoxShadow(blur_radius=30, spread_radius=0, offset=ft.Offset(0, 10),
                      color=ft.Colors.with_opacity(0.28, "#0B0420"))
SELECTED = ft.Colors.with_opacity(0.18, "#FFFFFF")
FONT = "Rubik"
MONO = "monospace"
CONTROL_HEIGHT = 36
CONTROL_PADDING = ft.Padding(14, 8, 14, 8)
CONTROL_RADIUS = 12
GAP = 14
SIDEBAR_WIDTH = 254
SESSION_WIDTH = 360


def tint(alpha: float, color: str = TEXT) -> str:
    """A see-through layer of `color`: hovers and hairlines over the violet panels."""
    return ft.Colors.with_opacity(alpha, color)


def app_theme() -> ft.Theme:
    return ft.Theme(
        color_scheme_seed=VIOLET,
        font_family=FONT,
        color_scheme=ft.ColorScheme(primary=ACCENT, on_primary=INK, secondary=INFO, surface=NIGHT,
                                    on_surface=TEXT, error=RED, outline=BORDER,
                                    surface_container_highest=NIGHT, on_surface_variant=MUTED),
        divider_color=DIVIDER,
        card_theme=ft.CardTheme(margin=0),
        scrollbar_theme=ft.ScrollbarTheme(thickness=6, radius=3, thumb_color=tint(0.30)),
        tooltip_theme=ft.TooltipTheme(decoration=ft.BoxDecoration(bgcolor=NIGHT, border_radius=10),
                                      text_style=ft.TextStyle(color=TEXT, size=12)),
    )


def text(value: str, size: float = 13, color: str = TEXT, weight=None, **kwargs) -> ft.Text:
    kwargs.setdefault("style", ft.TextStyle(height=1.4))
    return ft.Text(value, size=size, color=color, weight=weight, **kwargs)


def backdrop(content: ft.Control) -> ft.Container:
    """The window behind everything: orange and violet split on a slant, soft stripes, a faint Poke Ball
    ring in the corner, like a modern game's pause menu."""
    return ft.Container(ft.Stack([
        ft.Container(left=0, top=0, right=0, bottom=0,
                     image=ft.DecorationImage(src="stripes.png", repeat=ft.ImageRepeat.REPEAT, scale=1.6,
                                              alignment=ft.Alignment.TOP_LEFT)),
        ft.Container(ft.Image(src="ring.svg", width=820, height=820, opacity=0.09), right=-210, bottom=-260),
        ft.Container(content, left=0, top=0, right=0, bottom=0),
    ], expand=True), expand=True, bgcolor=BG,
        gradient=ft.LinearGradient(begin=ft.Alignment(-1, -0.6), end=ft.Alignment(1, 0.6),
                                   colors=[ORANGE, ORANGE_DEEP, VIOLET, VIOLET_DEEP],
                                   stops=[0.0, 0.37, 0.371, 1.0]))


def glass(content: ft.Control, radius: float = 26, **kwargs) -> ft.Container:
    """A translucent dark-violet panel floating over the backdrop: cards, tools and the session sit on these."""
    return ft.Container(content, bgcolor=PANEL, border_radius=radius, clip_behavior=ft.ClipBehavior.ANTI_ALIAS,
                        border=ft.Border.all(2, OUTLINE), shadow=SHADOW, blur=ft.Blur(8, 8), **kwargs)


def surface(content: ft.Control, *, bgcolor: str = CARD, radius: float = 18, **kwargs) -> ft.Container:
    """A solid surface in the content layer."""
    return ft.Container(content, bgcolor=bgcolor, border_radius=radius, **kwargs)


def panel(content: ft.Control, width: float | None = None, expand=None, padding=0) -> ft.Container:
    return glass(ft.Container(content, padding=padding), width=width, expand=expand)


TOOLBAR_ITEM = 32   # the icon buttons are this size
TOOLBAR_INSET = 4


def notch(*controls: ft.Control) -> ft.Row:
    """A small glass toolbar centred over the content; its groups are split by hairlines.
    Its corners are concentric with its items': outer radius = item radius + the even inset."""
    items: list[ft.Control] = []
    for control in controls:
        if items:
            items.append(ft.Container(width=1, height=18, bgcolor=tint(0.10)))
        items.append(control)
    row = ft.Row(items, spacing=8, tight=True, vertical_alignment=ft.CrossAxisAlignment.CENTER)
    return ft.Row([glass(ft.Container(row, padding=TOOLBAR_INSET), radius=TOOLBAR_ITEM / 2 + TOOLBAR_INSET)],
                  alignment=ft.MainAxisAlignment.CENTER)


def panel_header(title: str, *actions: ft.Control) -> ft.Container:
    return ft.Container(
        ft.Row([text(title, 17, weight=ft.FontWeight.W_800), ft.Row(list(actions), spacing=2)],
               alignment=ft.MainAxisAlignment.SPACE_BETWEEN, vertical_alignment=ft.CrossAxisAlignment.CENTER),
        padding=ft.Padding(18, 14, 12, 6), height=52)


def section(title: str, body: ft.Control | None = None, trailing: ft.Control | None = None) -> ft.Column:
    """A titled group inside a glass panel: the spacing separates it, no box."""
    head: list[ft.Control] = [text(title, 12, MUTED, weight=ft.FontWeight.W_700, expand=True)]
    if trailing:
        head.append(trailing)
    return ft.Column([ft.Row(head, spacing=8), *([body] if body else [])], spacing=8, tight=True)


def grid_rows(tiles: list[ft.Control], columns: int = 2, spacing: float = 6) -> list[ft.Control]:
    """Tiles in rows of `columns`; the tiles of a row share its tallest tile's height."""
    rows = []
    for i in range(0, len(tiles), columns):
        cells = tiles[i:i + columns]
        for cell in cells:
            cell.expand = 1
        cells += [ft.Container(expand=1) for _ in range(columns - len(cells))]
        rows.append(ft.Row(cells, spacing=spacing, intrinsic_height=True,
                           vertical_alignment=ft.CrossAxisAlignment.STRETCH))
    return rows


def grid(tiles: list[ft.Control], columns: int = 2, spacing: float = 6) -> ft.Column:
    return ft.Column(grid_rows(tiles, columns, spacing), spacing=spacing, tight=True)


def card(title: str, body: ft.Control | None = None, description: str = "",
         trailing: ft.Control | None = None, tip: str = "") -> ft.Container:
    head = [text(title, 14, weight=ft.FontWeight.W_800, expand=True)]
    if tip:
        head.append(pixel_icon("circle-info", color=FAINT, tooltip=tip))
    if trailing:
        head.append(trailing)
    rows: list[ft.Control] = [ft.Row(head, spacing=8, vertical_alignment=ft.CrossAxisAlignment.CENTER)]
    if description:
        rows.append(text(description, 12, MUTED))
    if body:
        rows.append(body)
    # A dark translucent card: it reads the same over the orange and the violet halves of the backdrop.
    return surface(ft.Container(ft.Column(rows, spacing=10, tight=True), padding=18), bgcolor=PANEL,
                   border=ft.Border.all(2, OUTLINE), radius=22)


def dialog(**kwargs) -> ft.AlertDialog:
    return ft.AlertDialog(bgcolor=NIGHT, elevation=24,
                          shape=ft.RoundedRectangleBorder(radius=26, side=ft.BorderSide(2, OUTLINE)),
                          barrier_color=ft.Colors.with_opacity(0.55, "#0B0420"), **kwargs)


def _border() -> dict:
    flat = ft.OutlineInputBorder(border_radius=CONTROL_RADIUS, side=ft.BorderSide(1, ft.Colors.TRANSPARENT))
    return {ft.ControlState.FOCUSED: ft.OutlineInputBorder(border_radius=CONTROL_RADIUS,
                                                           side=ft.BorderSide(1.5, ACCENT)),
            ft.ControlState.DISABLED: flat, ft.ControlState.DEFAULT: flat}


class _Field(ft.TextField):
    def before_update(self):
        super().before_update()
        details = self.error or self.helper or self.counter
        self.height = None if details else CONTROL_HEIGHT
        self.fit_parent_size = not bool(details)


def field(label: str = "", value: str = "", hint: str = "", mono: bool = False, digits: bool = False,
          limit: int = 0, **kwargs) -> ft.TextField:
    """`digits` takes 0-9 only; `limit` caps the length. Both are one regex over the whole value:
    Flet's max_length squeezes a fixed-height field into wrapping, and its filter refuses a whole edit."""
    if digits or limit:
        count = f"{{0,{limit}}}" if limit else "*"
        kwargs.setdefault("input_filter", ft.InputFilter(f"^{'[0-9]' if digits else '.'}{count}$"))
    if digits:
        kwargs.setdefault("keyboard_type", ft.KeyboardType.NUMBER)
    style = ft.TextStyle(size=13, color=TEXT, font_family=MONO if mono else None)
    uniform = not kwargs.get("multiline") and not label and "height" not in kwargs
    if uniform:
        kwargs.setdefault("height", CONTROL_HEIGHT)
        kwargs.setdefault("fit_parent_size", True)
    kwargs.setdefault("size_constraints", ft.BoxConstraints(min_height=CONTROL_HEIGHT))
    kwargs.setdefault("content_padding", CONTROL_PADDING)
    control = _Field if uniform else ft.TextField
    return control(value=value, label=label or None, hint_text=hint or None, text_style=style,
                   label_style=ft.TextStyle(size=12, color=MUTED), dense=True,
                   hint_style=ft.TextStyle(size=13, color=FAINT), bgcolor=FIELD, filled=True,
                   border=_border(), cursor_color=ACCENT,
                   text_vertical_align=ft.VerticalAlignment.CENTER, **kwargs)


def dropdown(options: list[tuple[str, str]], value: str | None, on_select=None, **kwargs) -> ft.Dropdown:
    return ft.Dropdown(value=value, options=[ft.DropdownOption(key=k, text=t) for k, t in options],
                       on_select=on_select, dense=True, filled=True, bgcolor=FIELD, border=_border(),
                       text_size=13, expand=True, height=CONTROL_HEIGHT, content_padding=CONTROL_PADDING,
                       trailing_icon=pixel_icon("chevron-down", color=MUTED),
                       selected_trailing_icon=pixel_icon("chevron-up", color=ACCENT),
                       menu_style=ft.MenuStyle(bgcolor=NIGHT, shape=ft.RoundedRectangleBorder(radius=14)),
                       **kwargs)


def labeled_control(label: str, control: ft.Control, **kwargs) -> ft.Column:
    return ft.Column([ft.Container(text(label, 11, MUTED), height=16,
                                   alignment=ft.Alignment.CENTER_LEFT), control],
                     spacing=4, tight=True, **kwargs)


class _Button(ft.Button):
    def before_update(self):
        super().before_update()
        if isinstance(self.icon, (ft.Image, ft.Icon)):   # the icon takes the label's colour by hand
            colors = self.style.color
            self.icon.color = colors[ft.ControlState.DISABLED if self.disabled else ft.ControlState.DEFAULT]


def button(label: str, on_click=None, icon=None, color: str = ACCENT, filled: bool = True,
           **kwargs) -> ft.Button:
    """A capsule. Filled carries the colour and is the one likely action in a view; the rest are not filled."""
    ink = INK if filled else TEXT
    style = ft.ButtonStyle(
        bgcolor={ft.ControlState.DISABLED: tint(0.06),
                 ft.ControlState.DEFAULT: color if filled else tint(0.06)},
        color={ft.ControlState.DISABLED: FAINT, ft.ControlState.DEFAULT: ink},
        shape=ft.StadiumBorder(), padding=ft.Padding(18, 8, 18, 8),
        side={ft.ControlState.FOCUSED: ft.BorderSide(2, ft.Colors.with_opacity(0.5, ACCENT)),
              ft.ControlState.DEFAULT: ft.BorderSide(0, ft.Colors.TRANSPARENT)},
        text_style=ft.TextStyle(size=13, weight=ft.FontWeight.W_800, font_family=FONT),
        overlay_color={ft.ControlState.DEFAULT: ft.Colors.TRANSPARENT,
                       ft.ControlState.HOVERED: ft.Colors.with_opacity(0.10, "#FFFFFF" if filled else TEXT),
                       ft.ControlState.PRESSED: ft.Colors.with_opacity(0.12, "#000000")},
        elevation=0, shadow_color=ft.Colors.TRANSPARENT)
    kwargs.setdefault("height", CONTROL_HEIGHT)
    return _Button(label, icon=pixel_icon(icon, color=ink) if icon else None, on_click=on_click,
                   style=style, elevation=0, **kwargs)


def secondary_button(label: str, on_click=None, icon=None, **kwargs) -> ft.Button:
    return button(label, on_click, icon, filled=False, **kwargs)


def link_button(label: str, on_click=None) -> ft.TextButton:
    return ft.TextButton(label, on_click=on_click, height=CONTROL_HEIGHT,
                         style=ft.ButtonStyle(color=ACCENT, padding=ft.Padding(10, 6, 10, 6),
                                              shape=ft.StadiumBorder(),
                                              text_style=ft.TextStyle(weight=ft.FontWeight.W_700, font_family=FONT),
                                              overlay_color=ft.Colors.with_opacity(0.08, ACCENT)))


def icon_button(icon, on_click=None, tooltip: str = "", color: str = MUTED, **kwargs) -> ft.IconButton:
    return ft.IconButton(pixel_icon(icon, color=color), tooltip=tooltip or None,
                         on_click=on_click, width=34, height=34,
                         style=ft.ButtonStyle(shape=ft.CircleBorder(), overlay_color=tint(0.06)),
                         **kwargs)


def switch(value: bool, on_change) -> ft.Switch:
    return ft.Switch(value=value, height=CONTROL_HEIGHT, padding=0,
                     active_color="#FFFFFF", active_track_color=ACCENT,
                     inactive_thumb_color="#FFFFFF", inactive_track_color=tint(0.28),
                     track_outline_color={ft.ControlState.DEFAULT: ft.Colors.TRANSPARENT},
                     overlay_color={ft.ControlState.DEFAULT: ft.Colors.TRANSPARENT,
                                    ft.ControlState.HOVERED: ft.Colors.TRANSPARENT,
                                    ft.ControlState.PRESSED: ft.Colors.TRANSPARENT,
                                    ft.ControlState.FOCUSED: ft.Colors.with_opacity(0.18, ACCENT)},
                     splash_radius=16,
                     on_change=on_change)


def badge(label: str, color: str = MUTED, icon: str = "circle-info") -> ft.Row:
    return ft.Row([pixel_icon(icon, size=12, color=color), text(label, 12, SOFT)],
                  spacing=6, tight=True, vertical_alignment=ft.CrossAxisAlignment.CENTER)


def segmented(options: list[tuple[str, str, str]], value: str, on_change, wrap: bool = False) -> ft.Row:
    """The capsule switcher (Basic / Advanced); it sits on the glass toolbar. `wrap` lets a long one break
    onto a second line: each capsule is then sized by its padding, since a centred one fills the line."""
    row = ft.Row(spacing=0, tight=True, wrap=wrap, run_spacing=4)
    size = ({"padding": ft.Padding(12, 8, 14, 8)} if wrap else
            {"height": TOOLBAR_ITEM, "padding": ft.Padding(12, 0, 14, 0), "alignment": ft.Alignment.CENTER})

    def render(selected):
        row.controls = [
            ft.Container(ft.Row([
                pixel_icon(icon, color=ACCENT if key == selected else FAINT),
                text(label, 12, TEXT if key == selected else MUTED, weight=ft.FontWeight.W_800),
            ], spacing=6, tight=True), border_radius=TOOLBAR_ITEM / 2, **size,
                bgcolor=SELECTED if key == selected else None,
                on_click=lambda e, k=key: pick(k))
            for key, label, icon in options]

    def pick(key):
        render(key)
        row.update()
        on_change(key)

    render(value)
    return row


def fade(scrollable: ft.ScrollableControl, size: float = 24) -> ft.ShaderMask:
    """The scrollable, its top and bottom edges fading out over size px while content lies beyond them."""
    edges = {"height": 0.0, "top": False, "bottom": not getattr(scrollable, "auto_scroll", False)}
    mask = ft.ShaderMask(content=scrollable, blend_mode=ft.BlendMode.DST_IN, expand=scrollable.expand,
                         shader=ft.LinearGradient(colors=["#FFFFFFFF", "#FFFFFFFF"]))

    def paint() -> bool:
        stop = min(size / edges["height"], 0.5) if edges["height"] else 0.0
        clear, solid = "#00FFFFFF", "#FFFFFFFF"
        shader = ft.LinearGradient(begin=ft.Alignment.TOP_CENTER, end=ft.Alignment.BOTTOM_CENTER,
                                   colors=[clear if edges["top"] else solid, solid, solid,
                                           clear if edges["bottom"] else solid],
                                   stops=[0, stop, 1 - stop, 1])
        changed = shader != mask.shader
        mask.shader = shader
        return changed

    def resized(e) -> None:
        edges["height"] = e.height
        if paint():
            mask.update()

    previous = scrollable.on_scroll

    def scrolled(e) -> None:
        top, bottom = e.pixels > e.min_scroll_extent + 1, e.pixels < e.max_scroll_extent - 1
        if (top, bottom) != (edges["top"], edges["bottom"]):
            edges["top"], edges["bottom"] = top, bottom
            if paint():
                mask.update()
        if previous:
            previous(e)

    scrollable.on_scroll = scrolled
    mask.on_size_change = resized
    paint()
    return mask


def step_list(steps: list[str]) -> ft.Column:
    rows = []
    for index, step in enumerate(steps):
        first, last = index == 0, index == len(steps) - 1
        lead = 22 if first else 0
        gap = 0 if last else 14

        def resize(e, initial=first, final=last, top=lead, bottom=gap):
            center = top + (e.height - top - bottom) / 2
            stroke = ft.Paint(color=MUTED, stroke_width=1, style=ft.PaintingStyle.STROKE)
            shapes = [cv.Circle(9, center, 4,
                                paint=ft.Paint(color=MUTED, stroke_width=1.5, style=ft.PaintingStyle.STROKE))]
            if initial:
                end = center - 7
                shapes.append(cv.Line(9, 0, 9, end, paint=ft.Paint(
                    stroke_width=1, style=ft.PaintingStyle.STROKE,
                    gradient=ft.PaintLinearGradient(begin=ft.Offset(9, 0), end=ft.Offset(9, end),
                                                   colors=[ft.Colors.with_opacity(0, MUTED), MUTED]))))
            ranges = ([] if initial else [(0, center - 7)])
            if not final:
                ranges.append((center + 7, e.height))
            for start, end in ranges:
                y = start
                while y < end:
                    shapes.append(cv.Line(9, y, 9, min(y + 3, end), paint=stroke))
                    y += 7
            e.control.shapes = shapes
            e.control.update()

        rows.append(ft.Row([
            cv.Canvas([], width=18, on_resize=resize),
            ft.Container(text(step, 13), expand=True, padding=ft.Padding(0, lead, 0, gap)),
        ], spacing=10, intrinsic_height=True, vertical_alignment=ft.CrossAxisAlignment.STRETCH))
    return ft.Column(rows, spacing=0, tight=True)
