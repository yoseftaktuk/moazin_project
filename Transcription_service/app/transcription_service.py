import speech_recognition as sr
from logger import Logger

log = Logger.get_logger()
class TranscriptionService:
    def add_audio_to_str_to_metadata(self, data: dict):
      try:
        r = sr.Recognizer()
        print(data)
        with sr.AudioFile(data['matadata']['path']) as source:
            audio = r.record(source)
        data['string'] = r.recognize_sphinx(audio).lower()   
        log.info(f'convert audio to str') 
        return data 
      except sr.UnknownValueError as e:
          log.error(str(e))
          raise str(e)