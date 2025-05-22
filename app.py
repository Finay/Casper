from vosk import Model, KaldiRecognizer
import pyaudio
import json
import pyttsx3
from google import genai
from google.genai import types

client = genai.Client(api_key="AIzaSyCGDrg27fYDpwSOatRxcoqVMGlv9-gkgJI")
chat = client.chats.create(
    model="gemini-2.0-flash",
    config=types.GenerateContentConfig(
        system_instruction="You are a helpful chatbot named Rob. You return an empty string when you are not referenced."
    )
)

def transcribe_microphone_audio():
    # Load the Vosk model
    model = Model("model")
    recognizer = KaldiRecognizer(model, 16000)

    # Initialize PyAudio
    audio = pyaudio.PyAudio()
    stream = audio.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=8000)
    stream.start_stream()

    print("Listening for speech. Press Ctrl+C to stop.")
    tts_engine = pyttsx3.init()

    try:
        while True:
            print("Start data")
            data = stream.read(4000, exception_on_overflow=False)
            if recognizer.AcceptWaveform(data):
                result = json.loads(recognizer.Result())
                transcription = result.get("text", "")
                print("Transcription:", transcription)
                response = chat.send_message(transcription)

                if response.text:
                    print("Rob:", response.text)
                    tts_engine.say(response.text)
                    tts_engine.runAndWait()
    except KeyboardInterrupt:
        print("\nTranscription stopped by user.")
    finally:
        stream.stop_stream()
        stream.close()
        audio.terminate()

if __name__ == "__main__":
    transcribe_microphone_audio()
