import tkinter as tk
from tkinter import messagebox
import threading
import screens.darkMode_Style as t
from queries.pet_queries import get_all_pets, insert_pet, update_pet, delete_pet
from queries.owner_queries import get_all_owners

SPECIES_ICONS = {
    "canine": "🐕",
    "feline": "🐈",
    "avian": "🦜",
    "reptile": "🦎",
    "rodent": "🐹",
    "other": "🐾",
}

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

def _species_icon(specie):
    return SPECIES_ICONS.get(specie.lower(), "🐾")


class PetCard(tk.Frame):
    CARD_W = 260
    CARD_H = 155

    def __init__(self, parent, pet_data, color_index, on_edit=None, on_delete=None, **kwargs):
        super().__init__(parent, bg=t.BG_CARD, highlightbackground=t.BORDER,
                         highlightthickness=1, relief="flat",
                         width=self.CARD_W, height=self.CARD_H, **kwargs)
        self.pack_propagate(False)

        pet_id, name, specie, breed, gender, dob, owner_id, owner_name = pet_data
        av_bg, av_fg = _avatar_colors(color_index)

        top = tk.Frame(self, bg=t.BG_CARD)
        top.pack(fill="x", padx=14, pady=(14, 0))

        tk.Label(top, text=_species_icon(specie or ""), bg=av_bg, fg=av_fg,
                 font=("Segoe UI", 14, "bold"), width=3, relief="flat").pack(side="left")

        btn_frame = tk.Frame(top, bg=t.BG_CARD)
        btn_frame.pack(side="right")

        tk.Button(btn_frame, text="✏", bg=t.BG_CARD, fg=t.TEXT_MUTED,
                  font=("Segoe UI", 13), relief="flat", borderwidth=0,
                  cursor="hand2", activebackground=t.BG_HOVER, activeforeground=t.TEXT_PRIMARY,
                  command=lambda: on_edit(pet_id) if on_edit else None).pack(side="left", padx=(0, 4))

        tk.Button(btn_frame, text="🗑", bg=t.BG_CARD, fg=t.DANGER,
                  font=("Segoe UI", 13), relief="flat", borderwidth=0,
                  cursor="hand2", activebackground=t.BG_HOVER, activeforeground=t.DANGER,
                  command=lambda: on_delete(pet_id) if on_delete else None).pack(side="left")

        tk.Label(self, text=name, bg=t.BG_CARD, fg=t.TEXT_PRIMARY,
                 font=("Segoe UI", 13, "bold"), anchor="w").pack(fill="x", padx=14, pady=(10, 4))

        info = tk.Frame(self, bg=t.BG_CARD)
        info.pack(fill="x", padx=14)

        for icon, value in [("🐾", f"{specie or '—'} • {breed or '—'}"),
                             ("👤", f"Owner: {owner_name or 'Unassigned'}")]:
            row = tk.Frame(info, bg=t.BG_CARD)
            row.pack(fill="x", pady=1)
            tk.Label(row, text=icon, bg=t.BG_CARD, fg=t.TEXT_MUTED, font=t.FONT_SMALL).pack(side="left")
            tk.Label(row, text=f"  {value}", bg=t.BG_CARD, fg=t.TEXT_MUTED,
                     font=t.FONT_SMALL, anchor="w").pack(side="left")

        self.bind("<Enter>", lambda e: self.config(highlightbackground=t.ACCENT_CYAN))
        self.bind("<Leave>", lambda e: self.config(highlightbackground=t.BORDER))


