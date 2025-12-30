class ModifierError(Exception):
    """
    Raised when if a modifier-only variable is set on a non-modifier token
    """
    pass

class Token:
    def __init__(self, TEXT: str, IS_MODIFIER: bool = False, SILENCE_TIME: float = 0.0, PITCH_MODIFIER: float = 0.0):
        self.text: str = TEXT.strip()
        self.is_modifier: bool = IS_MODIFIER

        if self.is_modifier:
            self.silence_time: float = SILENCE_TIME
            self.pitch_modifier: float = PITCH_MODIFIER
        pass

    def set_text(self, TEXT: str):
        self.text = TEXT

    def set_modifier_flag(self, IS_MODIFIER: bool):
        self.is_modifier = IS_MODIFIER
    
    def set_silence_time(self, SILENCE_TIME: float):
        if self.is_modifier:
            self.silence_time = SILENCE_TIME
        else:
            raise ModifierError("Cannot set a modifier-only flag on a non-modifier token")

    def set_pitch_modifier(self, PITCH_MODIFIER: float):
        if self.is_modifier:
            self.pitch_modifier = PITCH_MODIFIER
        else:
            raise ModifierError("Cannot set a modifier-only flag on a non-modifier token")

class Tokenization:
    def __init__(self, RAW_TEXT: str):
        self.tokens = self.list_to_tokens(RAW_TEXT.split())

    def __iter__(self):
        return iter(self.tokens)

    def list_to_tokens(self, LIST_OF_RAW_TEXT: list[str]) -> list[Token]:
        MODIFIER_TABLE = { # MODIFIER_NAME: [SILENCE_TIME (ms), PITCH_MODIFIER (%)]
            '[PERIOD_SILENCE]': [300.0, 0.0],
            '[COMMA_SILENCE]': [190.0, 0.0],
            '[QUESTION]': [280.0, 20.0],
            '[EXCLAMATION]': [280.0, 5.0],
            '[QUOTE]': [0.0, 0.0], # All quotes will be removed and replaced with proper words during normalization
        }
        output_list: list[Token] = []

        for text in LIST_OF_RAW_TEXT:
            text_token = Token(text)

            if text in MODIFIER_TABLE:
                text_token.is_modifier = True
                text_token.set_silence_time(MODIFIER_TABLE[text][0])
                text_token.set_pitch_modifier(MODIFIER_TABLE[text][1])
    
            output_list.append(text_token)

        return output_list
    
    def to_dict_list(self):
        output_list = []

        for token in self.tokens:
            if token.is_modifier:
                output_list.append({'text': token.text, 'silence_time': token.silence_time, 'pitch_modifier': token.pitch_modifier})
            else:
                output_list.append({'text': token.text})
        return output_list

    def __str__(self):
        return str(self.to_dict_list())




def main():
    tokens = Tokenization("hello world")

    print(tokens)
if __name__ == "__main__":
    main()