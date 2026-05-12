import sys as _sys

# Colors
BG_PRIMARY = "#0d1117"
BG_SECONDARY = "#111827"
BG_CARD = "#1a2233"
BG_HOVER = "#1f2d42"

ACCENT_CYAN = "#00d4d4"
ACCENT_PURPLE = "#7c3aed"

TEXT_PRIMARY = "#ffffff"
TEXT_MUTED = "#8892a4"
TEXT_ACCENT = "#00d4d4"

SUCCESS = "#22c55e"
DANGER = "#ef4444"
WARNING = "#f59e0b"

BORDER = "#1e2d40"
SEPARATOR = "#1a2233"

# Fonts
FONT_TITLE = ("Segoe UI", 22, "bold")
FONT_HEADER = ("Segoe UI", 16, "bold")
FONT_NORMAL = ("Segoe UI", 13)
FONT_SMALL = ("Segoe UI", 11)
FONT_LABEL = ("Segoe UI", 10, "bold")
FONT_NAV = ("Segoe UI", 13)
FONT_BTN = ("Segoe UI", 12, "bold")
FONT_LOGO = ("Segoe UI", 15, "bold")

# Window
WINDOW_STYLE = {
    "bg": BG_PRIMARY,
}

# Sidebar
SIDEBAR_BG = BG_PRIMARY
SIDEBAR_WIDTH = 210

NAV_ITEM_STYLE = {
    "bg": BG_PRIMARY,
    "fg": TEXT_MUTED,
    "font": FONT_NAV,
    "anchor": "w",
    "padx": 20,
    "pady": 0.5,
    "relief": "flat",
    "borderwidth": 0,
    "cursor": "hand2",
    "activebackground": BG_HOVER,
    "activeforeground": TEXT_PRIMARY,
}

NAV_ITEM_ACTIVE_STYLE = {
    **NAV_ITEM_STYLE,
    "bg": ACCENT_CYAN,
    "fg": BG_PRIMARY,
    "activebackground": ACCENT_CYAN,
    "activeforeground": BG_PRIMARY,
    "font": ("Segoe UI", 13, "bold"),
}

# Content Area
CONTENT_BG = BG_SECONDARY

PAGE_TITLE_STYLE = {
    "bg": BG_SECONDARY,
    "fg": TEXT_PRIMARY,
    "font": FONT_TITLE,
}

PAGE_SUBTITLE_STYLE = {
    "bg": BG_SECONDARY,
    "fg": TEXT_MUTED,
    "font": FONT_SMALL,
}

SECTION_HEADER_STYLE = {
    "bg": BG_CARD,
    "fg": TEXT_PRIMARY,
    "font": FONT_HEADER,
}

# Dashboard
STAT_CARD_BG = BG_CARD
STAT_CARD_BORDER = BORDER

STAT_LABEL_STYLE = {
    "bg": BG_CARD,
    "fg": TEXT_MUTED,
    "font": FONT_LABEL,
}

STAT_VALUE_STYLE = {
    "bg": BG_CARD,
    "fg": TEXT_PRIMARY,
    "font": ("Segoe UI", 26, "bold"),
}

# Cards
CARD_STYLE = {
    "bg": BG_CARD,
    "relief": "flat",
    "borderwidth": 0,
    "highlightbackground": BORDER,
    "highlightthickness": 1,
}

# Labels
LABEL_STYLE = {
    "bg": BG_SECONDARY,
    "fg": TEXT_PRIMARY,
    "font": FONT_NORMAL,
}

LABEL_MUTED_STYLE = {
    "bg": BG_SECONDARY,
    "fg": TEXT_MUTED,
    "font": FONT_SMALL,
}

LABEL_ON_CARD = {
    "bg": BG_CARD,
    "fg": TEXT_PRIMARY,
    "font": FONT_NORMAL,
}

LABEL_MUTED_ON_CARD = {
    "bg": BG_CARD,
    "fg": TEXT_MUTED,
    "font": FONT_SMALL,
}