class PetFormDialog(tk.Toplevel):
    def __init__(self, parent, title="Add Pet", pet_data=None, on_save=None):
        super().__init__(parent)
        self.title(title)
        self.configure(bg=t.BG_CARD)
        self.resizable(False, False)
        self.on_save = on_save
        self._owners = []

        w, h = 500, 480
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
        form.pack(fill="both", expand=True, padx=24, pady=(0, 12))

        self.vars = {}
        self._entries = {}

        row1 = tk.Frame(form, bg=t.BG_CARD)
        row1.pack(fill="x", pady=4)
        self._field_pair(row1, "Pet Name *", "name", "Breed", "breed")

        row2 = tk.Frame(form, bg=t.BG_CARD)
        row2.pack(fill="x", pady=4)
        self._field_pair(row2, "Date of Birth (YYYY-MM-DD)", "dob", "Gender", "gender", is_gender=True)

        row3 = tk.Frame(form, bg=t.BG_CARD)
        row3.pack(fill="x", pady=4)
        self._dropdown_pair(row3, "Species", "specie", ["Canine", "Feline", "Avian", "Reptile", "Rodent", "Other"], "Owner", "owner")

        if pet_data:
            pet_id, name, specie, breed, gender, dob, owner_id, owner_name = pet_data
            self.vars["name"].set(name or "")
            self.vars["breed"].set(breed or "")
            self.vars["dob"].set(str(dob)[:10] if dob else "")
            self.vars["gender"].set(gender or "Male")
            self.vars["specie"].set(specie or "Canine")
            self._selected_owner_id = owner_id

        btn_row = tk.Frame(self, bg=t.BG_CARD)
        btn_row.pack(fill="x", padx=24, pady=20)

        tk.Button(btn_row, text="Cancel", **t.BTN_SECONDARY,
                  width=10, command=self.destroy).pack(side="right", padx=(8, 0))

        tk.Button(btn_row, text=title, **t.BTN_PRIMARY,
                  width=12, command=self._submit).pack(side="right")

        threading.Thread(target=self._load_owners, daemon=True).start()

    def _field_pair(self, parent, label1, key1, label2, key2, is_gender=False):
        left = tk.Frame(parent, bg=t.BG_CARD)
        left.pack(side="left", fill="x", expand=True, padx=(0, 8))
        
        tk.Label(left, text=label1, bg=t.BG_CARD, fg=t.TEXT_PRIMARY,
                 font=("Segoe UI", 11, "bold"), anchor="w").pack(fill="x", pady=(0, 3))
        var1 = tk.StringVar()
        entry1 = tk.Entry(left, textvariable=var1, **t.ENTRY_STYLE)
        entry1.pack(fill="x", ipady=6)
        self.vars[key1] = var1
        entry1.bind("<FocusIn>", lambda e: e.widget.config(highlightbackground=t.ACCENT_CYAN))
        entry1.bind("<FocusOut>", lambda e: e.widget.config(highlightbackground=t.BORDER))
        self._entries[key1] = entry1

        right = tk.Frame(parent, bg=t.BG_CARD)
        right.pack(side="left", fill="x", expand=True, padx=(8, 0))
        
        tk.Label(right, text=label2, bg=t.BG_CARD, fg=t.TEXT_PRIMARY,
                 font=("Segoe UI", 11, "bold"), anchor="w").pack(fill="x", pady=(0, 3))
        
        if is_gender:
            var2 = tk.StringVar(value="Male")
            menu2 = tk.OptionMenu(right, var2, "Male", "Female")
            menu2.config(bg=t.BG_CARD, fg=t.TEXT_PRIMARY, font=t.FONT_NORMAL,
                         relief="flat", highlightthickness=1, highlightbackground=t.BORDER,
                         activebackground=t.BG_HOVER, activeforeground=t.TEXT_PRIMARY)
            menu2["menu"].config(bg=t.BG_CARD, fg=t.TEXT_PRIMARY, font=t.FONT_NORMAL)
            menu2.pack(fill="x", ipady=4)
            self.vars[key2] = var2
        else:
            var2 = tk.StringVar()
            entry2 = tk.Entry(right, textvariable=var2, **t.ENTRY_STYLE)
            entry2.pack(fill="x", ipady=6)
            self.vars[key2] = var2
            entry2.bind("<FocusIn>", lambda e: e.widget.config(highlightbackground=t.ACCENT_CYAN))
            entry2.bind("<FocusOut>", lambda e: e.widget.config(highlightbackground=t.BORDER))
            self._entries[key2] = entry2

    def _dropdown_pair(self, parent, label1, key1, options1, label2, key2):
        left = tk.Frame(parent, bg=t.BG_CARD)
        left.pack(side="left", fill="x", expand=True, padx=(0, 8))
        
        tk.Label(left, text=label1, bg=t.BG_CARD, fg=t.TEXT_PRIMARY,
                 font=("Segoe UI", 11, "bold"), anchor="w").pack(fill="x", pady=(0, 3))
        var1 = tk.StringVar(value=options1[0])
        menu1 = tk.OptionMenu(left, var1, *options1)
        menu1.config(bg=t.BG_CARD, fg=t.TEXT_PRIMARY, font=t.FONT_NORMAL,
                     relief="flat", highlightthickness=1, highlightbackground=t.BORDER,
                     activebackground=t.BG_HOVER, activeforeground=t.TEXT_PRIMARY)
        menu1["menu"].config(bg=t.BG_CARD, fg=t.TEXT_PRIMARY, font=t.FONT_NORMAL)
        menu1.pack(fill="x", ipady=4)
        self.vars[key1] = var1

        right = tk.Frame(parent, bg=t.BG_CARD)
        right.pack(side="left", fill="x", expand=True, padx=(8, 0))
        
        tk.Label(right, text=label2, bg=t.BG_CARD, fg=t.TEXT_PRIMARY,
                 font=("Segoe UI", 11, "bold"), anchor="w").pack(fill="x", pady=(0, 3))
        self._owner_var = tk.StringVar(value="Unassigned")
        self._owner_menu = tk.OptionMenu(right, self._owner_var, "Unassigned")
        self._owner_menu.config(bg=t.BG_CARD, fg=t.TEXT_PRIMARY, font=t.FONT_NORMAL,
                                relief="flat", highlightthickness=1, highlightbackground=t.BORDER,
                                activebackground=t.BG_HOVER, activeforeground=t.TEXT_PRIMARY)
        self._owner_menu["menu"].config(bg=t.BG_CARD, fg=t.TEXT_PRIMARY, font=t.FONT_NORMAL)
        self._owner_menu.pack(fill="x", ipady=4)
        self._selected_owner_id = None

    def _load_owners(self):
        try:
            owners = list(get_all_owners())
            self.after(0, lambda: self._populate_owners(owners))
        except Exception:
            pass

    def _populate_owners(self, owners):
        self._owners = owners
        menu = self._owner_menu["menu"]
        menu.delete(0, "end")
        menu.add_command(label="Unassigned", command=lambda: self._set_owner(None, "Unassigned"))
        for owner in owners:
            owner_id, name = owner[0], owner[1]
            menu.add_command(label=name, command=lambda oid=owner_id, n=name: self._set_owner(oid, n))
        if self._selected_owner_id:
            owner = next((o for o in owners if o[0] == self._selected_owner_id), None)
            self._owner_var.set(owner[1] if owner else "Unassigned")
        else:
            self._owner_var.set("Unassigned")

    def _set_owner(self, owner_id, name):
        self._selected_owner_id = owner_id
        self._owner_var.set(name)

    def _submit(self):
        data = {k: v.get().strip() for k, v in self.vars.items()}

        if not data.get("name"):
            messagebox.showwarning("Missing", "Pet Name is required.", parent=self)
            return
        if not data.get("dob"):
            messagebox.showwarning("Missing", "Date of Birth is required.", parent=self)
            return

        data["owner_id"] = self._selected_owner_id

        if self.on_save:
            self.on_save(data)
        self.destroy()

