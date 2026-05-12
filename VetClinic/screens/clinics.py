import tkinter as tk
from tkinter import messagebox
import threading
import screens.darkMode_Style as t
from queries.clinic_queries import get_all_clinics, insert_clinic, update_clinic, delete_clinic

AVATAR_COLORS = [
    ("#00d4d4", "#0d1117"),
    ("#7c3aed", "#ffffff"),
    ("#ef4444", "#ffffff"),
    ("#f59e0b", "#0d1117"),
    ("#22c55e", "#0d1117"),
    ("#3b82f6", "#ffffff"),
    ("#ec4899", "#ffffff"),
]

def _avatar_colors(index):
    return AVATAR_COLORS[index % len(AVATAR_COLORS)]


class ClinicCard(tk.Frame):
    CARD_W = 260
    CARD_H = 200

    def __init__(self, parent, clinic_data, color_index, on_edit=None, on_delete=None, **kwargs):
        super().__init__(parent, bg=t.BG_CARD, highlightbackground=t.BORDER,
                         highlightthickness=1, relief="flat",
                         width=self.CARD_W, height=self.CARD_H, **kwargs)
        self.pack_propagate(False)

        clinic_id, name, location, emergency_facilities = clinic_data
        av_bg, av_fg = _avatar_colors(color_index)

        top = tk.Frame(self, bg=t.BG_CARD)
        top.pack(fill="x", padx=14, pady=(14, 0))

        tk.Label(top, text="🏥", bg=av_bg, fg=av_fg,
                 font=("Segoe UI", 14), width=3, relief="flat").pack(side="left")

        btn_frame = tk.Frame(top, bg=t.BG_CARD)
        btn_frame.pack(side="right")

        tk.Button(btn_frame, text="✏", bg=t.BG_CARD, fg=t.TEXT_MUTED,
                  font=("Segoe UI", 13), relief="flat", borderwidth=0,
                  cursor="hand2", activebackground=t.BG_HOVER, activeforeground=t.TEXT_PRIMARY,
                  command=lambda: on_edit(clinic_id) if on_edit else None).pack(side="left", padx=(0, 4))

        tk.Button(btn_frame, text="🗑", bg=t.BG_CARD, fg=t.DANGER,
                  font=("Segoe UI", 13), relief="flat", borderwidth=0,
                  cursor="hand2", activebackground=t.BG_HOVER, activeforeground=t.DANGER,
                  command=lambda: on_delete(clinic_id) if on_delete else None).pack(side="left")

        tk.Label(self, text=name, bg=t.BG_CARD, fg=t.TEXT_PRIMARY,
                 font=("Segoe UI", 13, "bold"), anchor="w").pack(fill="x", padx=14, pady=(10, 4))

        has_emergency = str(emergency_facilities).strip().lower() in ("yes", "1", "true", "y")
        if has_emergency:
            badge_frame = tk.Frame(self, bg=t.BG_CARD)
            badge_frame.pack(fill="x", padx=14, pady=(0, 6))
            tk.Label(badge_frame, text="🛡 Emergency", bg=t.DANGER, fg=t.TEXT_PRIMARY,
                     font=("Segoe UI", 10, "bold"), padx=8, pady=2,
                     relief="flat").pack(side="left")

        info = tk.Frame(self, bg=t.BG_CARD)
        info.pack(fill="x", padx=14)

        for icon, value in [("📍", location or "—")]:
            row = tk.Frame(info, bg=t.BG_CARD)
            row.pack(fill="x", pady=1)
            tk.Label(row, text=icon, bg=t.BG_CARD, fg=t.TEXT_MUTED, font=t.FONT_SMALL).pack(side="left")
            tk.Label(row, text=f"  {value}", bg=t.BG_CARD, fg=t.TEXT_MUTED,
                     font=t.FONT_SMALL, anchor="w").pack(side="left")

        self.bind("<Enter>", lambda e: self.config(highlightbackground=t.ACCENT_CYAN))
        self.bind("<Leave>", lambda e: self.config(highlightbackground=t.BORDER))


