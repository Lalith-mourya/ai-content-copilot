from abc import ABC, abstractmethod
from deep_translator import GoogleTranslator

class BaseTranslationService(ABC):
    @abstractmethod
    def translate(self, text: str, target_lang: str, source_lang: str = "auto") -> str:
        """
        Abstract method to translate text from source_lang to target_lang.
        """
        pass

class GoogleTranslationService(BaseTranslationService):
    def translate(self, text: str, target_lang: str, source_lang: str = "auto") -> str:
        """
        Translates text into the target language using deep-translator (Google Translate).
        Splits text by paragraphs to handle long chapters under API limitations.
        """
        # Map common languages to their ISO 639-1 language codes
        lang_map = {
            "tamil": "ta",
            "english": "en",
            "spanish": "es",
            "hindi": "hi",
            "french": "fr",
            "german": "de",
            "telugu": "te",
            "kannada": "kn"
        }
        
        target_code = lang_map.get(target_lang.lower(), target_lang.lower())
        source_code = lang_map.get(source_lang.lower(), source_lang.lower())
        
        if target_code == source_code:
            return text
            
        paragraphs = text.split("\n")
        translated_paragraphs = []
        
        translator = GoogleTranslator(source=source_code, target=target_code)
        
        for para in paragraphs:
            trimmed = para.strip()
            if not trimmed:
                translated_paragraphs.append("")
                continue
            
            try:
                # Handle large paragraphs by chunking
                if len(trimmed) > 4000:
                    chunks = [trimmed[i:i+4000] for i in range(0, len(trimmed), 4000)]
                    trans_chunks = [translator.translate(c) for c in chunks]
                    translated_paragraphs.append("".join(trans_chunks))
                else:
                    translated_paragraphs.append(translator.translate(trimmed))
            except Exception as e:
                # Log error and fall back to original text for this paragraph
                print(f"Translation error on paragraph: {e}")
                translated_paragraphs.append(para)
                
        return "\n".join(translated_paragraphs)