# Input fields
ENTRY_STYLE = {
    "bg": BG_CARD,
    "fg": TEXT_PRIMARY,
    "insertbackground": ACCENT_CYAN,
    "font": FONT_NORMAL,
    "relief": "flat",
    "highlightbackground": BORDER,
    "highlightthickness": 1,
}

# Buttons
BTN_PRIMARY = {
    "bg": ACCENT_CYAN,
    "fg": BG_PRIMARY,
    "font": FONT_BTN,
    "relief": "flat",
    "borderwidth": 0,
    "cursor": "hand2",
    "padx": 16,
    "pady": 7,
    "activebackground": "#00bcbc",
    "activeforeground": BG_PRIMARY,
}

BTN_SECONDARY = {
    "bg": BG_CARD,
    "fg": TEXT_PRIMARY,
    "font": FONT_BTN,
    "relief": "flat",
    "borderwidth": 0,
    "cursor": "hand2",
    "padx": 16,
    "pady": 7,
    "activebackground": BG_HOVER,
    "activeforeground": TEXT_PRIMARY,
}

BTN_DANGER = {
    "bg": DANGER,
    "fg": TEXT_PRIMARY,
    "font": FONT_BTN,
    "relief": "flat",
    "borderwidth": 0,
    "cursor": "hand2",
    "padx": 16,
    "pady": 7,
    "activebackground": "#cc2222",
    "activeforeground": TEXT_PRIMARY,
}

BTN_LINK = {
    "bg": BG_SECONDARY,
    "fg": TEXT_ACCENT,
    "font": ("Segoe UI", 12),
    "relief": "flat",
    "borderwidth": 0,
    "cursor": "hand2",
    "padx": 0,
    "pady": 0,
    "activebackground": BG_SECONDARY,
    "activeforeground": "#00bcbc",
}

BTN_PURPLE = {
    "bg": ACCENT_PURPLE,
    "fg": TEXT_PRIMARY,
    "font": FONT_BTN,
    "relief": "flat",
    "borderwidth": 0,
    "cursor": "hand2",
    "padx": 12,
    "pady": 5,
    "activebackground": "#6d28d9",
    "activeforeground": TEXT_PRIMARY,
}

# Tables
TREEVIEW_STYLE = {
    "background": BG_CARD,
    "foreground": TEXT_PRIMARY,
    "fieldbackground": BG_CARD,
    "rowheight": 36,
    "font": FONT_NORMAL,
}

TREEVIEW_HEADING_STYLE = {
    "background": BG_PRIMARY,
    "foreground": TEXT_MUTED,
    "font": FONT_LABEL,
    "relief": "flat",
}

TREEVIEW_SELECTED = {
    "background": ACCENT_CYAN,
    "foreground": BG_PRIMARY,
}

# Dropdown
COMBO_STYLE = {
    "background": BG_CARD,
    "foreground": TEXT_PRIMARY,
    "font": FONT_NORMAL,
}

# Scrollbar
SCROLLBAR_STYLE = {
    "bg": BG_CARD,
    "troughcolor": BG_PRIMARY,
    "relief": "flat",
    "width": 8,
}

# Badge
BADGE_PURPLE = {"bg": ACCENT_PURPLE, "fg": TEXT_PRIMARY, "font": FONT_SMALL}
BADGE_CYAN = {"bg": ACCENT_CYAN, "fg": BG_PRIMARY, "font": FONT_SMALL}
BADGE_GREEN = {"bg": SUCCESS, "fg": BG_PRIMARY, "font": FONT_SMALL}
BADGE_RED = {"bg": DANGER, "fg": TEXT_PRIMARY, "font": FONT_SMALL}
BADGE_AMBER = {"bg": WARNING, "fg": BG_PRIMARY, "font": FONT_SMALL}


_active = None


class _Proxy(_sys.modules[__name__].__class__):
    def __getattribute__(self, name):
        active = super().__getattribute__("_active")
        if active is not None and not name.startswith("_"):
            try:
                return getattr(active, name)
            except AttributeError:
                pass
        return super().__getattribute__(name)


_sys.modules[__name__].__class__ = _Proxy