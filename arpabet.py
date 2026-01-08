from text_normalization import normalize_text
from tokenization import TokenList, Token
from formant_synth import FormantSynthesizer
from colorama import Fore
import sqlite3

def get_sound_from_db(WORD: str, CONNECTION: sqlite3.Connection, CURSOR: sqlite3.Cursor, sound_column: str = 'sound', word_column: str = 'word', table_name: str = 'pronunciations') -> str | None:
    QUERY = f"SELECT {sound_column} FROM {table_name} WHERE {word_column} = ?"
    CURSOR.execute(QUERY, (WORD,))
    CONNECTION.commit()

    result = CURSOR.fetchone()

    if result == None:
        return None
    
    result = result[0].strip()
    return result

def fallback_pronunciation(TEXT: str, CONNECTION: sqlite3.Connection, CURSOR: sqlite3.Cursor) -> str:
    CHARACTERS: list[str] = list(TEXT.strip())
    output: list[str] = []

    for CHARACTER in CHARACTERS:
        sound = get_sound_from_db(CHARACTER.lower(), CONNECTION, CURSOR)
        if sound:
            output.append(sound)
        else:
            print(f"{Fore.RESET}{Fore.YELLOW}Unknown Character \"{CHARACTER.encode()}\"")

    if output:
        return " ".join(output).strip()
    
    return ""
    


def arpabetize(tokens: TokenList, DB_FILE: str = 'pronunciation.db') -> TokenList:
    CONNECTION: sqlite3.Connection = sqlite3.connect(DB_FILE)
    CURSOR: sqlite3.Cursor = CONNECTION.cursor() 

    pronunciations: TokenList = TokenList()
    for token in tokens:
        if token.get_speakable_flag():
            pronunciation_token: Token = Token()

            TOKEN_TEXT = token.get_text().strip().lower()
            
            sound = get_sound_from_db(TOKEN_TEXT, CONNECTION, CURSOR)
            
            if sound == None:
                sound = fallback_pronunciation(TOKEN_TEXT, CONNECTION, CURSOR)

            sound = sound.split()
            pronunciation_token.set_text(sound)
            pronunciation_token.set_speakable_flag(True)
            
            pronunciations.append(pronunciation_token)
        else:
            pronunciations.append(token)

    CONNECTION.close()

    return pronunciations


def main():
    synth = FormantSynthesizer()
    input_text = input('> ').strip()
    normalized = normalize_text(input_text)
    arpabetized = arpabetize(normalized)

    print(arpabetized)


if __name__ == "__main__":
    main()