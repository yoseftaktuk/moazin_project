import speech_recognition as sr
#pip install PocketSphinx
#pip install pyttsx3
#pip install speechrecognition
class AudioProcessor:
    def speech_to_text(self, audio_path: str) -> str:   
        r = sr.Recognizer()
        with sr.AudioFile(audio_path) as source:
            audio = r.record(source)
        return r.recognize_sphinx(audio).lower()

    