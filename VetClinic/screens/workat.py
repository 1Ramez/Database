import tkinter as tk
from tkinter import messagebox, ttk
import threading
import screens.darkMode_Style as t
from queries.worksat_queries import get_all_worksat, insert_worksat, delete_worksat
from queries.vet_queries import get_all_vets
from queries.clinic_queries import get_all_clinics


AVATAR_COLORS = [
    ("#00d4d4", t.BG_PRIMARY),
    ("#7c3aed", "#ffffff"),
    ("#ef4444", "#ffffff"),
    ("#f59e0b", t.BG_PRIMARY),
    ("#22c55e", t.BG_PRIMARY),
    ("#3b82f6", "#ffffff"),
    ("#ec4899", "#ffffff"),
]

def _avatar_colors(index):
    bg, fg = AVATAR_COLORS[index % len(AVATAR_COLORS)]
    return bg, fg

def _initials(name: str) -> str:
    parts = name.strip().split()
    if len(parts) >= 2:
        return (parts[0][0] + parts[-1][0]).upper()
    return name[:2].upper() if name else "?"


class WorkatCard(tk.Frame):
    CARD_W = 300
    CARD_H = 200

    def __init__(self, parent, record_data, color_index, on_delete=None, **kwargs):
        super().__init__(parent, bg=t.BG_CARD, highlightbackground=t.BORDER,
                         highlightthickness=1, relief="flat",
                         width=self.CARD_W, height=self.CARD_H, **kwargs)
        self.pack_propagate(False)

        vet_id, vet_name, clinic_id, clinic_name = record_data
        av_bg, av_fg = _avatar_colors(color_index)

        top = tk.Frame(self, bg=t.BG_CARD)
        top.pack(fill="x", padx=14, pady=(14, 0))

        tk.Label(top, text=_initials(vet_name), bg=av_bg, fg=av_fg,
                 font=("Segoe UI", 14, "bold"), width=3, relief="flat").pack(side="left")

        btn_frame = tk.Frame(top, bg=t.BG_CARD)
        btn_frame.pack(side="right")

        tk.Button(btn_frame, text="🗑", bg=t.BG_CARD, fg=t.DANGER,
                  font=("Segoe UI", 13), relief="flat", borderwidth=0,
                  cursor="hand2", activebackground=t.BG_HOVER, activeforeground=t.DANGER,
                  command=lambda: on_delete(vet_id, clinic_id) if on_delete else None).pack(side="left")

        tk.Label(self, text=vet_name, bg=t.BG_CARD, fg=t.TEXT_PRIMARY,
                 font=("Segoe UI", 13, "bold"), anchor="w").pack(fill="x", padx=14, pady=(10, 4))

        info = tk.Frame(self, bg=t.BG_CARD)
        info.pack(fill="x", padx=14)

        for icon, value in [("🏥", clinic_name or "—"), ("🔗", f"Vet ID: {vet_id}  |  Clinic ID: {clinic_id}")]:
            row = tk.Frame(info, bg=t.BG_CARD)
            row.pack(fill="x", pady=1)
            tk.Label(row, text=icon, bg=t.BG_CARD, fg=t.TEXT_MUTED, font=t.FONT_SMALL).pack(side="left")
            tk.Label(row, text=f"  {value}", bg=t.BG_CARD, fg=t.TEXT_MUTED,
                     font=t.FONT_SMALL, anchor="w").pack(side="left")

        self.bind("<Enter>", lambda e: self.config(highlightbackground=t.ACCENT_CYAN))
        self.bind("<Leave>", lambda e: self.config(highlightbackground=t.BORDER))


