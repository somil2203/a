import sys, json, subprocess, numpy as np
from faster_whisper import WhisperModel
from resemblyzer import VoiceEncoder, preprocess_wav
S="/tmp/claude-0/-home-user/2882668f-e38f-5e78-8827-1711ed8f9426/scratchpad"
L=lambda p,sr=16000: np.frombuffer(subprocess.run(["ffmpeg","-v","error","-i",p,"-ac","1","-ar",str(sr),"-f","f32le","-"],capture_output=True).stdout,np.float32)
enc=VoiceEncoder("cpu")
ref=np.mean([enc.embed_utterance(preprocess_wav(L(f"{S}/sep/clone_{v}.mp3"),16000)) for v in "BCD"],0); ref/=np.linalg.norm(ref)
m=WhisperModel("medium",device="cpu",compute_type="int8")
for p in sys.argv[1:]:
    a=L(f"{p}/vo/raw.mp3")
    sim=float(enc.embed_utterance(preprocess_wav(a,16000))@ref)
    segs,_=m.transcribe(a,language="hi",word_timestamps=True)
    segs=[{"s":s.start,"e":s.end,"t":s.text,"w":[(w.start,w.end,w.word) for w in s.words]} for s in segs]
    json.dump(segs,open(f"{p}/vo/whisper.json","w"),ensure_ascii=False)
    print(f"== {p} voice-sim {sim:.3f}")
    for s in segs: print(f"{s['s']:6.2f} {s['t']}")
