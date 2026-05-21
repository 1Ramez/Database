import json
import urllib.error
import urllib.parse
import urllib.request


class GeminiError(RuntimeError):
    def __init__(self, message: str, code: int | None = None, detail: str | None = None):
        super().__init__(message)
        self.code = code
        self.detail = detail


class GeminiClient:
    """
    Minimal Gemini REST client without extra dependencies.

    Endpoint:
      POST https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key=API_KEY
    """

    def __init__(self, api_key: str, model: str = "gemini-1.5-flash", timeout_s: int = 40):
        self.api_key = (api_key or "").strip()
        self.model = (model or "gemini-1.5-flash").strip()
        self.timeout_s = timeout_s

    def _endpoint(self) -> str:
        if not self.api_key:
            raise GeminiError("Missing Gemini API key. Add it from Settings.")
        base = f"https://generativelanguage.googleapis.com/v1beta/models/{urllib.parse.quote(self.model)}:generateContent"
        return f"{base}?key={urllib.parse.quote(self.api_key)}"

    @staticmethod
    def _messages_to_contents(messages):
        contents = []
        for m in messages:
            role = m.get("role")
            txt = (m.get("text") or "").strip()
            if not txt:
                continue
            api_role = "model" if role in ("assistant", "model") else "user"
            contents.append({"role": api_role, "parts": [{"text": txt}]})
        return contents

    def generate_reply(self, messages, system_instruction: str | None = None) -> str:
        body = {"contents": self._messages_to_contents(messages)}
        if system_instruction:
            body["systemInstruction"] = {"parts": [{"text": system_instruction}]}

        req = urllib.request.Request(
            self._endpoint(),
            data=json.dumps(body).encode("utf-8"),
            headers={"Content-Type": "application/json"},
            method="POST",
        )

        try:
            with urllib.request.urlopen(req, timeout=self.timeout_s) as resp:
                data = json.loads(resp.read().decode("utf-8", errors="replace"))
        except urllib.error.HTTPError as e:
            detail = ""
            try:
                detail = e.read().decode("utf-8", errors="replace")
            except Exception:
                detail = str(e)
            raise GeminiError(f"Gemini API error ({e.code}).", code=e.code, detail=detail) from e
        except urllib.error.URLError as e:
            raise GeminiError(f"Network error calling Gemini API: {e}") from e

        try:
            candidates = data.get("candidates") or []
            content = (candidates[0] or {}).get("content") or {}
            parts = content.get("parts") or []
            text = (parts[0] or {}).get("text") or ""
            text = text.strip()
            if not text:
                raise KeyError("Empty response")
            return text
        except Exception as e:
            raise GeminiError(f"Unexpected Gemini response: {data}") from e
