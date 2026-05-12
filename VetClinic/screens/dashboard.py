import tkinter as tk
from tkinter import ttk
import threading
import screens.darkMode_Style as t
from queries.pet_queries import get_all_pets
from queries.owner_queries import get_all_owners
from queries.clinic_queries import get_all_clinics
from queries.vet_queries import get_all_vets
from queries.visit_queries import get_all_visits
from queries.vaccine_queries import get_all_vaccines
from queries.vaccination_queries import get_all_vaccination_records


class DashboardScreen(tk.Frame):
    def __init__(self, parent, navigate=None):
        super().__init__(parent, bg=t.BG_SECONDARY)
        self._navigate = navigate
        self._build()
        threading.Thread(target=self._fetch_all, daemon=True).start()

    def _build(self):
        outer = tk.Frame(self, bg=t.BG_SECONDARY)
        outer.pack(fill="both", expand=True, padx=30, pady=24)

        tk.Label(outer, text="Dashboard", bg=t.BG_SECONDARY, fg=t.TEXT_PRIMARY,
                 font=t.FONT_TITLE, anchor="w").pack(anchor="w")
        tk.Label(outer, text="Welcome to VetCare Wellness Portal", bg=t.BG_SECONDARY,
                 fg=t.TEXT_MUTED, font=t.FONT_SMALL, anchor="w").pack(anchor="w", pady=(2, 20))

        self._build_stat_cards(outer)
        self._build_bottom_section(outer)

    def _fetch_all(self):
        try:
            pets = len(get_all_pets())
            owners = len(get_all_owners())
            clinics = len(get_all_clinics())
            vets = len(get_all_vets())
            visits = list(get_all_visits())
            vaccines = len(get_all_vaccines())
            records = list(get_all_vaccination_records())
        except Exception:
            pets = owners = clinics = vets = vaccines = 0
            visits = []
            records = []

        self.after(0, lambda: self._populate(pets, owners, clinics, vets, visits, vaccines, records))

    def _populate(self, pets, owners, clinics, vets, visits, vaccines, records):
        stats = [
            ("PETS", pets, "🐾"),
            ("OWNERS", owners, "👥"),
            ("CLINICS", clinics, "🏢"),
            ("VETS", vets, "⚕️"),
            ("VISITS", len(visits), "📅"),
            ("VACCINES", vaccines, "🧪"),
        ]
        for i, (label, value, icon) in enumerate(stats):
            self._stat_values[i].config(text=str(value))

        upcoming = sorted(visits, key=lambda x: x[1])[:5]
        self._fill_visits(upcoming)

        reminders = sorted(records, key=lambda x: x[3] if x[3] else "")[:5]
        self._fill_reminders(reminders)

    def _build_stat_cards(self, parent):
        stats = [
            ("PETS", "—", "🐾"),
            ("OWNERS", "—", "👥"),
            ("CLINICS", "—", "🏢"),
            ("VETS", "—", "⚕️"),
            ("VISITS", "—", "📅"),
            ("VACCINES", "—", "🧪"),
        ]

        self._stat_values = []
        cards_frame = tk.Frame(parent, bg=t.BG_SECONDARY)
        cards_frame.pack(fill="x", pady=(0, 20))

        for label, value, icon in stats:
            card = tk.Frame(cards_frame, bg=t.BG_CARD, highlightbackground=t.BORDER, highlightthickness=1)
            card.pack(side="left", expand=True, fill="both", padx=(0, 10), ipadx=10, ipady=14)

            top = tk.Frame(card, bg=t.BG_CARD)
            top.pack(fill="x", padx=14, pady=(14, 6))

            tk.Label(top, text=label, bg=t.BG_CARD, fg=t.TEXT_MUTED,
                     font=t.FONT_LABEL, anchor="w").pack(side="left")

            icon_frame = tk.Frame(top, bg=t.BG_PRIMARY, width=36, height=36)
            icon_frame.pack(side="right")
            icon_frame.pack_propagate(False)
            tk.Label(icon_frame, text=icon, bg=t.BG_PRIMARY, fg=t.ACCENT_CYAN,
                     font=("Segoe UI", 14)).place(relx=0.5, rely=0.5, anchor="center")

            val_lbl = tk.Label(card, text=value, bg=t.BG_CARD, fg=t.TEXT_PRIMARY,
                               font=("Segoe UI", 26, "bold"), anchor="w")
            val_lbl.pack(anchor="w", padx=14, pady=(0, 14))
            self._stat_values.append(val_lbl)

    def _build_bottom_section(self, parent):
        bottom = tk.Frame(parent, bg=t.BG_SECONDARY)
        bottom.pack(fill="both", expand=True)

        self._build_upcoming_visits(bottom)
        self._build_booster_reminders(bottom)

    def _build_upcoming_visits(self, parent):
        card = tk.Frame(parent, bg=t.BG_CARD, highlightbackground=t.BORDER, highlightthickness=1)
        card.pack(side="left", fill="both", expand=True, padx=(0, 10))

        header = tk.Frame(card, bg=t.BG_CARD)
        header.pack(fill="x", padx=16, pady=(16, 10))
        tk.Label(header, text="Upcoming Visits", bg=t.BG_CARD, fg=t.TEXT_PRIMARY,
                 font=t.FONT_HEADER, anchor="w").pack(side="left")
        tk.Button(header, text="View all", bg=t.BG_CARD, fg=t.ACCENT_CYAN, font=("Segoe UI", 11),
                  relief="flat", borderwidth=0, cursor="hand2",
                  activebackground=t.BG_CARD, activeforeground=t.ACCENT_CYAN,
                  command=lambda: self._navigate(5) if self._navigate else None).pack(side="right")

        self._visits_frame = tk.Frame(card, bg=t.BG_CARD)
        self._visits_frame.pack(fill="both", expand=True)

        self._visits_placeholder = tk.Label(self._visits_frame, text="Loading...",
                                            bg=t.BG_CARD, fg=t.TEXT_MUTED, font=t.FONT_SMALL)
        self._visits_placeholder.pack(pady=20)

    def _fill_visits(self, upcoming):
        for w in self._visits_frame.winfo_children():
            w.destroy()

        if not upcoming:
            tk.Label(self._visits_frame, text="No upcoming visits",
                     bg=t.BG_CARD, fg=t.TEXT_MUTED, font=t.FONT_SMALL).pack(pady=20)
            return

        for visit in upcoming:
            visit_id, visit_date, reason, pet_id, pet_name, vet_id, vet_name, clinic_id, clinic_name = visit
            row = tk.Frame(self._visits_frame, bg=t.BG_CARD)
            row.pack(fill="x", padx=16, pady=6)
            tk.Frame(self._visits_frame, bg=t.BORDER, height=1).pack(fill="x", padx=16)

            left = tk.Frame(row, bg=t.BG_CARD)
            left.pack(side="left", fill="x", expand=True)
            tk.Label(left, text=pet_name, bg=t.BG_CARD, fg=t.TEXT_PRIMARY,
                     font=t.FONT_NORMAL, anchor="w").pack(anchor="w")
            tk.Label(left, text=f"{clinic_name} · {vet_name}", bg=t.BG_CARD,
                     fg=t.TEXT_MUTED, font=t.FONT_SMALL, anchor="w").pack(anchor="w")

            date_str = visit_date.strftime("%b %d") if hasattr(visit_date, "strftime") else str(visit_date)[:10]
            tk.Label(row, text=date_str, bg=t.BG_CARD, fg=t.TEXT_PRIMARY,
                     font=("Segoe UI", 12, "bold")).pack(side="right")

    def _build_booster_reminders(self, parent):
        card = tk.Frame(parent, bg=t.BG_CARD, highlightbackground=t.BORDER, highlightthickness=1)
        card.pack(side="left", fill="both", expand=True)

        header = tk.Frame(card, bg=t.BG_CARD)
        header.pack(fill="x", padx=16, pady=(16, 10))

        title_frame = tk.Frame(header, bg=t.BG_CARD)
        title_frame.pack(side="left")
        tk.Label(title_frame, text="⚠", bg=t.BG_CARD, fg=t.ACCENT_PURPLE,
                 font=("Segoe UI", 13)).pack(side="left", padx=(0, 6))
        tk.Label(title_frame, text="Booster Reminders", bg=t.BG_CARD,
                 fg=t.TEXT_PRIMARY, font=t.FONT_HEADER).pack(side="left")
        tk.Button(header, text="View all", bg=t.BG_CARD, fg=t.ACCENT_CYAN, font=("Segoe UI", 11),
                  relief="flat", borderwidth=0, cursor="hand2",
                  activebackground=t.BG_CARD, activeforeground=t.ACCENT_CYAN,
                  command=lambda: self._navigate(6) if self._navigate else None).pack(side="right")

        self._reminders_frame = tk.Frame(card, bg=t.BG_CARD)
        self._reminders_frame.pack(fill="both", expand=True)

        self._reminders_placeholder = tk.Label(self._reminders_frame, text="Loading...",
                                               bg=t.BG_CARD, fg=t.TEXT_MUTED, font=t.FONT_SMALL)
        self._reminders_placeholder.pack(pady=20)

    def _fill_reminders(self, reminders):
        for w in self._reminders_frame.winfo_children():
            w.destroy()

        if not reminders:
            tk.Label(self._reminders_frame, text="No booster reminders",
                     bg=t.BG_CARD, fg=t.TEXT_MUTED, font=t.FONT_SMALL).pack(pady=20)
            return

        for rec in reminders:
            record_id, batch_num, vaccine_type, next_booster, vaccine_id, vaccine_name, note_id, vet_name = rec
            row = tk.Frame(self._reminders_frame, bg=t.BG_HOVER,
                           highlightbackground=t.BORDER, highlightthickness=1)
            row.pack(fill="x", padx=16, pady=6, ipady=10)

            left = tk.Frame(row, bg=t.BG_HOVER)
            left.pack(side="left", fill="x", expand=True, padx=10)
            tk.Label(left, text=vaccine_name or "Unknown", bg=t.BG_HOVER,
                     fg=t.TEXT_PRIMARY, font=t.FONT_NORMAL, anchor="w").pack(anchor="w")
            tk.Label(left, text=vaccine_type or "", bg=t.BG_HOVER,
                     fg=t.TEXT_MUTED, font=t.FONT_SMALL, anchor="w").pack(anchor="w")

            date_str = next_booster.strftime("%b %d") if hasattr(next_booster, "strftime") else str(next_booster)[:10]
            tk.Label(row, text=date_str, bg=t.ACCENT_PURPLE, fg=t.TEXT_PRIMARY,
                     font=("Segoe UI", 10, "bold"), padx=10, pady=4).pack(side="right", padx=10)