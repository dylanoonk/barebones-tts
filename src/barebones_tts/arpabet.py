from .text_normalization import normalize_text
from .tokenization import TokenList, Token
from colorama import Fore
from pickle import load
from pathlib import Path

DEFAULT_PRONUNCIATION_FILE = Path(__file__).parent / "data" / "pronunciation.pkl"

class arpabet:
    def __init__(self, pronunciation_file: str = str(DEFAULT_PRONUNCIATION_FILE)) -> None:
        with open(pronunciation_file, mode='rb') as f:
            self.PRONUNCIATIONS: dict[str, str] = load(f)
        
    def get_sound_from_db(self, TEXT: str) -> str | None:
        if TEXT in self.PRONUNCIATIONS:
            return self.PRONUNCIATIONS[TEXT]

        return None


    def fallback_pronunciation(self, TEXT: str) -> str:
        CHARACTERS: list[str] = list(TEXT.strip())
        output: list[str] = []

        for CHARACTER in CHARACTERS:
            sound = self.get_sound_from_db(CHARACTER.lower())
            if sound:
                output.append(sound)
            else:
                print(f"{Fore.RESET}{Fore.YELLOW}Unknown Character \"{CHARACTER.encode()}\"")

        if output:
            return " ".join(output).strip()
        
        return ""
        


    def arpabetize(self, tokens: TokenList, ) -> TokenList:
        pronunciations: TokenList = TokenList()
        for token in tokens:
            if token.get_speakable_flag():
                pronunciation_token: Token = Token()

                TOKEN_TEXT = token.get_text().strip().lower()
                
                sound = self.get_sound_from_db(TOKEN_TEXT)
                
                if sound == None:
                    sound = self.fallback_pronunciation(TOKEN_TEXT)

                sound = sound.split()
                pronunciation_token.set_text(TOKEN_TEXT)
                pronunciation_token.set_phoneme(sound)
                pronunciation_token.set_speakable_flag(True)
                
                pronunciations.append(pronunciation_token)
            else:
                pronunciations.append(token)


        return pronunciations


def main():
    arpa = arpabet()
    input_text = input('> ').strip()
    normalized = normalize_text(input_text)
    arpabetized = arpa.arpabetize(normalized)
    

    print(arpabetized)


if __name__ == "__main__":
    main()