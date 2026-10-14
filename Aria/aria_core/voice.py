import asyncio, tempfile, os
import edge_tts, pygame, keyboard
import speech_recognition as sr
import sys
sys.path.insert(0, "F:\\Aria")
from config import TTS_VOICE

class Voice:
    def __init__(self):
        pygame.mixer.init()
        self.recognizer = sr.Recognizer()
        self.mic = sr.Microphone()

    def listen(self, timeout=8, phrase_limit=10):
        with self.mic as source:
            self.recognizer.adjust_for_ambient_noise(source, duration=0.3)
            try:
                audio = self.recognizer.listen(
                    source, timeout=timeout, phrase_time_limit=phrase_limit)
                return self.recognizer.recognize_google(audio)
            except Exception:
                return ""

    async def _speak_async(self, text):
        tmp = tempfile.mktemp(suffix=".mp3")
        try:
            communicate = edge_tts.Communicate(text, TTS_VOICE)
            await communicate.save(tmp)
            pygame.mixer.music.load(tmp)
            pygame.mixer.music.play()
            while pygame.mixer.music.get_busy():
                if keyboard.is_pressed("space"):
                    pygame.mixer.music.stop()
                    break
                await asyncio.sleep(0.05)
            pygame.mixer.music.unload()
        finally:
            try:
                os.remove(tmp)
            except:
                pass

    def speak(self, text):
        print(f"Aria: {text}")
        asyncio.run(self._speak_async(text))