"""ElevenLabs VO for Katha Deep. Voice: Rudra (matched to yesterday's episodes), model eleven_v3.
The API key is injected by the session's network proxy; the header value here is a placeholder.
usage: python3 tts.py PROJECT_DIR      -> vo/raw.mp3 + vo/alignment.json
"""
import base64, json, os, sys, urllib.request
VOICE = "vIdhHAZdn1bGjKe1dFw8"   # Rudra – Intense Documentary Narrator
MODEL = "eleven_v3"
d = sys.argv[1]
text = open(f"{d}/vo/script.txt").read().strip()
body = json.dumps({"text": text, "model_id": MODEL, "language_code": "hi",
                   "voice_settings": {"stability": 0.5}}).encode()
req = urllib.request.Request(
    f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE}/with-timestamps?output_format=mp3_44100_128",
    data=body, headers={"xi-api-key": os.environ.get("XI_API_KEY", "proxy-injected"), "Content-Type": "application/json"})
r = json.load(urllib.request.urlopen(req, timeout=600))
open(f"{d}/vo/raw.mp3", "wb").write(base64.b64decode(r["audio_base64"]))
json.dump(r.get("normalized_alignment") or r["alignment"], open(f"{d}/vo/alignment.json", "w"), ensure_ascii=False)
print(d, "ok")