class ClinicFormDialog(tk.Toplevel):
    def __init__(self, parent, title="Add Clinic", clinic_data=None, on_save=None):
        super().__init__(parent)
        self.title(title)
        self.configure(bg=t.BG_CARD)
        self.resizable(False, False)
        self.on_save = on_save

        w, h = 450, 380
        self.update_idletasks()
        x = (self.winfo_screenwidth() - w) // 2
        y = (self.winfo_screenheight() - h) // 2
        self.geometry(f"{w}x{h}+{x}+{y}")
        self.grab_set()

        header_frame = tk.Frame(self, bg=t.BG_CARD)
        header_frame.pack(fill="x", padx=24, pady=(16, 8))

        tk.Label(header_frame, text=title, bg=t.BG_CARD, fg=t.TEXT_PRIMARY,
                 font=("Segoe UI", 18, "bold")).pack(side="left")

        tk.Button(header_frame, text="✕", bg=t.BG_CARD, fg=t.TEXT_MUTED, font=("Segoe UI", 12),
                  bd=0, cursor="hand2", command=self.destroy,
                  activebackground=t.BG_CARD, activeforeground=t.TEXT_PRIMARY).pack(side="right")

        form = tk.Frame(self, bg=t.BG_CARD)
        form.pack(fill="both", expand=True, padx=24)

        self.vars = {}
        self._entries = {}

        self._field(form, "Clinic Name *", "name")
        self._field(form, "Location", "location")
        self._field(form, "Emergency Facilities (yes/no)", "emergency_facilities")

        if clinic_data:
            clinic_id, name, location, emergency_facilities = clinic_data
            self.vars["name"].set(name or "")
            self.vars["location"].set(location or "")
            self.vars["emergency_facilities"].set(str(emergency_facilities) if emergency_facilities else "")

        btn_row = tk.Frame(self, bg=t.BG_CARD)
        btn_row.pack(fill="x", padx=24, pady=12)

        tk.Button(btn_row, text="Cancel", **t.BTN_SECONDARY,
                  width=10, command=self.destroy).pack(side="right", padx=(8, 0))

        tk.Button(btn_row, text=title, **t.BTN_PRIMARY,
                  width=12, command=self._submit).pack(side="right")

    def _field(self, parent, label, key):
        tk.Label(parent, text=label, bg=t.BG_CARD, fg=t.TEXT_PRIMARY,
                 font=("Segoe UI", 11, "bold"), anchor="w").pack(fill="x", pady=(6, 3))

        var = tk.StringVar()
        entry = tk.Entry(parent, textvariable=var, **t.ENTRY_STYLE)
        entry.pack(fill="x", ipady=6)
        self.vars[key] = var
        entry.bind("<FocusIn>", lambda e: e.widget.config(highlightbackground=t.ACCENT_CYAN))
        entry.bind("<FocusOut>", lambda e: e.widget.config(highlightbackground=t.BORDER))
        self._entries[key] = entry

    def _submit(self):
        data = {k: v.get().strip() for k, v in self.vars.items()}

        if not data.get("name"):
            messagebox.showwarning("Missing", "Clinic Name is required.", parent=self)
            return

        if self.on_save:
            self.on_save(data)
        self.destroy()


