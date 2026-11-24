import queue
import json
import sounddevice as sd
from vosk import Model, KaldiRecognizer

from src.config import VOSK_MODEL_PATH

# Load the speech recognition model
# Source: https://alphacephei.com/vosk/models
model = Model(str(VOSK_MODEL_PATH))

# Create recognizer
recognizer = KaldiRecognizer(model, 16000)

# Queue for microphone audio
audio_queue = queue.Queue()


def audio_callback(indata, frames, time, status):
    audio_queue.put(bytes(indata))


def listen():
    """analyze audio chunks to find beginning and end of speaking and return converted text"""

    print("Listening...")

    with sd.RawInputStream(
        samplerate=16000,
        blocksize=1600,
        dtype="int16",
        channels=1,
        callback=audio_callback
    ):
        while True:
            data = audio_queue.get()

            # check whether Vosk detected the end of a speech segment
            if recognizer.AcceptWaveform(data):
                result = json.loads(recognizer.Result())
                text = result["text"]

                # prompts must be longer than 10 characters to avoid random sounds being picked up
                if len(text) > 10:
                    return text
