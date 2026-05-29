from elevenlabs.client import ElevenLabs
from config import settings

client = ElevenLabs(api_key=settings.ELEVENLABS_API_KEY)

def text_to_speech(text: str, voice_id: str = "s3TPKV1kjDlVtZbl4Ksh") -> bytes:
    audio_generator = client.text_to_speech.convert(
        text=text,
        voice_id=voice_id,
        model_id="eleven_multilingual_v2"
    )
    audio_bytes = b"".join(audio_generator)
    return audio_bytes