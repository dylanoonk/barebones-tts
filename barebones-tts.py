from text_normalization import normalize_text
from tokenization import Token, TokenList
from arpabet import arpabetize
from formant_synth import FormantSynthesizer
from colorama import init, Fore

import numpy as np
import re
import sys

def sanitize_for_filename(input_string: str) -> str:
    s = input_string.strip()
    s = re.sub(r'[\s-]+', '_', s)
    s = re.sub(r'[<>:"/\\|?*]', '', s)
    s = s.strip('._')

    if not s:
        return "unnamed_file"

    return s

def speaking_loop(synth: FormantSynthesizer, save_to_file=False):
    input_text = input(f"{Fore.GREEN}> ").strip()
    normalized = normalize_text(input_text)
    print(f"{Fore.RESET}normalized: {Fore.CYAN}'{normalized}'")
    arpabetized = arpabetize(normalized)
    print(f"{Fore.RESET}arpabetized: {Fore.YELLOW}'{arpabetized}'")

    audios = []

    for index, token in enumerate(arpabetized):
        if token.get_speakable_flag():
            TOKEN_TEXT = token.get_text()

            #print(f"{Fore.RESET}speaking {Fore.LIGHTRED_EX}'{' '.join(TOKEN_TEXT)}'")
            audio = synth.synthesize(TOKEN_TEXT)
            silence = synth.generate_silence(100)
            audio = np.concatenate([audio, silence])
            #synth.play(audio)
        else:
            """
            if token.get_modifies_previous_token_flag() and index > 0:
                previous_audio = audios[index - 1]
                previous_audio = synth.pitch_shift(previous_audio, token.get_pitch_modifier())

            else:
                silence_time = synth.generate_silence(token.get_silence_time())
                audio = silence_time
            """

            audio = synth.generate_silence(500)

        audios.append(audio)

    print(f"{Fore.RESET}{Fore.BLUE}Playing...")
    complete_audio = np.concatenate(audios)
    synth.play(complete_audio)

    if save_to_file:
        filename = f'{sanitize_for_filename(input_text)}.wav'
        # print(f"{Fore.RESET}Saving as {Fore.GREEN}'{filename}'")
        synth.save_wav(complete_audio, filename)



    

if __name__ == '__main__':
    init()
    synth: FormantSynthesizer = FormantSynthesizer()
    save_to_file = True if '--wav' in sys.argv or '-w' in sys.argv else False
    try:
        while True:
            speaking_loop(synth, save_to_file=save_to_file)
    except:
        print(f"{Fore.RESET}\nGoodbye.")
        exit()