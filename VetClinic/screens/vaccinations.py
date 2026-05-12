import tkinter as tk
from tkinter import messagebox, ttk
import threading
from datetime import datetime
import screens.darkMode_Style as t
from queries.vaccination_queries import get_all_vaccination_records, insert_vaccination_record, update_vaccination_record, delete_vaccination_record
from queries.vaccine_queries import get_all_vaccines
from queries.clinical_note_queries import get_all_clinical_notes


class VaccinationCard(tk.Frame):
    CARD_W = 300
    CARD_H = 220

    def __init__(self, parent, record_data, color_index, on_edit=None, on_delete=None, **kwargs):
        super().__init__(parent, bg=t.BG_CARD, highlightbackground=t.BORDER,
                         highlightthickness=1, relief="flat",
                         width=self.CARD_W, height=self.CARD_H, **kwargs)
        self.pack_propagate(False)

        record_id, batch_num, vaccine_type, next_booster, vaccine_id, vaccine_name, note_id, vet_name = record_data

        top = tk.Frame(self, bg=t.BG_CARD)
        top.pack(fill="x", padx=14, pady=(14, 0))

        tk.Label(top, text="💉", bg=t.ACCENT_CYAN, fg=t.BG_PRIMARY,
                 font=("Segoe UI", 13), width=3, relief="flat").pack(side="left")

        btn_frame = tk.Frame(top, bg=t.BG_CARD)
        btn_frame.pack(side="right")

        tk.Button(btn_frame, text="✏", bg=t.BG_CARD, fg=t.TEXT_MUTED,
                  font=("Segoe UI", 13), relief="flat", borderwidth=0,
                  cursor="hand2", activebackground=t.BG_HOVER, activeforeground=t.TEXT_PRIMARY,
                  command=lambda: on_edit(record_id) if on_edit else None).pack(side="left", padx=(0, 4))

        tk.Button(btn_frame, text="🗑", bg=t.BG_CARD, fg=t.DANGER,
                  font=("Segoe UI", 13), relief="flat", borderwidth=0,
                  cursor="hand2", activebackground=t.BG_HOVER, activeforeground=t.DANGER,
                  command=lambda: on_delete(record_id) if on_delete else None).pack(side="left")

        tk.Label(self, text=vaccine_name or vaccine_type or "Unknown Vaccine", bg=t.BG_CARD, fg=t.TEXT_PRIMARY,
                 font=("Segoe UI", 13, "bold"), anchor="w").pack(fill="x", padx=14, pady=(10, 2))

        info = tk.Frame(self, bg=t.BG_CARD)
        info.pack(fill="x", padx=14)

        date_str = next_booster.strftime("%b %d, %Y") if hasattr(next_booster, "strftime") else str(next_booster)[:10] if next_booster else "—"

        for icon, value in [("🔢", f"Batch: {batch_num or '—'}"),
                             ("📅", f"Next Booster: {date_str}"),
                             ("⚕️", vet_name or "—"),
                             ("📝", f"Note ID: {note_id or '—'}")]:
            row = tk.Frame(info, bg=t.BG_CARD)
            row.pack(fill="x", pady=1)
            tk.Label(row, text=icon, bg=t.BG_CARD, fg=t.TEXT_MUTED, font=t.FONT_SMALL).pack(side="left")
            tk.Label(row, text=f"  {value}", bg=t.BG_CARD, fg=t.TEXT_MUTED,
                     font=t.FONT_SMALL, anchor="w").pack(side="left")

        self.bind("<Enter>", lambda e: self.config(highlightbackground=t.ACCENT_CYAN))
        self.bind("<Leave>", lambda e: self.config(highlightbackground=t.BORDER))


