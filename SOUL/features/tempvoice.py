import requests
import sys
import os
from dotenv import load_dotenv
from pydub import AudioSegment
from pydub.playback import play
import io

# Force ffmpeg path
AudioSegment.converter = r"C:\Program Files\ffmpeg-7.1.1-full_build\bin\ffmpeg.exe"

# Load environment variables
load_dotenv()
API_KEY = os.getenv("ELEVENLABS_API_KEY")
DEFAULT_VOICE = "Xb7hH8MSUJpSbSDYk0k2"
DEFAULT_MODEL = "eleven_monolingual_v1"

def text_to_speech(text, voice_id=DEFAULT_VOICE, model_id=DEFAULT_MODEL):
    """Convert text to speech using ElevenLabs API and return audio bytes"""
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"

    headers = {
        "xi-api-key": API_KEY,
        "Content-Type": "application/json",
        "accept": "audio/mpeg"
    }

    data = {
        "text": text,
        "model_id": model_id,
        "voice_settings": {
            "stability": 0.5,
            "similarity_boost": 0.75
        }
    }

    try:
        response = requests.post(url, headers=headers, json=data, timeout=10)
        response.raise_for_status()
        return True, response.content
    except requests.exceptions.RequestException as e:
        return False, f"API Error: {str(e)}"
    except Exception as e:
        return False, f"General Error: {str(e)}"

def play_audio_bytes(audio_data):
    """Play audio data directly from memory without saving"""
    try:
        # Load audio from memory buffer
        audio_segment = AudioSegment.from_file(io.BytesIO(audio_data), format="mp3")
        play(audio_segment)
        return True, "Playback completed"
    except Exception as e:
        return False, f"Playback Error: {str(e)}"

def main():
    if not API_KEY:
        print("❌ Error: API key not found. Please set ELEVENLABS_API_KEY in your .env file.")
        sys.exit(1)

    print("🎤 Enter text to speak (type 'exit' to quit):")

    while True:
        text = input(" Your input: ").strip()
        if text.lower() == "exit":
            print("👋 Exiting.")
            break
        if not text:
            print("⚠️ Please enter some text.")
            continue

        # Convert to speech
        success, result = text_to_speech(text)
        if not success:
            print(f"❌ Error: {result}")
            continue

        print("🔊 Playing audio...")
        success, message = play_audio_bytes(result)
        print("✅ " + message if success else "❌ " + message)

if __name__ == "__main__":
    main()
