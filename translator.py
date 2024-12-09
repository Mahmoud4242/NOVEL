# translator.py
from googletrans import Translator

class TextTranslator:
    def __init__(self, target_language='ar'):
        self.translator = Translator()
        self.target_language = target_language

    def translate(self, text):
        try:
            return self.translator.translate(text, dest=self.target_language).text
        except Exception as e:
            return f"Error in translation: {str(e)}"
