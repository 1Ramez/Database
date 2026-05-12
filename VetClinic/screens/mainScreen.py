import tkinter as tk
from tkinter import ttk
import importlib
import screens.darkMode_Style as _dark
import screens.lightMode_Style as _light
import screens.darkMode_Style as theme

from screens.dashboard import DashboardScreen
from screens.owners import OwnersScreen
from screens.pets import PetsScreen
from screens.clinics import ClinicsScreen
from screens.vets import VetsScreen
from screens.visits import VisitsScreen
from screens.vaccinations import VaccinationsScreen
from screens.vaccines import VaccinesScreen
from screens.workat import WorkatScreen
from screens.clinical_notes import ClinicalNotesScreen
from screens.inquiries import InquiriesScreen

NAV_ITEMS = [
    ("Dashboard", "🏠", DashboardScreen),
    ("Owners", "👤", OwnersScreen),
    ("Pets", "🐾", PetsScreen),
    ("Clinics", "🏥", ClinicsScreen),
    ("Veterinarians","⚕️", VetsScreen),
    ("Visits", "📅", VisitsScreen),
    ("Vaccinations", "💉", VaccinationsScreen),
    ("Vaccines", "🧪", VaccinesScreen),
    ("Works At", "🔗", WorkatScreen),
    ("Clinical Notes","📝", ClinicalNotesScreen),
    ("Reports", "📊", InquiriesScreen),
]


class VetCareApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("VetCare Wellness Portal")
        self.state("zoomed")
        self.attributes("-fullscreen", False)
        self._is_dark = True
        self._current_index = 0
        self.current_screen = None
        self.nav_buttons = []
        self.sidebar_collapsed = False
        _dark._active = None
        self.configure(bg=_dark.BG_PRIMARY)
        self._build_ui()
        self._show_screen(0)

    def _t(self):
        return _dark if self._is_dark else _light

    def _build_ui(self):
        t = self._t()

        self.sidebar = tk.Frame(self, bg=t.BG_PRIMARY, width=t.SIDEBAR_WIDTH)
        self.sidebar.pack(side="left", fill="y")
        self.sidebar.pack_propagate(False)

        self.logo_frame = tk.Frame(self.sidebar, bg=t.BG_PRIMARY)
        self.logo_frame.pack(fill="x", padx=16, pady=(20, 10))

        tk.Label(self.logo_frame, text="🐾", bg=t.ACCENT_CYAN, font=("Segoe UI", 18),
                 width=2, relief="flat").pack(side="left", padx=(0, 10))

        logo_text_frame = tk.Frame(self.logo_frame, bg=t.BG_PRIMARY)
        logo_text_frame.pack(side="left")
        tk.Label(logo_text_frame, text="VetCare", bg=t.BG_PRIMARY, fg=t.TEXT_PRIMARY,
                 font=t.FONT_LOGO).pack(anchor="w")
        tk.Label(logo_text_frame, text="Wellness Portal", bg=t.BG_PRIMARY, fg=t.TEXT_MUTED,
                 font=t.FONT_SMALL).pack(anchor="w")

        tk.Frame(self.sidebar, bg=t.BORDER, height=1).pack(fill="x", padx=16, pady=(10, 6))

        self.collapse_btn = tk.Button(
            self.sidebar, text="〈",
            bg=t.BG_PRIMARY, fg=t.TEXT_MUTED,
            font=("Segoe UI", 14), relief="flat", borderwidth=0,
            cursor="hand2", activebackground=t.BG_PRIMARY,
            activeforeground=t.ACCENT_CYAN,
            command=self._toggle_sidebar
        )
        self.collapse_btn.pack(side="bottom", pady=(0, 16))

        tk.Frame(self.sidebar, bg=t.BORDER, height=1).pack(
            fill="x", padx=16, pady=(10, 3), side="bottom")

        self.theme_btn = tk.Button(
            self.sidebar,
            text="🌙 Dark Mode" if self._is_dark else "☀ Light Mode",
            bg=t.BG_PRIMARY, fg=t.TEXT_MUTED,
            font=t.FONT_NAV, anchor="w", padx=20, pady=4,
            relief="flat", borderwidth=0, cursor="hand2",
            activebackground=t.BG_HOVER, activeforeground=t.TEXT_PRIMARY,
            command=self._toggle_theme
        )
        self.theme_btn.pack(side="bottom", fill="x", padx=8, pady=(0, 4))

        self.nav_frame = tk.Frame(self.sidebar, bg=t.BG_PRIMARY)
        self.nav_frame.pack(fill="x", pady=(0, 20))

        for i, (label, icon, _) in enumerate(NAV_ITEMS):
            btn = tk.Button(
                self.nav_frame,
                text=f"  {icon}  {label}",
                **t.NAV_ITEM_STYLE,
                command=lambda idx=i: self._show_screen(idx)
            )
            btn.pack(fill="x", padx=8, pady=0.5)
            self.nav_buttons.append(btn)

        self.content_frame = tk.Frame(self, bg=t.BG_SECONDARY)
        self.content_frame.pack(side="left", fill="both", expand=True)

    def _toggle_theme(self):
        self._is_dark = not self._is_dark
        if self._is_dark:
            _dark._active = None
        else:
            _dark._active = _light
        self._rebuild_ui()

    def _rebuild_ui(self):
        t = self._t()
        self.configure(bg=t.BG_PRIMARY)

        for widget in self.winfo_children():
            widget.destroy()

        self.nav_buttons = []
        self.sidebar_collapsed = False
        self.current_screen = None
        self._build_ui()
        self._show_screen(self._current_index)

    def _toggle_sidebar(self):
        t = self._t()
        if self.sidebar_collapsed:
            self.sidebar.configure(width=t.SIDEBAR_WIDTH)
            self.collapse_btn.configure(text="〈")
            self.sidebar_collapsed = False
        else:
            self.sidebar.configure(width=50)
            self.collapse_btn.configure(text="〉")
            self.sidebar_collapsed = True

    def _show_screen(self, index):
        t = self._t()
        self._current_index = index
        for i, btn in enumerate(self.nav_buttons):
            btn.configure(**(t.NAV_ITEM_ACTIVE_STYLE if i == index else t.NAV_ITEM_STYLE))
        if self.current_screen:
            self.current_screen.destroy()
        screen_class = NAV_ITEMS[index][2]
        if screen_class == DashboardScreen:
            self.current_screen = DashboardScreen(self.content_frame, navigate=self._show_screen)
        else:
            self.current_screen = screen_class(self.content_frame)
        self.current_screen.pack(fill="both", expand=True)