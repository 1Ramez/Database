import tkinter as tk
import threading

import screens.darkMode_Style as t
from services.settings_store import load_settings
from services.gemini_client import GeminiClient, GeminiError


class ChatbotScreen(tk.Frame):
    def __init__(self, parent, navigate=None, settings_index=None, **kwargs):
        super().__init__(parent, bg=t.BG_SECONDARY, **kwargs)
        self._navigate = navigate
        self._settings_index = settings_index
        self._messages = []
        self._build_ui()

    def _build_ui(self):
        outer = tk.Frame(self, bg=t.BG_SECONDARY)
        outer.pack(fill="both", expand=True, padx=30, pady=24)

        header = tk.Frame(outer, bg=t.BG_SECONDARY)
        header.pack(fill="x")

        left = tk.Frame(header, bg=t.BG_SECONDARY)
        left.pack(side="left", fill="x", expand=True)
        tk.Label(left, text="AI Chatbot", **t.PAGE_TITLE_STYLE).pack(anchor="w")
        tk.Label(
            left,
            text="Requires your Gemini API key in Settings",
            **t.PAGE_SUBTITLE_STYLE,
        ).pack(anchor="w", pady=(2, 0))

        right = tk.Frame(header, bg=t.BG_SECONDARY)
        right.pack(side="right")
        tk.Button(right, text="Settings", **t.BTN_SECONDARY, command=self._go_settings).pack(side="left", padx=(0, 8))
        tk.Button(right, text="Clear", **t.BTN_SECONDARY, command=self._clear).pack(side="left")

        chat_card = tk.Frame(outer, bg=t.BG_CARD, highlightbackground=t.BORDER, highlightthickness=1)
        chat_card.pack(fill="both", expand=True, pady=(16, 10))

        self.chat = tk.Text(
            chat_card,
            bg=t.BG_CARD,
            fg=t.TEXT_PRIMARY,
            font=t.FONT_NORMAL,
            relief="flat",
            borderwidth=0,
            highlightthickness=0,
            wrap="word",
        )
        self.chat.pack(side="left", fill="both", expand=True, padx=(16, 0), pady=16)

        sb = tk.Scrollbar(chat_card, orient="vertical", command=self.chat.yview, **t.SCROLLBAR_STYLE)
        sb.pack(side="right", fill="y", pady=16, padx=(0, 8))
        self.chat.configure(yscrollcommand=sb.set)

        self.chat.tag_configure("user", foreground=t.ACCENT_CYAN, font=("Segoe UI", 12, "bold"))
        self.chat.tag_configure("assistant", foreground=t.TEXT_PRIMARY, font=("Segoe UI", 12, "bold"))
        self.chat.tag_configure("body", foreground=t.TEXT_MUTED, font=t.FONT_NORMAL)

        self._append("Assistant", "Hi! Add your Gemini API key from Settings, then ask me anything.", role="assistant")

        input_row = tk.Frame(outer, bg=t.BG_SECONDARY)
        input_row.pack(fill="x")

        self.input_var = tk.StringVar()
        self.input_entry = tk.Entry(input_row, textvariable=self.input_var, **t.ENTRY_STYLE)
        self.input_entry.pack(side="left", fill="x", expand=True, ipady=8)
        self.input_entry.bind("<Return>", lambda e: self._send())

        self.send_btn = tk.Button(input_row, text="Send", **t.BTN_PRIMARY, command=self._send)
        self.send_btn.pack(side="left", padx=(10, 0))

        self.status_lbl = tk.Label(outer, text="", bg=t.BG_SECONDARY, fg=t.TEXT_MUTED, font=t.FONT_SMALL, anchor="w")
        self.status_lbl.pack(fill="x", pady=(8, 0))

    def _go_settings(self):
        if self._navigate and isinstance(self._settings_index, int):
            self._navigate(self._settings_index)

    def _clear(self):
        self._messages = []
        self.chat.configure(state="normal")
        self.chat.delete("1.0", "end")
        self.chat.configure(state="disabled")
        self._append("Assistant", "Chat cleared. Ask a new question.", role="assistant")
        self.status_lbl.configure(text="", fg=t.TEXT_MUTED)

    def _append(self, who: str, text: str, role: str):
        self.chat.configure(state="normal")
        tag = "assistant" if role == "assistant" else "user"
        self.chat.insert("end", f"{who}\n", (tag,))
        self.chat.insert("end", f"{text}\n\n", ("body",))
        self.chat.configure(state="disabled")
        self.chat.see("end")

    def _send(self):
        text = self.input_var.get().strip()
        if not text:
            return
        self.input_var.set("")

        self._messages.append({"role": "user", "text": text})
        self._append("You", text, role="user")

        self.send_btn.configure(state="disabled")
        self.status_lbl.configure(text="Thinking...", fg=t.TEXT_MUTED)

        settings = load_settings()
        api_key = (settings.gemini_api_key or "").strip()
        model = (settings.gemini_model or "gemini-1.5-flash").strip()

        def work():
            try:
                client = GeminiClient(api_key=api_key, model=model)
                reply = client.generate_reply(
                    self._messages,
                    system_instruction=(
                        "You are a helpful assistant inside a veterinary clinic database app. "
                        "Be concise and practical."
                    ),
                )
                self._messages.append({"role": "assistant", "text": reply})
                self.after(0, lambda: self._done(reply))
            except GeminiError as e:
                self.after(0, lambda: self._error(str(e)))
            except Exception as e:
                self.after(0, lambda: self._error(f"Unexpected error: {e}"))

        threading.Thread(target=work, daemon=True).start()

    def _done(self, reply: str):
        self._append("Assistant", reply, role="assistant")
        self.send_btn.configure(state="normal")
        self.status_lbl.configure(text="", fg=t.TEXT_MUTED)

    def _error(self, msg: str):
        self._append("Assistant", msg, role="assistant")
        self.send_btn.configure(state="normal")
        self.status_lbl.configure(text="Failed.", fg=t.DANGER)

