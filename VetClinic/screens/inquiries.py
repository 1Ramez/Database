import tkinter as tk
from tkinter import ttk
import threading
import screens.darkMode_Style as t
from queries.inquiry_queries import (
    inquiry_1_most_visited_species,
    inquiry_2_clinics_with_no_visits,
    inquiry_3_vet_most_vaccinations,
    inquiry_4_owners_no_visits,
    inquiry_5_vaccines_per_clinic,
    inquiry_6_pet_visit_count_this_year,
)


class InquiriesScreen(tk.Frame):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, bg=t.BG_SECONDARY, **kwargs)
        self._build_ui()
        threading.Thread(target=self._fetch_all, daemon=True).start()

    def _build_ui(self):
        wrapper = tk.Frame(self, bg=t.BG_SECONDARY)
        wrapper.pack(fill="both", expand=True)

        self.canvas = tk.Canvas(wrapper, bg=t.BG_SECONDARY, highlightthickness=0)
        sb = tk.Scrollbar(wrapper, orient="vertical", command=self.canvas.yview,
                          bg=t.BG_CARD, troughcolor=t.BG_SECONDARY, relief="flat", width=8)
        self.canvas.configure(yscrollcommand=sb.set)

        sb.pack(side="right", fill="y")
        self.canvas.pack(side="left", fill="both", expand=True)

        self.inner = tk.Frame(self.canvas, bg=t.BG_SECONDARY)
        self._win = self.canvas.create_window((0, 0), window=self.inner, anchor="nw")

        self.inner.bind("<Configure>",
                        lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        self.canvas.bind("<Configure>",
                         lambda e: self.canvas.itemconfig(self._win, width=e.width))
        self.canvas.bind("<Enter>", lambda e: self.canvas.bind_all("<MouseWheel>", self._on_scroll))
        self.canvas.bind("<Leave>", lambda e: self.canvas.unbind_all("<MouseWheel>"))

        outer = tk.Frame(self.inner, bg=t.BG_SECONDARY)
        outer.pack(fill="both", expand=True, padx=30, pady=24)

        tk.Label(outer, text="Reports & Inquiries", bg=t.BG_SECONDARY, fg=t.TEXT_PRIMARY,
                 font=t.FONT_TITLE, anchor="w").pack(anchor="w")
        tk.Label(outer, text="Analytics and insights about your veterinary network",
                 bg=t.BG_SECONDARY, fg=t.TEXT_MUTED, font=t.FONT_SMALL, anchor="w").pack(anchor="w", pady=(2, 20))

        self.grid_frame = tk.Frame(outer, bg=t.BG_SECONDARY)
        self.grid_frame.pack(fill="both", expand=True)

        self.grid_frame.columnconfigure(0, weight=1)
        self.grid_frame.columnconfigure(1, weight=1)

        self._cards = {}
        layout = [
            ("species_chart",   0, 0),
            ("no_visits_clinic",1, 0),
            ("top_vet",         0, 1),
            ("no_visits_owners",1, 1),
            ("vaccines_clinic", 0, 2),
            ("pet_visits_year", 1, 2),
        ]
        for key, col, row in layout:
            card = tk.Frame(self.grid_frame, bg=t.BG_CARD,
                            highlightbackground=t.BORDER, highlightthickness=1)
            card.grid(row=row, column=col, padx=8, pady=8, sticky="nsew")
            self._cards[key] = card

    def _on_scroll(self, event):
        self.canvas.yview_scroll(-1 * (event.delta // 120), "units")

    def _fetch_all(self):
        results = {}
        funcs = {
            "q1": inquiry_1_most_visited_species,
            "q2": inquiry_2_clinics_with_no_visits,
            "q3": inquiry_3_vet_most_vaccinations,
            "q4": inquiry_4_owners_no_visits,
            "q5": inquiry_5_vaccines_per_clinic,
            "q6": inquiry_6_pet_visit_count_this_year,
        }
        for key, fn in funcs.items():
            try:
                results[key] = fn()
            except Exception:
                results[key] = None
        self.after(0, lambda: self._populate(results))

    def _populate(self, r):
        self._build_species_chart(r.get("q1"), r.get("q6"))
        self._build_no_visits_clinic(r.get("q2"))
        self._build_top_vet(r.get("q3"))
        self._build_no_visits_owners(r.get("q4"))
        self._build_vaccines_clinic(r.get("q5"))
        self._build_pet_visits_year(r.get("q6"))

    def _card_header(self, card, title):
        tk.Label(card, text=title, bg=t.BG_CARD, fg=t.TEXT_PRIMARY,
                 font=t.FONT_HEADER, anchor="w").pack(fill="x", padx=16, pady=(16, 10))
        tk.Frame(card, bg=t.BORDER, height=1).pack(fill="x", padx=16)

    def _build_species_chart(self, q1, q6):
        card = self._cards["species_chart"]
        self._card_header(card, "Visits by Species (Last Month)")

        if not q6:
            tk.Label(card, text="No data", bg=t.BG_CARD, fg=t.TEXT_MUTED,
                     font=t.FONT_SMALL).pack(pady=20)
            return

        species_counts = {}
        for _, name, specie, count in q6:
            if specie:
                species_counts[specie] = species_counts.get(specie, 0) + count

        if not species_counts:
            tk.Label(card, text="No data", bg=t.BG_CARD, fg=t.TEXT_MUTED,
                     font=t.FONT_SMALL).pack(pady=20)
            return

        chart_frame = tk.Frame(card, bg=t.BG_CARD)
        chart_frame.pack(fill="x", padx=16, pady=12)

        canvas_h = 200
        canvas_w = 400
        c = tk.Canvas(chart_frame, bg=t.BG_CARD, height=canvas_h,
                      width=canvas_w, highlightthickness=0)
        c.pack(fill="x")

        max_val = max(species_counts.values()) if species_counts else 1
        pad_l, pad_r, pad_t, pad_b = 40, 20, 20, 40
        n = len(species_counts)
        bar_w = min(80, (canvas_w - pad_l - pad_r) // max(n, 1) - 10)
        slot_w = (canvas_w - pad_l - pad_r) // max(n, 1)
        chart_h = canvas_h - pad_t - pad_b

        for i in range(5):
            y_val = max_val * i / 4
            y_px = canvas_h - pad_b - (chart_h * i / 4)
            c.create_line(pad_l, y_px, canvas_w - pad_r, y_px,
                          fill="#1e2d40", dash=(4, 4))
            c.create_text(pad_l - 6, y_px, text=f"{y_val:.1f}",
                          fill=t.TEXT_MUTED, font=("Segoe UI", 9), anchor="e")

        for idx, (specie, count) in enumerate(species_counts.items()):
            x_center = pad_l + idx * slot_w + slot_w // 2
            bar_h = int(chart_h * count / max_val) if max_val else 0
            x0 = x_center - bar_w // 2
            x1 = x_center + bar_w // 2
            y0 = canvas_h - pad_b - bar_h
            y1 = canvas_h - pad_b
            c.create_rectangle(x0, y0, x1, y1, fill=t.ACCENT_CYAN, outline="")
            c.create_text(x_center, canvas_h - pad_b + 12, text=specie,
                          fill=t.TEXT_MUTED, font=("Segoe UI", 10), anchor="n")

    def _build_no_visits_clinic(self, q2):
        card = self._cards["no_visits_clinic"]
        self._card_header(card, "Clinics with No Visits (Last Month)")

        if not q2:
            tk.Label(card, text="All clinics had visits", bg=t.BG_CARD,
                     fg=t.TEXT_MUTED, font=t.FONT_SMALL).pack(pady=20)
            return

        for clinic_id, name, location in q2:
            row = tk.Frame(card, bg=t.BG_CARD)
            row.pack(fill="x", padx=16, pady=8)
            tk.Label(row, text=name, bg=t.BG_CARD, fg=t.TEXT_PRIMARY,
                     font=t.FONT_NORMAL, anchor="w").pack(side="left")
            tk.Label(row, text="No visits", bg=t.BG_CARD, fg=t.TEXT_MUTED,
                     font=("Segoe UI", 12, "bold"), anchor="e").pack(side="right")
            tk.Frame(card, bg=t.BORDER, height=1).pack(fill="x", padx=16)

        tk.Frame(card, bg=t.BG_CARD, height=10).pack()

    def _build_top_vet(self, q3):
        card = self._cards["top_vet"]
        self._card_header(card, "Top Vaccinating Vet (Last Month)")

        if not q3:
            tk.Label(card, text="No data", bg=t.BG_CARD, fg=t.TEXT_MUTED,
                     font=t.FONT_SMALL).pack(pady=20)
            return

        vet_id, vet_name, vac_count = q3

        inner = tk.Frame(card, bg=t.BG_HOVER,
                         highlightbackground=t.BORDER, highlightthickness=1)
        inner.pack(fill="x", padx=16, pady=12, ipady=10)

        icon_frame = tk.Frame(inner, bg="#0f3030", width=46, height=46)
        icon_frame.pack(side="left", padx=(12, 10))
        icon_frame.pack_propagate(False)
        tk.Label(icon_frame, text="🏆", bg="#0f3030",
                 font=("Segoe UI", 20)).place(relx=0.5, rely=0.5, anchor="center")

        text_frame = tk.Frame(inner, bg=t.BG_HOVER)
        text_frame.pack(side="left", fill="x", expand=True)
        tk.Label(text_frame, text=vet_name, bg=t.BG_HOVER, fg=t.TEXT_PRIMARY,
                 font=("Segoe UI", 13, "bold"), anchor="w").pack(anchor="w")
        tk.Label(text_frame, text=f"{vac_count} vaccinations administered",
                 bg=t.BG_HOVER, fg=t.TEXT_MUTED, font=t.FONT_SMALL, anchor="w").pack(anchor="w")

        tk.Frame(card, bg=t.BG_CARD, height=10).pack()

    def _build_no_visits_owners(self, q4):
        card = self._cards["no_visits_owners"]
        self._card_header(card, "Owners with No Visits (Last Month)")

        if not q4:
            tk.Label(card, text="All owners had visits", bg=t.BG_CARD,
                     fg=t.TEXT_MUTED, font=t.FONT_SMALL).pack(pady=20)
            return

        list_frame = tk.Frame(card, bg=t.BG_CARD)
        list_frame.pack(fill="both", expand=True, padx=16)

        for owner_id, name, phone, emergency in q4:
            row = tk.Frame(list_frame, bg=t.BG_CARD)
            row.pack(fill="x", pady=8)
            tk.Label(row, text=name, bg=t.BG_CARD, fg=t.TEXT_PRIMARY,
                     font=t.FONT_NORMAL, anchor="w").pack(side="left")
            tk.Label(row, text=phone or "—", bg=t.BG_CARD, fg=t.TEXT_MUTED,
                     font=t.FONT_NORMAL, anchor="e").pack(side="right")
            tk.Frame(list_frame, bg=t.BORDER, height=1).pack(fill="x")

        tk.Frame(card, bg=t.BG_CARD, height=10).pack()

    def _build_vaccines_clinic(self, q5):
        card = self._cards["vaccines_clinic"]
        self._card_header(card, "Vaccines by Clinic (Last Month)")

        if not q5:
            tk.Label(card, text="No data", bg=t.BG_CARD, fg=t.TEXT_MUTED,
                     font=t.FONT_SMALL).pack(pady=20)
            return

        clinics = {}
        for clinic_name, vaccine_name, times in q5:
            clinics.setdefault(clinic_name, []).append(vaccine_name)

        content = tk.Frame(card, bg=t.BG_CARD)
        content.pack(fill="x", padx=16, pady=10)

        for clinic_name, vaccines in clinics.items():
            tk.Label(content, text=clinic_name, bg=t.BG_CARD, fg=t.TEXT_PRIMARY,
                     font=("Segoe UI", 12, "bold"), anchor="w").pack(anchor="w", pady=(8, 4))
            badge_row = tk.Frame(content, bg=t.BG_CARD)
            badge_row.pack(anchor="w", pady=(0, 4))
            for v in vaccines:
                tk.Label(badge_row, text=v, bg=t.BG_HOVER, fg=t.TEXT_PRIMARY,
                         font=("Segoe UI", 10), padx=10, pady=4,
                         relief="flat").pack(side="left", padx=(0, 6))

        tk.Frame(card, bg=t.BG_CARD, height=10).pack()

    def _build_pet_visits_year(self, q6):
        card = self._cards["pet_visits_year"]
        self._card_header(card, "Pet Visits This Year")

        if not q6:
            tk.Label(card, text="No data", bg=t.BG_CARD, fg=t.TEXT_MUTED,
                     font=t.FONT_SMALL).pack(pady=20)
            return

        list_wrap = tk.Frame(card, bg=t.BG_CARD, highlightbackground=t.BORDER, highlightthickness=1)
        list_wrap.pack(fill="both", expand=True, padx=16, pady=8)

        scroll_canvas = tk.Canvas(list_wrap, bg=t.BG_CARD, highlightthickness=0, height=220)
        vsb = tk.Scrollbar(list_wrap, orient="vertical", command=scroll_canvas.yview,
                           width=6, relief="flat", bg=t.BG_CARD, troughcolor=t.BG_SECONDARY)
        scroll_canvas.configure(yscrollcommand=vsb.set)

        vsb.pack(side="right", fill="y")
        scroll_canvas.pack(side="left", fill="both", expand=True)

        inner = tk.Frame(scroll_canvas, bg=t.BG_CARD)
        scroll_canvas.create_window((0, 0), window=inner, anchor="nw")
        inner.bind("<Configure>",
                   lambda e: scroll_canvas.configure(scrollregion=scroll_canvas.bbox("all")))

        for pet_id, name, specie, count in q6:
            row = tk.Frame(inner, bg=t.BG_CARD)
            row.pack(fill="x", pady=6)
            tk.Label(row, text=name, bg=t.BG_CARD, fg=t.TEXT_PRIMARY,
                     font=t.FONT_NORMAL, anchor="w").pack(side="left")
            label = f"{count} visit{'s' if count != 1 else ''}"
            tk.Label(row, text=label, bg=t.ACCENT_CYAN, fg=t.BG_PRIMARY,
                     font=("Segoe UI", 10, "bold"),
                     padx=10, pady=3).pack(side="right")

        tk.Frame(card, bg=t.BG_CARD, height=10).pack()