import asyncio
from abc import ABC, abstractmethod
import edge_tts
from gtts import gTTS

class BaseTTSService(ABC):
    @abstractmethod
    async def synthesize(self, text: str, output_path: str, voice_gender: str = "female", language: str = "english") -> str:
        """
        Synthesizes text into speech and saves it as an MP3 file at output_path.
        Returns the output path on success.
        """
        pass

class EdgeTTSService(BaseTTSService):
    # Mapping of (language, gender) to Edge TTS neural voice IDs
    VOICE_MAP = {
        ("english", "female"): "en-US-AriaNeural",
        ("english", "male"): "en-US-GuyNeural",
        ("tamil", "female"): "ta-IN-PallaviNeural",
        ("tamil", "male"): "ta-IN-ValluvarNeural",
        ("hindi", "female"): "hi-IN-SwararaNeural",
        ("hindi", "male"): "hi-IN-MadhurNeural",
        ("spanish", "female"): "es-ES-ElviraNeural",
        ("spanish", "male"): "es-ES-AlvaroNeural",
        ("telugu", "female"): "te-IN-ShrutiNeural",
        ("telugu", "male"): "te-IN-MohanNeural",
    }
    
    async def synthesize(self, text: str, output_path: str, voice_gender: str = "female", language: str = "english") -> str:
        voice_key = (language.lower(), voice_gender.lower())
        # Default to AriaNeural (English Female) if no match found
        voice = self.VOICE_MAP.get(voice_key, "en-US-AriaNeural")
        
        try:
            communicate = edge_tts.Communicate(text, voice)
            await communicate.save(output_path)
            return output_path
        except Exception as e:
            print(f"EdgeTTS failed: {e}. Falling back to gTTS...")
            # Run blocking gTTS in executor to prevent event loop block
            loop = asyncio.get_event_loop()
            await loop.run_in_executor(None, self._run_gtts, text, output_path, language)
            return output_path
            
    def _run_gtts(self, text: str, output_path: str, language: str):
        lang_map = {
            "tamil": "ta",
            "english": "en",
            "hindi": "hi",
            "spanish": "es",
            "telugu": "te"
        }
        lang_code = lang_map.get(language.lower(), "en")
        tts = gTTS(text=text, lang=lang_code)
        tts.save(output_path)
