from text_normalization import normalize_text
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


def speak(input_text: str, synth: FormantSynthesizer = FormantSynthesizer(), save_to_file: bool = False, filename: str = "") -> str | None:
    """
    Speaks given text out loud (or saves to a file) the given English text 
    
    :param input_text: Text to be spoken
    :type input_text: str
    :param synth: Syntheizer object to use for synthesizing the phonemes into sound
    :type synth: FormantSynthesizer
    :param save_to_file: Flag for whether or play the sound out loud or save it to a file
    :type save_to_file: bool
    :param filename: File name for the wav file of the spoken text
    :type filename: str

    :return: Returns the filename (string) if save_to_file flag is set to True; otherwise returns nothing
    :rtype: str | None
    """

    normalized = normalize_text(input_text)
    print(f"{Fore.RESET}normalized: {Fore.CYAN}'{normalized}'")
    arpabetized = arpabetize(normalized)
    print(f"{Fore.RESET}arpabetized: {Fore.YELLOW}'{arpabetized}'")

    audios = []

    for index, token in enumerate(arpabetized):
        if token.get_speakable_flag():
            TOKEN_TEXT = token.get_text()

            audio = synth.synthesize(TOKEN_TEXT)
            silence = synth.generate_silence(100)
            audio = np.concatenate([audio, silence])
        elif token.get_modifies_previous_token_flag() and index > 0:
            
            audios[index - 1] = synth.pitch_shift(audios[index - 1], token.get_pitch_modifier())
            audio = synth.generate_silence(token.get_silence_time())
        else:
            audio = synth.generate_silence(token.get_silence_time())
        audios.append(audio)

    print(f"{Fore.RESET}{Fore.BLUE}Playing...")
    complete_audio = np.concatenate(audios)
    
    if not save_to_file:
        synth.play(complete_audio)
        return None

    
    if filename == "":
        filename = f'{sanitize_for_filename(input_text)}.wav'
    
    synth.save_wav(complete_audio, filename)
    return filename



    

if __name__ == '__main__':
    init()
    synth: FormantSynthesizer = FormantSynthesizer()
    save_to_file = True if '--wav' in sys.argv or '-w' in sys.argv else False

    try:
        while True:
            input_text = input(f"{Fore.GREEN}> ").strip()
            # set synth explicitly so it doesn't have to reinitialize over and over again
            speak(input_text, synth=synth, save_to_file=save_to_file)
    except KeyboardInterrupt:
        print(f"{Fore.RESET}\nGoodbye.")
        exit()