class WorkatFormDialog(tk.Toplevel):
    def __init__(self, parent, title="Assign Vet to Clinic", on_save=None):
        super().__init__(parent)
        self.title(title)
        self.configure(bg=t.BG_CARD)
        self.resizable(False, False)
        self.on_save = on_save
        self._vets = []
        self._clinics = []

        w, h = 460, 300
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
        self._combos = {}

        self._dropdown(form, "Veterinarian *", "vet_id")
        self._dropdown(form, "Clinic *", "clinic_id")

        self._load_dropdowns()

        btn_row = tk.Frame(self, bg=t.BG_CARD)
        btn_row.pack(fill="x", padx=24, pady=12)

        tk.Button(btn_row, text="Cancel", **t.BTN_SECONDARY,
                  width=10, command=self.destroy).pack(side="right", padx=(8, 0))

        tk.Button(btn_row, text="Assign", **t.BTN_PRIMARY,
                  width=16, command=self._submit).pack(side="right")

    def _dropdown(self, parent, label, key):
        tk.Label(parent, text=label, bg=t.BG_CARD, fg=t.TEXT_PRIMARY,
                 font=("Segoe UI", 11, "bold"), anchor="w").pack(fill="x", pady=(6, 3))

        var = tk.StringVar()
        combo = ttk.Combobox(parent, textvariable=var, state="readonly", font=t.FONT_NORMAL)
        combo.pack(fill="x", ipady=4)
        self.vars[key] = var
        self._combos[key] = combo

    def _load_dropdowns(self):
        def fetch():
            try:
                vets = list(get_all_vets())
                clinics = list(get_all_clinics())
                self.after(0, lambda: self._populate(vets, clinics))
            except Exception as exc:
                self.after(0, lambda: messagebox.showerror("Error", str(exc)))
        threading.Thread(target=fetch, daemon=True).start()

    def _populate(self, vets, clinics):
        self._vets = vets
        self._clinics = clinics
        self._combos["vet_id"]["values"] = [v[1] for v in vets]
        self._combos["clinic_id"]["values"] = [c[1] for c in clinics]

    def _submit(self):
        vet_sel = self.vars["vet_id"].get()
        clinic_sel = self.vars["clinic_id"].get()

        if not vet_sel or not clinic_sel:
            messagebox.showwarning("Missing", "Please select both a Veterinarian and a Clinic.", parent=self)
            return

        vet = next((v for v in self._vets if v[1] == vet_sel), None)
        clinic = next((c for c in self._clinics if c[1] == clinic_sel), None)

        if not vet or not clinic:
            messagebox.showwarning("Error", "Could not find selected vet or clinic.", parent=self)
            return

        vet_id = vet[0]
        clinic_id = clinic[0]

        if self.on_save:
            self.on_save({"vet_id": vet_id, "clinic_id": clinic_id})
        self.destroy()


class WorkatScreen(tk.Frame):
    COLUMNS = 3
    CARD_PAD = 16

    def __init__(self, parent, **kwargs):
        super().__init__(parent, bg=t.BG_SECONDARY, **kwargs)
        self._all_records = []
        self._build_ui()
        self._load_records()

    def _build_ui(self):
        header = tk.Frame(self, bg=t.BG_SECONDARY)
        header.pack(fill="x", padx=36, pady=(28, 0))

        left = tk.Frame(header, bg=t.BG_SECONDARY)
        left.pack(side="left")

        tk.Label(left, text="Works At", **t.PAGE_TITLE_STYLE).pack(anchor="w")
        self.subtitle_lbl = tk.Label(left, text="Loading...", **t.PAGE_SUBTITLE_STYLE)
        self.subtitle_lbl.pack(anchor="w")

        tk.Button(header, text="  + Assign Vet  ", **t.BTN_PRIMARY,
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

    def _load_records(self):
        self.subtitle_lbl.config(text="Loading...")
        threading.Thread(target=self._fetch, daemon=True).start()

    def _fetch(self):
        try:
            data = list(get_all_worksat())
            self.after(0, lambda: self._on_loaded(data, None))
        except Exception as exc:
            self.after(0, lambda: self._on_loaded([], exc))

    def _on_loaded(self, data, error):
        if error:
            messagebox.showerror("DB Error", str(error))
        self._all_records = data
        self._render(self._all_records)

    def _filter(self):
        q = self.search_var.get().lower()
        filtered = [r for r in self._all_records
                    if q in str(r[1]).lower()
                    or q in str(r[3]).lower()]
        self._render(filtered)

    def _render(self, records):
        for w in self.cards_frame.winfo_children():
            w.destroy()

        n = len(records)
        self.subtitle_lbl.config(text=f"{n} assignment{'s' if n != 1 else ''}")

        for idx, record in enumerate(records):
            row, col = divmod(idx, self.COLUMNS)
            WorkatCard(self.cards_frame, record_data=record, color_index=idx,
                       on_delete=self._confirm_delete
                       ).grid(row=row, column=col, padx=self.CARD_PAD // 2,
                              pady=self.CARD_PAD // 2, sticky="nw")

        for c in range(self.COLUMNS):
            self.cards_frame.columnconfigure(c, weight=1)

    def _open_add(self):
        WorkatFormDialog(self, on_save=self._do_insert)

    def _confirm_delete(self, vet_id, clinic_id):
        if messagebox.askyesno("Remove Assignment", "Remove this vet-clinic assignment? This cannot be undone."):
            try:
                delete_worksat(vet_id, clinic_id)
                self._load_records()
            except Exception as exc:
                messagebox.showerror("Error", str(exc))

    def _do_insert(self, data):
        try:
            insert_worksat(data["vet_id"], data["clinic_id"])
            self._load_records()
        except Exception as exc:
            messagebox.showerror("Error", str(exc))