class VaccinationFormDialog(tk.Toplevel):
    def __init__(self, parent, title="Add Vaccination", record_data=None, on_save=None):
        super().__init__(parent)
        self.title(title)
        self.configure(bg=t.BG_CARD)
        self.resizable(False, False)
        self.on_save = on_save
        self._vaccines = []
        self._notes = []

        w, h = 460, 520
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

        self._dropdown(form, "Vaccine *", "vaccine_id")
        self._dropdown(form, "Clinical Note *", "note_id")
        self._field(form, "Batch Number", "batch_num")
        self._field(form, "Next Booster Date (YYYY-MM-DD)", "date_next_booster")
        self._field(form, "Vaccine Type", "vaccine_type")

        self._load_dropdowns(record_data)

        btn_row = tk.Frame(self, bg=t.BG_CARD)
        btn_row.pack(fill="x", padx=24, pady=12)

        tk.Button(btn_row, text="Cancel", **t.BTN_SECONDARY,
                  width=10, command=self.destroy).pack(side="right", padx=(8, 0))

        tk.Button(btn_row, text=title, **t.BTN_PRIMARY,
                  width=16, command=self._submit).pack(side="right")

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

    def _load_dropdowns(self, record_data=None):
        def fetch():
            try:
                vaccines = list(get_all_vaccines())
                notes = list(get_all_clinical_notes())
                self.after(0, lambda: self._populate(vaccines, notes, record_data))
            except Exception as exc:
                self.after(0, lambda: messagebox.showerror("Error", str(exc)))
        threading.Thread(target=fetch, daemon=True).start()

    def _populate(self, vaccines, notes, record_data):
        self._vaccines = vaccines
        self._notes = notes

        self._combos["vaccine_id"]["values"] = [f"{v[1]} - {v[0]}" for v in vaccines]
        self._combos["note_id"]["values"] = [
            f"{n[0]} - {n[5] or 'Note ' + str(n[0])}"
            for n in notes
        ]

        if record_data:
            record_id, batch_num, vaccine_type, next_booster, vaccine_id, vaccine_name, note_id, vet_name = record_data
            self.vars["vaccine_id"].set(f"{vaccine_name or ''} - {vaccine_id or ''}")
            matching_note = next((n for n in notes if str(n[0]) == str(note_id)), None)
            if matching_note:
                self.vars["note_id"].set(f"{matching_note[0]} - {matching_note[5] or 'Note ' + str(matching_note[0])}")
            self.vars["batch_num"].set(str(batch_num) if batch_num else "")
            date_str = next_booster.strftime("%Y-%m-%d") if hasattr(next_booster, "strftime") else str(next_booster)[:10] if next_booster else ""
            self.vars["date_next_booster"].set(date_str)
            self.vars["vaccine_type"].set(vaccine_type or "")

    def _submit(self):
        vaccine_sel = self.vars["vaccine_id"].get()
        note_sel = self.vars["note_id"].get()
        batch_num = self.vars["batch_num"].get().strip()
        date_next_booster = self.vars["date_next_booster"].get().strip()
        vaccine_type = self.vars["vaccine_type"].get().strip()

        if not vaccine_sel or not note_sel:
            messagebox.showwarning("Missing", "Please select Vaccine and Clinical Note.", parent=self)
            return
        if date_next_booster:
            try:
                datetime.strptime(date_next_booster, "%Y-%m-%d")
            except ValueError:
                messagebox.showwarning("Invalid", "Date must be in YYYY-MM-DD format.", parent=self)
                return

        vaccine_id = int(vaccine_sel.split(" - ")[-1])
        note_id = int(note_sel.split(" - ")[0])

        if self.on_save:
            self.on_save({"vaccine_id": vaccine_id, "note_id": note_id,
                          "batch_num": batch_num, "date_next_booster": date_next_booster,
                          "vaccine_type": vaccine_type})
        self.destroy()


class VaccinationsScreen(tk.Frame):
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

        tk.Label(left, text="Vaccinations", **t.PAGE_TITLE_STYLE).pack(anchor="w")
        self.subtitle_lbl = tk.Label(left, text="Loading...", **t.PAGE_SUBTITLE_STYLE)
        self.subtitle_lbl.pack(anchor="w")

        tk.Button(header, text="  + Add Vaccination  ", **t.BTN_PRIMARY,
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
            data = list(get_all_vaccination_records())
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
                    if q in str(r[5]).lower()
                    or q in str(r[2]).lower()
                    or q in str(r[7]).lower()]
        self._render(filtered)

    def _render(self, records):
        for w in self.cards_frame.winfo_children():
            w.destroy()

        n = len(records)
        self.subtitle_lbl.config(text=f"{n} vaccination record{'s' if n != 1 else ''}")

        for idx, record in enumerate(records):
            row, col = divmod(idx, self.COLUMNS)
            VaccinationCard(self.cards_frame, record_data=record, color_index=idx,
                            on_edit=self._open_edit, on_delete=self._confirm_delete
                            ).grid(row=row, column=col, padx=self.CARD_PAD // 2,
                                   pady=self.CARD_PAD // 2, sticky="nw")

        for c in range(self.COLUMNS):
            self.cards_frame.columnconfigure(c, weight=1)

    def _open_add(self):
        VaccinationFormDialog(self, title="Add Vaccination", on_save=self._do_insert)

    def _open_edit(self, record_id):
        record = next((r for r in self._all_records if str(r[0]) == str(record_id)), None)
        if not record:
            return
        VaccinationFormDialog(self, title="Edit Vaccination", record_data=record,
                              on_save=lambda d: self._do_update(record_id, d))

    def _confirm_delete(self, record_id):
        if messagebox.askyesno("Delete Vaccination", "Delete this record? This cannot be undone."):
            try:
                delete_vaccination_record(record_id)
                self._load_records()
            except Exception as exc:
                messagebox.showerror("Error", str(exc))

    def _do_insert(self, data):
        try:
            insert_vaccination_record(data["batch_num"], data["date_next_booster"], data["vaccine_type"])
            self._load_records()
        except Exception as exc:
            messagebox.showerror("Error", str(exc))

    def _do_update(self, record_id, data):
        try:
            update_vaccination_record(record_id, data["note_id"], data["vaccine_id"],
                                      data["batch_num"], data["date_next_booster"], data["vaccine_type"])
            self._load_records()
        except Exception as exc:
            messagebox.showerror("Error", str(exc))