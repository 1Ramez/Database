# Colors
BG_PRIMARY = "#eaf0f6"
BG_SECONDARY = "#f0f4f8"
BG_CARD = "#ffffff"
BG_HOVER = "#e2eaf2"

ACCENT_CYAN = "#00b4b4"
ACCENT_PURPLE = "#7c3aed"

TEXT_PRIMARY = "#0d1117"
TEXT_MUTED = "#5a6a7a"
TEXT_ACCENT = "#00b4b4"

SUCCESS = "#22c55e"
DANGER = "#ef4444"
WARNING = "#f59e0b"

BORDER = "#d0dce8"
SEPARATOR = "#e8eef4"

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
    "fg": "#ffffff",
    "activebackground": ACCENT_CYAN,
    "activeforeground": "#ffffff",
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
    "fg": "#ffffff",
    "font": FONT_BTN,
    "relief": "flat",
    "borderwidth": 0,
    "cursor": "hand2",
    "padx": 16,
    "pady": 7,
    "activebackground": "#009999",
    "activeforeground": "#ffffff",
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
    "fg": "#ffffff",
    "font": FONT_BTN,
    "relief": "flat",
    "borderwidth": 0,
    "cursor": "hand2",
    "padx": 16,
    "pady": 7,
    "activebackground": "#cc2222",
    "activeforeground": "#ffffff",
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
    "activeforeground": "#009999",
}

BTN_PURPLE = {
    "bg": ACCENT_PURPLE,
    "fg": "#ffffff",
    "font": FONT_BTN,
    "relief": "flat",
    "borderwidth": 0,
    "cursor": "hand2",
    "padx": 12,
    "pady": 5,
    "activebackground": "#6d28d9",
    "activeforeground": "#ffffff",
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
    "foreground": "#ffffff",
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
BADGE_PURPLE = {"bg": ACCENT_PURPLE, "fg": "#ffffff", "font": FONT_SMALL}
BADGE_CYAN = {"bg": ACCENT_CYAN, "fg": "#ffffff", "font": FONT_SMALL}
BADGE_GREEN = {"bg": SUCCESS, "fg": "#ffffff", "font": FONT_SMALL}
BADGE_RED = {"bg": DANGER, "fg": "#ffffff", "font": FONT_SMALL}
BADGE_AMBER = {"bg": WARNING, "fg": "#ffffff", "font": FONT_SMALL}