class PetsScreen(tk.Frame):
    COLUMNS = 3
    CARD_PAD = 16

    def __init__(self, parent, **kwargs):
        super().__init__(parent, bg=t.BG_SECONDARY, **kwargs)
        self._all_pets = []
        self._build_ui()
        self._load_pets()

    def _build_ui(self):
        header = tk.Frame(self, bg=t.BG_SECONDARY)
        header.pack(fill="x", padx=36, pady=(28, 0))

        left = tk.Frame(header, bg=t.BG_SECONDARY)
        left.pack(side="left")

        tk.Label(left, text="Pets", **t.PAGE_TITLE_STYLE).pack(anchor="w")
        self.subtitle_lbl = tk.Label(left, text="Loading...", **t.PAGE_SUBTITLE_STYLE)
        self.subtitle_lbl.pack(anchor="w")

        tk.Button(header, text="  + Add Pet  ", **t.BTN_PRIMARY,
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

    def _load_pets(self):
        self.subtitle_lbl.config(text="Loading...")
        threading.Thread(target=self._fetch, daemon=True).start()

    def _fetch(self):
        try:
            data = list(get_all_pets())
            self.after(0, lambda: self._on_loaded(data, None))
        except Exception as exc:
            self.after(0, lambda: self._on_loaded([], exc))

    def _on_loaded(self, data, error):
        if error:
            messagebox.showerror("DB Error", str(error))
        self._all_pets = data
        self._render(self._all_pets)

    def _filter(self):
        q = self.search_var.get().lower()
        filtered = [p for p in self._all_pets
                    if q in str(p[1]).lower()
                    or q in str(p[2]).lower()
                    or q in str(p[3]).lower()
                    or q in str(p[7] or "").lower()]
        self._render(filtered)

    def _render(self, pets):
        for w in self.cards_frame.winfo_children():
            w.destroy()

        n = len(pets)
        self.subtitle_lbl.config(text=f"{n} pet{'s' if n != 1 else ''} registered")

        for idx, pet in enumerate(pets):
            row, col = divmod(idx, self.COLUMNS)
            PetCard(self.cards_frame, pet_data=pet, color_index=idx,
                    on_edit=self._open_edit, on_delete=self._confirm_delete
                    ).grid(row=row, column=col, padx=self.CARD_PAD // 2,
                           pady=self.CARD_PAD // 2, sticky="nw")

        for c in range(self.COLUMNS):
            self.cards_frame.columnconfigure(c, weight=1)

    def _open_add(self):
        PetFormDialog(self, title="Add Pet", on_save=self._do_insert)

    def _open_edit(self, pet_id):
        pet = next((p for p in self._all_pets if str(p[0]) == str(pet_id)), None)
        if not pet:
            return
        PetFormDialog(self, title="Edit Pet", pet_data=pet,
                      on_save=lambda d: self._do_update(pet_id, d))

    def _confirm_delete(self, pet_id):
        pet = next((p for p in self._all_pets if str(p[0]) == str(pet_id)), None)
        name = pet[1] if pet else pet_id
        if messagebox.askyesno("Delete Pet", f"Delete '{name}'? This cannot be undone."):
            try:
                delete_pet(pet_id)
                self._load_pets()
            except Exception as exc:
                messagebox.showerror("Error", str(exc))

    def _do_insert(self, data):
        try:
            insert_pet(data["owner_id"], data["name"], data["breed"],
                       data["dob"], data["gender"], data["specie"])
            self._load_pets()
        except Exception as exc:
            messagebox.showerror("Error", str(exc))

    def _do_update(self, pet_id, data):
        try:
            update_pet(pet_id, data["owner_id"], data["name"], data["breed"],
                       data["dob"], data["gender"], data["specie"])
            self._load_pets()
        except Exception as exc:
            messagebox.showerror("Error", str(exc))