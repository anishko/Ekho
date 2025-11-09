import os
from elevenlabs import ElevenLabs, play
from dotenv import load_dotenv

def main():
    load_dotenv()
    api_key = os.getenv("ELEVENLABS_API_KEY")
    if not api_key:
        print("❌ ELEVENLABS_API_KEY not found")
        return

    client = ElevenLabs(api_key=api_key)

    text_to_speak = "Hello! This is a test of ElevenLabs text to speech."
    voice_id = "21m00Tcm4TlvDq8ikWAM"  # Rachel

    # Save directly to Downloads folder
    downloads_path = os.path.join(os.path.expanduser("~"), "Downloads")
    output_path = os.path.join(downloads_path, "test_audio.mp3")
    print(f"💾 Saving directly to: {output_path}")

    # ✅ Open file first, then stream bytes directly into it
    try:
        with open(output_path, "wb") as f:
            # generator yields chunks; write each immediately
            for chunk in client.text_to_speech.convert(
                voice_id=voice_id,
                model_id="eleven_multilingual_v2",
                text=text_to_speak,
            ):
                f.write(chunk)
        print(f"✅ Audio saved successfully to: {output_path}")
    except Exception as e:
        print(f"❌ Failed to write file: {e}")
        return

    # Play audio from memory
    try:
        # Read the file again to play
        with open(output_path, "rb") as f:
            audio_bytes = f.read()
        play(audio_bytes)
        print("🔊 Played successfully.")
    except Exception as e:
        print(f"⚠️ Could not play audio: {e}")

if __name__ == "__main__":
    main()
