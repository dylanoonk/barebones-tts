# Barebones Text To Speech

I wrote a text-to-speech system from first principles because I wanted to learn how old-timey text-to-speech systems worked. I'll make a video or something on how it works because there weren't any good in-depth videos about non-nueral-network text-to-speech systems.

## How to install

Use `pip` to install

```bash
pip install barebones-tts
```

## Start speaking

Literally just

```bash
python3 barebones-tts.py
```

...and start typing. This is still in early development so this will change soon to be better.

If you want to save the audio to a wav file then use the `--wav` or `-w` flags.

```bash
python3 barebones-tts.py --wav
```

Also, to use, just import like normal and start speaking:

```python
from barebones-tts import barebones_tts

barebones = barebones_tts()
barebones.speak("Hello world.")
```