class ClinicsScreen(tk.Frame):
    COLUMNS = 3
    CARD_PAD = 16

    def __init__(self, parent, **kwargs):
        super().__init__(parent, bg=t.BG_SECONDARY, **kwargs)
        self._all_clinics = []
        self._build_ui()
        self._load_clinics()

    def _build_ui(self):
        header = tk.Frame(self, bg=t.BG_SECONDARY)
        header.pack(fill="x", padx=36, pady=(28, 0))

        left = tk.Frame(header, bg=t.BG_SECONDARY)
        left.pack(side="left")

        tk.Label(left, text="Clinics", **t.PAGE_TITLE_STYLE).pack(anchor="w")
        self.subtitle_lbl = tk.Label(left, text="Loading...", **t.PAGE_SUBTITLE_STYLE)
        self.subtitle_lbl.pack(anchor="w")

        tk.Button(header, text="  + Add Clinic  ", **t.BTN_PRIMARY,
                  command=self._open_add).pack(side="right", pady=4)

        search_wrap = tk.Frame(self, bg=t.BG_CARD, highlightbackground=t.BORDER, highlightthickness=1)
        search_wrap.pack(fill="x", padx=36, pady=(18, 0), ipadx=6, ipady=4)

        tk.Label(search_wrap, text="🔍", bg=t.BG_CARD, fg=t.TEXT_MUTED,
                 font=t.FONT_NORMAL).pack(side="left", padx=(10, 4))

        self.search_var = tk.StringVar()
        self.search_var.trace_add("write", lambda *_: self._filter())

        tk.Entry(search_wrap, textvariable=self.search_var, bg=t.BG_CARD, fg=t.TEXT_PRIMARY,
                 insertbackground=t.ACCENT_CYAN, font=t.FONT_NORMAL, relief="flat",
                 highlightthickness=0, borderwidth=0).pack(side="left", fill="x", expand=True, ipady=6)

        wrapper = tk.Frame(self, bg=t.BG_SECONDARY)
        wrapper.pack(fill="both", expand=True, padx=36, pady=18)

        self.canvas = tk.Canvas(wrapper, bg=t.BG_SECONDARY, highlightthickness=0)
        sb = tk.Scrollbar(wrapper, orient="vertical", command=self.canvas.yview,
                          bg=t.BG_CARD, troughcolor=t.BG_SECONDARY, relief="flat", width=8)
        self.canvas.configure(yscrollcommand=sb.set)

        sb.pack(side="right", fill="y")
        self.canvas.pack(side="left", fill="both", expand=True)

        self.cards_frame = tk.Frame(self.canvas, bg=t.BG_SECONDARY)
        self._win = self.canvas.create_window((0, 0), window=self.cards_frame, anchor="nw")

        self.cards_frame.bind("<Configure>",
                              lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        self.canvas.bind("<Configure>",
                         lambda e: self.canvas.itemconfig(self._win, width=e.width))
        self.canvas.bind("<Enter>", lambda e: self.canvas.bind_all("<MouseWheel>", self._on_scroll))
        self.canvas.bind("<Leave>", lambda e: self.canvas.unbind_all("<MouseWheel>"))

    def _on_scroll(self, event):
        self.canvas.yview_scroll(-1 * (event.delta // 120), "units")

    def _load_clinics(self):
        self.subtitle_lbl.config(text="Loading...")
        threading.Thread(target=self._fetch, daemon=True).start()

    def _fetch(self):
        try:
            data = list(get_all_clinics())
            self.after(0, lambda: self._on_loaded(data, None))
        except Exception as exc:
            self.after(0, lambda: self._on_loaded([], exc))

    def _on_loaded(self, data, error):
        if error:
            messagebox.showerror("DB Error", str(error))
        self._all_clinics = data
        self._render(self._all_clinics)

    def _filter(self):
        q = self.search_var.get().lower()
        filtered = [c for c in self._all_clinics
                    if q in str(c[1]).lower()
                    or q in str(c[2]).lower()]
        self._render(filtered)

    def _render(self, clinics):
        for w in self.cards_frame.winfo_children():
            w.destroy()

        n = len(clinics)
        self.subtitle_lbl.config(text=f"{n} clinic{'s' if n != 1 else ''} registered")

        for idx, clinic in enumerate(clinics):
            row, col = divmod(idx, self.COLUMNS)
            ClinicCard(self.cards_frame, clinic_data=clinic, color_index=idx,
                       on_edit=self._open_edit, on_delete=self._confirm_delete
                       ).grid(row=row, column=col, padx=self.CARD_PAD // 2,
                              pady=self.CARD_PAD // 2, sticky="nw")

        for c in range(self.COLUMNS):
            self.cards_frame.columnconfigure(c, weight=1)

    def _open_add(self):
        ClinicFormDialog(self, title="Add Clinic", on_save=self._do_insert)

    def _open_edit(self, clinic_id):
        clinic = next((c for c in self._all_clinics if str(c[0]) == str(clinic_id)), None)
        if not clinic:
            return
        ClinicFormDialog(self, title="Edit Clinic", clinic_data=clinic,
                         on_save=lambda d: self._do_update(clinic_id, d))

    def _confirm_delete(self, clinic_id):
        clinic = next((c for c in self._all_clinics if str(c[0]) == str(clinic_id)), None)
        name = clinic[1] if clinic else clinic_id
        if messagebox.askyesno("Delete Clinic", f"Delete '{name}'? This cannot be undone."):
            try:
                delete_clinic(clinic_id)
                self._load_clinics()
            except Exception as exc:
                messagebox.showerror("Error", str(exc))

    def _do_insert(self, data):
        try:
            insert_clinic(data["name"], data["location"], data["emergency_facilities"])
            self._load_clinics()
        except Exception as exc:
            messagebox.showerror("Error", str(exc))

    def _do_update(self, clinic_id, data):
        try:
            update_clinic(clinic_id, data["name"], data["location"], data["emergency_facilities"])
            self._load_clinics()
        except Exception as exc:
            messagebox.showerror("Error", str(exc))