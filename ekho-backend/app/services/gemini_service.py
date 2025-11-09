# app/services/gemini_service.py
import os
import asyncio  # <-- 1. IMPORT ASYNCIO
from app.config import get_settings

try:
    import google.generativeai as genai  # type: ignore
except Exception:
    genai = None

class GeminiService:
    def __init__(self):
        settings = get_settings()
        self.api_key = settings.gemini_api_key or os.getenv("GEMINI_API_KEY")
        self.enabled = False
        self.model = None

        if self.api_key and genai:
            try:
                genai.configure(api_key=self.api_key)
                # --- 2. UPDATED MODEL NAME ---
                self.model = genai.GenerativeModel("gemini-2.5-flash-preview-09-2025")
                self.enabled = True
                print("✅ Gemini initialized")
            except Exception as e:
                print("⚠️ Gemini init failed:", e)

    # --- 3. CREATE A SYNC HELPER ---
    def _generate_sync(self, prompt: str) -> str:
        """Synchronous helper that runs the blocking AI call."""
        if not self.enabled or not self.model:
            return "(stub) Tell me more about that." # Simpler stub

        try:
            resp = self.model.generate_content(prompt)
            text = getattr(resp, "text", None)
            return (text or "(no response)").strip()
        except Exception as e:
            print("⚠️ Gemini call failed:", e)
            return "I’m here. What part worries you most?"

    # --- 4. MAKE THE MAIN METHOD ASYNC ---
    async def generate(self, user_message: str, user_name: str = "you") -> str:
        """
        Return a text reply. This method NEVER raises; it returns a stub if SDK/key fail.
        Now runs non-blocking.
        """
        prompt = (
            f"You are {user_name}, speaking to your past self from 5 years in the future. "
            "Warm, concise, supportive. Ask one gentle follow-up question.\n\n"
            f"User: {user_message}"
        )

        if not self.enabled:
             return f"(stub) Future {user_name}: '{user_message}' — tell me more."

        # --- 5. RUN THE BLOCKING CALL IN A THREAD ---
        return await asyncio.to_thread(self._generate_sync, prompt)
