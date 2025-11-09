# app/services/elevenlabs_service.py

from elevenlabs.client import ElevenLabs
from elevenlabs import Voice, VoiceSettings
from app.config import get_settings
from io import BytesIO
import asyncio  # <-- 1. IMPORT ASYNCIO

class ElevenLabsService:
    def __init__(self):
        settings = get_settings()
        if not settings.elevenlabs_api_key:
            print("❌ ERROR: ELEVENLABS_API_KEY not set!")
            raise ValueError("ELEVENLABS_API_KEY not set")
            
        self.client = ElevenLabs(api_key=settings.elevenlabs_api_key)
        print("✅ ElevenLabs Service initialized.")

    async def clone_voice(self, audio_data: bytes, user_id: str) -> str:
        """
        Clones a user's voice from an audio file and returns the new voice_id.
        This is now non-blocking.
        """
        try:
            audio_file = BytesIO(audio_data)
            
            # --- 2. RUN THE BLOCKING CODE IN A SEPARATE THREAD ---
            voice = await asyncio.to_thread(
                self.client.voices.add,
                name=f"Ekho User - {user_id}",
                files=[audio_file],
                description=f"Voice clone for Ekho user {user_id}"
            )
            # --------------------------------------------------
            
            print(f"Cloned voice for user {user_id}. Voice ID: {voice.voice_id}")
            return voice.voice_id
            
        except Exception as e:
            print(f"❌ Failed to clone voice for user {user_id}: {e}")
            raise

    # --- 3. CREATE A SYNCHRONOUS HELPER FUNCTION ---
    # We put all the blocking logic in its own function.
    def _generate_speech_sync(self, text: str, voice_id: str) -> bytes:
        """
        Synchronous helper for audio generation.
        """
        try:
            voice_settings = VoiceSettings(
                stability=0.35,
                similarity_boost=0.75,
                style=0.2,
                use_speaker_boost=True
            )

            # This call blocks
            audio_chunks = self.client.text_to_speech.convert(
                voice_id=voice_id,
                text=text,
                model_id="eleven_multilingual_v2",
                voice_settings=voice_settings
            )

            # This call also blocks
            audio_bytes = b"".join(chunk for chunk in audio_chunks)
            
            print(f"Generated speech for voice_id {voice_id}")
            return audio_bytes
        except Exception as e:
            print(f"❌ Failed to generate speech for voice_id {voice_id}: {e}")
            raise

    async def generate_speech(self, text: str, voice_id: str) -> bytes:
        """
        Converts text to speech using a cloned voice.
        Returns full audio bytes, non-blocking.
        """
        # --- 4. RUN THE HELPER FUNCTION IN A THREAD ---
        return await asyncio.to_thread(
            self._generate_speech_sync,
            text,
            voice_id
        )