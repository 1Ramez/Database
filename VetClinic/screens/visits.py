import tkinter as tk
from tkinter import messagebox, ttk
import threading
from datetime import datetime
import screens.darkMode_Style as t
from queries.visit_queries import get_all_visits, insert_visit, update_visit, delete_visit
from queries.pet_queries import get_all_pets
from queries.vet_queries import get_all_vets
from queries.clinic_queries import get_all_clinics


class VisitCard(tk.Frame):
    CARD_W = 300
    CARD_H = 200

    def __init__(self, parent, visit_data, color_index, on_edit=None, on_delete=None, **kwargs):
        super().__init__(parent, bg=t.BG_CARD, highlightbackground=t.BORDER,
                         highlightthickness=1, relief="flat",
                         width=self.CARD_W, height=self.CARD_H, **kwargs)
        self.pack_propagate(False)

        visit_id, visit_date, reason, pet_id, pet_name, vet_id, vet_name, clinic_id, clinic_name = visit_data

        top = tk.Frame(self, bg=t.BG_CARD)
        top.pack(fill="x", padx=14, pady=(14, 0))

        date_str = visit_date.strftime("%b %d, %Y") if hasattr(visit_date, "strftime") else str(visit_date)[:10]
        tk.Label(top, text=date_str, bg=t.ACCENT_CYAN, fg=t.BG_PRIMARY,
                 font=("Segoe UI", 10, "bold"), padx=8, pady=3).pack(side="left")

        btn_frame = tk.Frame(top, bg=t.BG_CARD)
        btn_frame.pack(side="right")

        tk.Button(btn_frame, text="✏", bg=t.BG_CARD, fg=t.TEXT_MUTED,
                  font=("Segoe UI", 13), relief="flat", borderwidth=0,
                  cursor="hand2", activebackground=t.BG_HOVER, activeforeground=t.TEXT_PRIMARY,
                  command=lambda: on_edit(visit_id) if on_edit else None).pack(side="left", padx=(0, 4))

        tk.Button(btn_frame, text="🗑", bg=t.BG_CARD, fg=t.DANGER,
                  font=("Segoe UI", 13), relief="flat", borderwidth=0,
                  cursor="hand2", activebackground=t.BG_HOVER, activeforeground=t.DANGER,
                  command=lambda: on_delete(visit_id) if on_delete else None).pack(side="left")

        tk.Label(self, text=pet_name or "Unknown Pet", bg=t.BG_CARD, fg=t.TEXT_PRIMARY,
                 font=("Segoe UI", 13, "bold"), anchor="w").pack(fill="x", padx=14, pady=(10, 2))

        info = tk.Frame(self, bg=t.BG_CARD)
        info.pack(fill="x", padx=14)

        for icon, value in [("⚕️", vet_name or "—"), ("🏥", clinic_name or "—"), ("📋", reason or "—")]:
            row = tk.Frame(info, bg=t.BG_CARD)
            row.pack(fill="x", pady=1)
            tk.Label(row, text=icon, bg=t.BG_CARD, fg=t.TEXT_MUTED, font=t.FONT_SMALL).pack(side="left")
            tk.Label(row, text=f"  {value}", bg=t.BG_CARD, fg=t.TEXT_MUTED,
                     font=t.FONT_SMALL, anchor="w").pack(side="left")

        self.bind("<Enter>", lambda e: self.config(highlightbackground=t.ACCENT_CYAN))
        self.bind("<Leave>", lambda e: self.config(highlightbackground=t.BORDER))


