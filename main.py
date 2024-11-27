# type: ignore
import whisper
# import openai
from api_key import API_KEY
import requests
import json
from pytubefix import YouTube
from pathlib import Path, PurePath


# Download audio from video
link = input("Digite a url de um vídeo do youtube:")
video = YouTube(link)
stream = video.streams.get_audio_only().download()
filename = Path.home() / stream
audio_name = PurePath(filename).name

# transcription
model = whisper.load_model("base")
transcription = model.transcribe(audio_name)
# print(transcription["text"])

# analiser
headers = {
    "Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"
}
id_model = "gpt-4o-mini"
link = "https://api.openai.com/v1/chat/completions"
body_message = {
    "model": "gpt-4o-mini",
    "messages": [
        {
            "role": "user",
            "content": f"Descreva o seguinte vídeo {transcription}"
        }
    ]
}

body_message = json.dumps(body_message)
requisition = requests.post(link, headers=headers, data=body_message)
# print(requisition)
answer = requisition.json()
message = answer["choices"][0]["message"]["content"]
print(message)
