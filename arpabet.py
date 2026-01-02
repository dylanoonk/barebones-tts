from text_normalization import normalize_text
from tokenization import TokenList, Token
from formant_synth import FormantSynthesizer
import sqlite3


def arpabetize(tokens: TokenList, DB_FILE: str = 'pronunciation.db', sound_column: str = 'sound', word_column: str = 'word', table_name: str = 'pronunciations') -> TokenList:
    CONNECTION: sqlite3.Connection = sqlite3.connect(DB_FILE)
    CURSOR: sqlite3.Cursor = CONNECTION.cursor() 

    pronunciations: TokenList = TokenList()
    for token in tokens:
        if token.get_speakable_flag():
            pronunciation_token: Token = Token()

            TOKEN_TEXT = token.get_text().strip()
            query = f"SELECT {sound_column} FROM {table_name} WHERE {word_column} = ?"

            CURSOR.execute(query, (TOKEN_TEXT,))
            CONNECTION.commit()

            result = CURSOR.fetchone()
            
            if result == None:
                continue

            result = result[0].strip().split()
            pronunciation_token.set_text(result)
            
            pronunciations.append(pronunciation_token)



            
        
    return pronunciations


def main():
    synth = FormantSynthesizer()
    input_text = input('> ').strip()
    normalized = normalize_text(input_text)
    arpabetized = arpabetize(normalized)

    for token in arpabetized:
        TOKEN_TEXT = token.get_text()

        print(f"saying {' '.join(TOKEN_TEXT)}")
        audio = synth.synthesize(TOKEN_TEXT)
        synth.play(audio)
    main()


if __name__ == "__main__":
    try:
        main()
    except:
        exit()