class VisitFormDialog(tk.Toplevel):
    def __init__(self, parent, title="Add Visit", visit_data=None, on_save=None):
        super().__init__(parent)
        self.title(title)
        self.configure(bg=t.BG_CARD)
        self.resizable(False, False)
        self.on_save = on_save
        self._pets = []
        self._vets = []
        self._clinics = []

        w, h = 460, 500
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

        self._dropdown(form, "Pet *", "pet_id")
        self._dropdown(form, "Veterinarian *", "vet_id")
        self._dropdown(form, "Clinic *", "clinic_id")
        self._field(form, "Visit Date * (YYYY-MM-DD)", "visit_date")
        self._field(form, "Reason *", "reason")

        self._load_dropdowns(visit_data)

        btn_row = tk.Frame(self, bg=t.BG_CARD)
        btn_row.pack(fill="x", padx=24, pady=12)

        tk.Button(btn_row, text="Cancel", **t.BTN_SECONDARY,
                  width=10, command=self.destroy).pack(side="right", padx=(8, 0))

        tk.Button(btn_row, text=title, **t.BTN_PRIMARY,
                  width=14, command=self._submit).pack(side="right")

    def _field(self, parent, label, key):
        tk.Label(parent, text=label, bg=t.BG_CARD, fg=t.TEXT_PRIMARY,
                 font=("Segoe UI", 11, "bold"), anchor="w").pack(fill="x", pady=(6, 3))

        var = tk.StringVar()
        entry = tk.Entry(parent, textvariable=var, **t.ENTRY_STYLE)
        entry.pack(fill="x", ipady=6)
        self.vars[key] = var
        entry.bind("<FocusIn>", lambda e: e.widget.config(highlightbackground=t.ACCENT_CYAN))
        entry.bind("<FocusOut>", lambda e: e.widget.config(highlightbackground=t.BORDER))

    def _dropdown(self, parent, label, key):
        tk.Label(parent, text=label, bg=t.BG_CARD, fg=t.TEXT_PRIMARY,
                 font=("Segoe UI", 11, "bold"), anchor="w").pack(fill="x", pady=(6, 3))

        var = tk.StringVar()
        combo = ttk.Combobox(parent, textvariable=var, state="readonly", font=t.FONT_NORMAL)
        combo.pack(fill="x", ipady=4)
        self.vars[key] = var
        self._combos[key] = combo

    def _load_dropdowns(self, visit_data=None):
        def fetch():
            try:
                pets = list(get_all_pets())
                vets = list(get_all_vets())
                clinics = list(get_all_clinics())
                self.after(0, lambda: self._populate(pets, vets, clinics, visit_data))
            except Exception as exc:
                self.after(0, lambda: messagebox.showerror("Error", str(exc)))
        threading.Thread(target=fetch, daemon=True).start()

    def _populate(self, pets, vets, clinics, visit_data):
        self._pets = pets
        self._vets = vets
        self._clinics = clinics

        self._combos["pet_id"]["values"] = [f"{p[0]} - {p[1]}" for p in pets]
        self._combos["vet_id"]["values"] = [f"{v[0]} - {v[1]}" for v in vets]
        self._combos["clinic_id"]["values"] = [f"{c[0]} - {c[1]}" for c in clinics]

        if visit_data:
            visit_id, visit_date, reason, pet_id, pet_name, vet_id, vet_name, clinic_id, clinic_name = visit_data
            self.vars["pet_id"].set(f"{pet_id} - {pet_name}")
            self.vars["vet_id"].set(f"{vet_id} - {vet_name}")
            self.vars["clinic_id"].set(f"{clinic_id} - {clinic_name}")
            date_str = visit_date.strftime("%Y-%m-%d") if hasattr(visit_date, "strftime") else str(visit_date)[:10]
            self.vars["visit_date"].set(date_str)
            self.vars["reason"].set(reason or "")

    def _submit(self):
        pet_sel = self.vars["pet_id"].get()
        vet_sel = self.vars["vet_id"].get()
        clinic_sel = self.vars["clinic_id"].get()
        visit_date = self.vars["visit_date"].get().strip()
        reason = self.vars["reason"].get().strip()

        if not pet_sel or not vet_sel or not clinic_sel:
            messagebox.showwarning("Missing", "Please select Pet, Vet and Clinic.", parent=self)
            return
        if not visit_date or not reason:
            messagebox.showwarning("Missing", "Visit Date and Reason are required.", parent=self)
            return
        try:
            datetime.strptime(visit_date, "%Y-%m-%d")
        except ValueError:
            messagebox.showwarning("Invalid", "Date must be in YYYY-MM-DD format.", parent=self)
            return

        pet_id = int(pet_sel.split(" - ")[0])
        vet_id = int(vet_sel.split(" - ")[0])
        clinic_id = int(clinic_sel.split(" - ")[0])

        if self.on_save:
            self.on_save({"pet_id": pet_id, "vet_id": vet_id, "clinic_id": clinic_id,
                          "visit_date": visit_date, "reason": reason})
        self.destroy()
 
