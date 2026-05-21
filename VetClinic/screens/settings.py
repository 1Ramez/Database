import tkinter as tk
from tkinter import messagebox
import threading

import screens.darkMode_Style as t
from services.settings_store import AppSettings, load_settings, save_settings
from services.gemini_client import GeminiClient, GeminiError


GEMINI_KEY_STEPS = (
    "How to get your Gemini API key:\n"
    "1) Open Google AI Studio.\n"
    "2) Sign in with your Google account.\n"
    "3) Find the API keys section (usually “Get API key” / “API keys”).\n"
    "4) Create a new API key.\n"
    "5) Copy the key and paste it here, then press Save.\n\n"
    "Tip: Keep your key private and do not share it."
)


class SettingsScreen(tk.Frame):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, bg=t.BG_SECONDARY, **kwargs)
        self._key_visible = False
        self._build_ui()
        self._load()

    def _build_ui(self):
        outer = tk.Frame(self, bg=t.BG_SECONDARY)
        outer.pack(fill="both", expand=True, padx=30, pady=24)

        tk.Label(outer, text="Settings", **t.PAGE_TITLE_STYLE).pack(anchor="w")
        tk.Label(
            outer,
            text="Configure your Gemini API key for the AI chatbot",
            **t.PAGE_SUBTITLE_STYLE,
        ).pack(anchor="w", pady=(2, 18))

        body = tk.Frame(outer, bg=t.BG_SECONDARY)
        body.pack(fill="both", expand=True)

        card = tk.Frame(body, bg=t.BG_CARD, highlightbackground=t.BORDER, highlightthickness=1)
        card.pack(side="left", fill="both", expand=True, padx=(0, 10))

        tk.Label(card, text="Gemini API", bg=t.BG_CARD, fg=t.TEXT_PRIMARY, font=t.FONT_HEADER).pack(
            anchor="w", padx=16, pady=(16, 8)
        )
        tk.Frame(card, bg=t.BORDER, height=1).pack(fill="x", padx=16, pady=(0, 12))

        form = tk.Frame(card, bg=t.BG_CARD)
        form.pack(fill="x", padx=16, pady=(0, 12))

        tk.Label(form, text="API key", bg=t.BG_CARD, fg=t.TEXT_PRIMARY, font=("Segoe UI", 11, "bold")).pack(
            anchor="w"
        )
        key_row = tk.Frame(form, bg=t.BG_CARD)
        key_row.pack(fill="x", pady=(6, 12))

        self.api_key_var = tk.StringVar()
        self.api_key_entry = tk.Entry(key_row, textvariable=self.api_key_var, **t.ENTRY_STYLE, show="*")
        self.api_key_entry.pack(side="left", fill="x", expand=True, ipady=6)

        self.toggle_btn = tk.Button(key_row, text="Show", **t.BTN_SECONDARY, command=self._toggle_key)
        self.toggle_btn.pack(side="left", padx=(8, 0))

        tk.Label(form, text="Model", bg=t.BG_CARD, fg=t.TEXT_PRIMARY, font=("Segoe UI", 11, "bold")).pack(
            anchor="w"
        )
        self.model_var = tk.StringVar()
        tk.Entry(form, textvariable=self.model_var, **t.ENTRY_STYLE).pack(fill="x", ipady=6, pady=(6, 4))
        tk.Label(
            form,
            text='Examples: "gemini-1.5-flash" (fast), "gemini-1.5-pro" (stronger)',
            bg=t.BG_CARD,
            fg=t.TEXT_MUTED,
            font=t.FONT_SMALL,
            wraplength=560,
            justify="left",
        ).pack(anchor="w", pady=(0, 6))

        btn_row = tk.Frame(card, bg=t.BG_CARD)
        btn_row.pack(fill="x", padx=16, pady=(0, 16))

        self.status_lbl = tk.Label(btn_row, text="", bg=t.BG_CARD, fg=t.TEXT_MUTED, font=t.FONT_SMALL, anchor="w")
        self.status_lbl.pack(side="left", fill="x", expand=True)

        self.test_btn = tk.Button(btn_row, text="Test", **t.BTN_SECONDARY, command=self._test_key)
        self.test_btn.pack(side="right", padx=(8, 0))

        tk.Button(btn_row, text="Save", **t.BTN_PRIMARY, command=self._save).pack(side="right")

        steps = tk.Frame(body, bg=t.BG_CARD, highlightbackground=t.BORDER, highlightthickness=1)
        steps.pack(side="left", fill="both", expand=True)

        tk.Label(steps, text="Get your API key", bg=t.BG_CARD, fg=t.TEXT_PRIMARY, font=t.FONT_HEADER).pack(
            anchor="w", padx=16, pady=(16, 8)
        )
        tk.Frame(steps, bg=t.BORDER, height=1).pack(fill="x", padx=16, pady=(0, 12))
        tk.Label(
            steps,
            text=GEMINI_KEY_STEPS,
            bg=t.BG_CARD,
            fg=t.TEXT_MUTED,
            font=t.FONT_NORMAL,
            justify="left",
            wraplength=520,
        ).pack(anchor="w", padx=16, pady=(0, 16))

    def _toggle_key(self):
        self._key_visible = not self._key_visible
        self.api_key_entry.configure(show="" if self._key_visible else "*")
        self.toggle_btn.configure(text="Hide" if self._key_visible else "Show")

    def _load(self):
        s = load_settings()
        self.api_key_var.set(s.gemini_api_key)
        self.model_var.set(s.gemini_model)

    def _save(self):
        s = AppSettings(
            gemini_api_key=self.api_key_var.get().strip(),
            gemini_model=self.model_var.get().strip() or "gemini-1.5-flash",
        )
        save_settings(s)
        self.status_lbl.config(text="Saved.", fg=t.TEXT_MUTED)
        messagebox.showinfo("Saved", "Settings saved.", parent=self)

    def _test_key(self):
        api_key = self.api_key_var.get().strip()
        model = self.model_var.get().strip() or "gemini-1.5-flash"

        self.test_btn.configure(state="disabled")
        self.status_lbl.config(text="Testing...", fg=t.TEXT_MUTED)

        def work():
            try:
                client = GeminiClient(api_key=api_key, model=model)
                reply = client.generate_reply(
                    [{"role": "user", "text": "Reply with exactly: OK"}],
                    system_instruction="Reply with short plain text only.",
                )
                ok = "OK" in reply.strip().upper()
                msg = "Test successful." if ok else f"Got a reply, but not OK: {reply}"
                self.after(0, lambda: self._test_done(msg, success=ok))
            except GeminiError as e:
                self.after(0, lambda: self._test_done(str(e), success=False))
            except Exception as e:
                self.after(0, lambda: self._test_done(f"Unexpected error: {e}", success=False))

        threading.Thread(target=work, daemon=True).start()

    def _test_done(self, msg: str, success: bool):
        self.test_btn.configure(state="normal")
        self.status_lbl.config(text=msg, fg=(t.SUCCESS if success else t.DANGER))
