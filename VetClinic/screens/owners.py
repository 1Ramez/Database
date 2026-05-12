import tkinter as tk
from tkinter import messagebox
import threading
import screens.darkMode_Style as t
from queries.owner_queries import get_all_owners, insert_owner, update_owner, delete_owner

AVATAR_COLORS = [
    ("#00d4d4", t.BG_PRIMARY),
    ("#7c3aed", t.BG_PRIMARY),
    ("#ef4444", t.BG_PRIMARY),
    ("#f59e0b", t.BG_PRIMARY),
    ("#22c55e", t.BG_PRIMARY),
    ("#3b82f6", t.BG_PRIMARY),
    ("#ec4899", t.BG_PRIMARY),
]

def _avatar_colors(index):
    return AVATAR_COLORS[index % len(AVATAR_COLORS)]

def _initials(name):
    parts = name.strip().split()
    if len(parts) >= 2:
        return (parts[0][0] + parts[-1][0]).upper()
    return name[:2].upper() if name else "?"


class OwnerCard(tk.Frame):
    CARD_W = 260
    CARD_H = 155

    def __init__(self, parent, owner_data, color_index, on_edit=None, on_delete=None, **kwargs):
        super().__init__(parent, bg=t.BG_CARD, highlightbackground=t.BORDER,
                         highlightthickness=1, relief="flat",
                         width=self.CARD_W, height=self.CARD_H, **kwargs)
        self.pack_propagate(False)

        owner_id, name, billing, emergency, phone = owner_data
        av_bg, av_fg = _avatar_colors(color_index)

        top = tk.Frame(self, bg=t.BG_CARD)
        top.pack(fill="x", padx=14, pady=(14, 0))

        tk.Label(top, text=_initials(name), bg=av_bg, fg=av_fg,
                 font=("Segoe UI", 14, "bold"), width=3, relief="flat").pack(side="left")

        btn_frame = tk.Frame(top, bg=t.BG_CARD)
        btn_frame.pack(side="right")

        tk.Button(btn_frame, text="✏", bg=t.BG_CARD, fg=t.TEXT_MUTED,
                  font=("Segoe UI", 13), relief="flat", borderwidth=0,
                  cursor="hand2", activebackground=t.BG_HOVER, activeforeground=t.TEXT_PRIMARY,
                  command=lambda: on_edit(owner_id) if on_edit else None).pack(side="left", padx=(0, 4))

        tk.Button(btn_frame, text="🗑", bg=t.BG_CARD, fg=t.DANGER,
                  font=("Segoe UI", 13), relief="flat", borderwidth=0,
                  cursor="hand2", activebackground=t.BG_HOVER, activeforeground=t.DANGER,
                  command=lambda: on_delete(owner_id) if on_delete else None).pack(side="left")

        tk.Label(self, text=name, bg=t.BG_CARD, fg=t.TEXT_PRIMARY,
                 font=("Segoe UI", 13, "bold"), anchor="w").pack(fill="x", padx=14, pady=(10, 4))

        info = tk.Frame(self, bg=t.BG_CARD)
        info.pack(fill="x", padx=14)

        for icon, value in [("📞", phone or "—"), ("✉", billing or "—")]:
            row = tk.Frame(info, bg=t.BG_CARD)
            row.pack(fill="x", pady=1)
            tk.Label(row, text=icon, bg=t.BG_CARD, fg=t.TEXT_MUTED, font=t.FONT_SMALL).pack(side="left")
            tk.Label(row, text=f"  {value}", bg=t.BG_CARD, fg=t.TEXT_MUTED,
                     font=t.FONT_SMALL, anchor="w").pack(side="left")

        self.bind("<Enter>", lambda e: self.config(highlightbackground=t.ACCENT_CYAN))
        self.bind("<Leave>", lambda e: self.config(highlightbackground=t.BORDER))


