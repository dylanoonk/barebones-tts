from text_normalization import normalize_text
from arpabet import arpabetize
from formant_synth import FormantSynthesizer
from colorama import init, Fore

def speaking_loop(synth: FormantSynthesizer):
    input_text = input(f"{Fore.GREEN}> ").strip()
    normalized = normalize_text(input_text)
    print(f"{Fore.RESET}normalized: {Fore.CYAN}'{normalized}'")
    arpabetized = arpabetize(normalized)
    print(f"{Fore.RESET}arpabetized: {Fore.YELLOW}'{arpabetized}'")

    for token in arpabetized:
        TOKEN_TEXT = token.get_text()

        print(f"{Fore.RESET}speaking {Fore.LIGHTRED_EX}'{' '.join(TOKEN_TEXT)}'")
        audio = synth.synthesize(TOKEN_TEXT)
        synth.play(audio)

if __name__ == '__main__':
    init()
    synth: FormantSynthesizer = FormantSynthesizer()

    try:
        while True:
            speaking_loop(synth)
    except:
        print(f"{Fore.RESET}\nGoodbye.")
        exit()