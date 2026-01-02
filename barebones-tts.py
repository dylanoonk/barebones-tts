from text_normalization import normalize_text
from arpabet import arpabetize
from formant_synth import FormantSynthesizer

def speaking_loop(synth: FormantSynthesizer):
    input_text = input('> ').strip()
    normalized = normalize_text(input_text)
    print(f"normalized: '{normalized}'")
    arpabetized = arpabetize(normalized)

    for token in arpabetized:
        TOKEN_TEXT = token.get_text()

        print(f"saying {' '.join(TOKEN_TEXT)}")
        audio = synth.synthesize(TOKEN_TEXT)
        synth.play(audio)

if __name__ == '__main__':
    synth: FormantSynthesizer = FormantSynthesizer()

    try:
        while True:
            speaking_loop(synth)
    except:
        print('Goodbye')
        exit()