class OwnerFormDialog(tk.Toplevel):
    def __init__(self, parent, title="Add Owner", owner_data=None, on_save=None):
        super().__init__(parent)
        self.title(title)
        self.configure(bg=t.BG_CARD)
        self.resizable(False, False)
        self.on_save = on_save

        w, h = 450, 480
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

        self._field(form, "Full Name *", "name")
        self._field(form, "Phone", "phone")
        self._field(form, "Billing Address", "billing", is_textarea=True)
        self._field(form, "Emergency Contact", "emergency")

        if owner_data:
            owner_id, name, billing, emergency, phone = owner_data
            self.vars["name"].set(name)
            self.vars["phone"].set(phone or "")
            self.vars["billing_text"].insert("1.0", billing or "")
            self.vars["emergency"].set(emergency or "")

        btn_row = tk.Frame(self, bg=t.BG_CARD)
        btn_row.pack(fill="x", padx=24, pady=12)

        tk.Button(btn_row, text="Cancel", **t.BTN_SECONDARY,
                  width=10, command=self.destroy).pack(side="right", padx=(8, 0))

        tk.Button(btn_row, text=title, **t.BTN_PRIMARY,
                  width=12, command=self._submit).pack(side="right")

    def _field(self, parent, label, key, is_textarea=False):
        tk.Label(parent, text=label, bg=t.BG_CARD, fg=t.TEXT_PRIMARY,
                 font=("Segoe UI", 11, "bold"), anchor="w").pack(fill="x", pady=(6, 3))

        if is_textarea:
            txt = tk.Text(parent, bg=t.BG_CARD, fg=t.TEXT_PRIMARY, font=t.FONT_NORMAL,
                          height=2, relief="flat", highlightthickness=1,
                          highlightbackground=t.BORDER, insertbackground=t.ACCENT_CYAN)
            txt.pack(fill="x")
            self.vars[f"{key}_text"] = txt
            txt.bind("<FocusIn>", lambda e: e.widget.config(highlightbackground=t.ACCENT_CYAN))
            txt.bind("<FocusOut>", lambda e: e.widget.config(highlightbackground=t.BORDER))
            self._entries[key] = txt
        else:
            var = tk.StringVar()
            entry = tk.Entry(parent, textvariable=var, **t.ENTRY_STYLE)
            entry.pack(fill="x", ipady=6)
            self.vars[key] = var
            entry.bind("<FocusIn>", lambda e: e.widget.config(highlightbackground=t.ACCENT_CYAN))
            entry.bind("<FocusOut>", lambda e: e.widget.config(highlightbackground=t.BORDER))
            self._entries[key] = entry

    def _submit(self):
        data = {}
        for k, v in self.vars.items():
            if k.endswith("_text"):
                data[k.replace("_text", "")] = v.get("1.0", "end-1c").strip()
            else:
                data[k] = v.get().strip()

        if not data.get("name"):
            messagebox.showwarning("Missing", "Full Name is required.", parent=self)
            return
        if not all(c.isalpha() or c.isspace() for c in data.get("name", "")):
            messagebox.showwarning("Invalid", "Name must contain letters only.", parent=self)
            return
        if data.get("phone") and not data.get("phone").isdigit():
            messagebox.showwarning("Invalid", "Phone must be numbers only.", parent=self)
            return

        if self.on_save:
            self.on_save(data)
        self.destroy()


class OwnersScreen(tk.Frame):
    COLUMNS = 3
    CARD_PAD = 16

    def __init__(self, parent, **kwargs):
        super().__init__(parent, bg=t.BG_SECONDARY, **kwargs)
        self._all_owners = []
        self._build_ui()
        self._load_owners()

    def _build_ui(self):
        header = tk.Frame(self, bg=t.BG_SECONDARY)
        header.pack(fill="x", padx=36, pady=(28, 0))

        left = tk.Frame(header, bg=t.BG_SECONDARY)
        left.pack(side="left")

        tk.Label(left, text="Pet Owners", **t.PAGE_TITLE_STYLE).pack(anchor="w")
        self.subtitle_lbl = tk.Label(left, text="Loading...", **t.PAGE_SUBTITLE_STYLE)
        self.subtitle_lbl.pack(anchor="w")

        tk.Button(header, text="  + Add Owner  ", **t.BTN_PRIMARY,
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

    def _load_owners(self):
        self.subtitle_lbl.config(text="Loading...")
        threading.Thread(target=self._fetch, daemon=True).start()

    def _fetch(self):
        try:
            data = list(get_all_owners())
            self.after(0, lambda: self._on_loaded(data, None))
        except Exception as exc:
            self.after(0, lambda: self._on_loaded([], exc))

    def _on_loaded(self, data, error):
        if error:
            messagebox.showerror("DB Error", str(error))
        self._all_owners = data
        self._render(self._all_owners)

    def _filter(self):
        q = self.search_var.get().lower()
        filtered = [o for o in self._all_owners
                    if q in str(o[1]).lower()
                    or q in str(o[4]).lower()
                    or q in str(o[2]).lower()]
        self._render(filtered)

    def _render(self, owners):
        for w in self.cards_frame.winfo_children():
            w.destroy()

        n = len(owners)
        self.subtitle_lbl.config(text=f"{n} owner{'s' if n != 1 else ''} registered")

        for idx, owner in enumerate(owners):
            row, col = divmod(idx, self.COLUMNS)
            OwnerCard(self.cards_frame, owner_data=owner, color_index=idx,
                      on_edit=self._open_edit, on_delete=self._confirm_delete
                      ).grid(row=row, column=col, padx=self.CARD_PAD // 2,
                             pady=self.CARD_PAD // 2, sticky="nw")

        for c in range(self.COLUMNS):
            self.cards_frame.columnconfigure(c, weight=1)

    def _open_add(self):
        OwnerFormDialog(self, title="Add Owner", on_save=self._do_insert)

    def _open_edit(self, owner_id):
        owner = next((o for o in self._all_owners if str(o[0]) == str(owner_id)), None)
        if not owner:
            return
        OwnerFormDialog(self, title="Edit Owner", owner_data=owner,
                        on_save=lambda d: self._do_update(owner_id, d))

    def _confirm_delete(self, owner_id):
        owner = next((o for o in self._all_owners if str(o[0]) == str(owner_id)), None)
        name = owner[1] if owner else owner_id
        if messagebox.askyesno("Delete Owner", f"Delete '{name}'? This cannot be undone."):
            try:
                delete_owner(owner_id)
                self._load_owners()
            except Exception as exc:
                messagebox.showerror("Error", str(exc))

    def _do_insert(self, data):
        try:
            insert_owner(data["name"], data["billing"], data["emergency"], data["phone"])
            self._load_owners()
        except Exception as exc:
            messagebox.showerror("Error", str(exc))

    def _do_update(self, owner_id, data):
        try:
            update_owner(owner_id, data["name"],
                         data["billing"], data["emergency"], data["phone"])
            self._load_owners()
        except Exception as exc:
            messagebox.showerror("Error", str(exc))