class VisitsScreen(tk.Frame):
    COLUMNS = 3
    CARD_PAD = 16

    def __init__(self, parent, **kwargs):
        super().__init__(parent, bg=t.BG_SECONDARY, **kwargs)
        self._all_visits = []
        self._build_ui()
        self._load_visits()

    def _build_ui(self):
        header = tk.Frame(self, bg=t.BG_SECONDARY)
        header.pack(fill="x", padx=36, pady=(28, 0))

        left = tk.Frame(header, bg=t.BG_SECONDARY)
        left.pack(side="left")

        tk.Label(left, text="Visits", **t.PAGE_TITLE_STYLE).pack(anchor="w")
        self.subtitle_lbl = tk.Label(left, text="Loading...", **t.PAGE_SUBTITLE_STYLE)
        self.subtitle_lbl.pack(anchor="w")

        tk.Button(header, text="  + Add Visit  ", **t.BTN_PRIMARY,
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

    def _load_visits(self):
        self.subtitle_lbl.config(text="Loading...")
        threading.Thread(target=self._fetch, daemon=True).start()

    def _fetch(self):
        try:
            data = list(get_all_visits())
            self.after(0, lambda: self._on_loaded(data, None))
        except Exception as exc:
            self.after(0, lambda: self._on_loaded([], exc))

    def _on_loaded(self, data, error):
        if error:
            messagebox.showerror("DB Error", str(error))
        self._all_visits = data
        self._render(self._all_visits)

    def _filter(self):
        q = self.search_var.get().lower()
        filtered = [v for v in self._all_visits
                    if q in str(v[4]).lower()
                    or q in str(v[6]).lower()
                    or q in str(v[8]).lower()
                    or q in str(v[2]).lower()]
        self._render(filtered)

    def _render(self, visits):
        for w in self.cards_frame.winfo_children():
            w.destroy()

        n = len(visits)
        self.subtitle_lbl.config(text=f"{n} visit{'s' if n != 1 else ''} recorded")

        for idx, visit in enumerate(visits):
            row, col = divmod(idx, self.COLUMNS)
            VisitCard(self.cards_frame, visit_data=visit, color_index=idx,
                      on_edit=self._open_edit, on_delete=self._confirm_delete
                      ).grid(row=row, column=col, padx=self.CARD_PAD // 2,
                             pady=self.CARD_PAD // 2, sticky="nw")

        for c in range(self.COLUMNS):
            self.cards_frame.columnconfigure(c, weight=1)

    def _open_add(self):
        VisitFormDialog(self, title="Add Visit", on_save=self._do_insert)

    def _open_edit(self, visit_id):
        visit = next((v for v in self._all_visits if str(v[0]) == str(visit_id)), None)
        if not visit:
            return
        VisitFormDialog(self, title="Edit Visit", visit_data=visit,
                        on_save=lambda d: self._do_update(visit_id, d))

    def _confirm_delete(self, visit_id):
        if messagebox.askyesno("Delete Visit", "Delete this visit? This cannot be undone."):
            try:
                delete_visit(visit_id)
                self._load_visits()
            except Exception as exc:
                messagebox.showerror("Error", str(exc))

    def _do_insert(self, data):
        try:
            insert_visit(data["clinic_id"], data["pet_id"], data["vet_id"],
                         data["visit_date"], data["reason"])
            self._load_visits()
        except Exception as exc:
            messagebox.showerror("Error", str(exc))

    def _do_update(self, visit_id, data):
        try:
            update_visit(visit_id, data["clinic_id"], data["pet_id"], data["vet_id"],
                         data["visit_date"], data["reason"])
            self._load_visits()
        except Exception as exc:
            messagebox.showerror("Error", str(exc))