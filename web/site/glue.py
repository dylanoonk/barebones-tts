import struct
import time

import numpy as np

from barebones_tts import barebones_tts

tts = barebones_tts()


def _wav_bytes(audio: np.ndarray) -> bytes:
    pcm = np.int16(np.clip(audio, -1.0, 1.0) * 32767).tobytes()
    header = struct.pack(
        '<4sI4s4sIHHIIHH4sI',
        b'RIFF', 36 + len(pcm), b'WAVE',
        b'fmt ', 16, 1, 1,
        tts.synth.sample_rate, tts.synth.sample_rate * 2, 2, 16,
        b'data', len(pcm),
    )
    return header + pcm


def speak_wav(text: str) -> bytes:
    t0 = time.time()
    audio = tts.render(text)
    seconds = len(audio) / tts.synth.sample_rate
    print(
        f"rendered {seconds:.2f}s of audio in "
        f"{(time.time() - t0) * 1000:.0f} ms @ {tts.synth.sample_rate} Hz"
    )
    return _wav_bytes(audio)


def save_wav_file(text: str) -> list:
    t0 = time.time()
    filename = tts.save(text)
    with open(filename, 'rb') as f:
        data = f.read()
    seconds = (len(data) - 44) / 2 / tts.synth.sample_rate
    print(
        f"rendered {seconds:.2f}s of audio in "
        f"{(time.time() - t0) * 1000:.0f} ms @ {tts.synth.sample_rate} Hz"
    )
    return [filename, data]


print("synth online! type something and press SPEAK")
