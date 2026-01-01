class ModifierError(Exception):
    """
    Raised if a modifier-only attribute is attempted to be set on a non-modifier token
    """
    pass

class Token:
    def __init__(self, TEXT: str = "", IS_MODIFIER: bool = False, MODIFIES_PREVIOUS_TOKEN: bool = False, SILENCE_TIME: float = 0.0, PITCH_MODIFIER: float = 0.0):
        self.text: str = TEXT.strip()
        self.is_modifier: bool = IS_MODIFIER

        if self.is_modifier:
            self.modifies_previous_token: bool = MODIFIES_PREVIOUS_TOKEN
            self.silence_time: float = SILENCE_TIME
            self.pitch_modifier: float = PITCH_MODIFIER
        pass

    def set_text(self, TEXT: str):
        self.text = TEXT
        
    def get_text(self) -> str:
        return self.text

    def set_modifier_flag(self, IS_MODIFIER: bool):
        self.is_modifier = IS_MODIFIER

    def get_modifier_flag(self) -> bool:
        return self.is_modifier

    def set_modifies_previous_token_flag(self, MODIFIES_PREVIOUS_TOKEN: bool):
        self.modifies_previous_token = MODIFIES_PREVIOUS_TOKEN

    def get_modifies_previous_token_flag(self) -> bool:
        return self.modifies_previous_token
    
    def set_silence_time(self, SILENCE_TIME: float):
        if self.is_modifier:
            self.silence_time = SILENCE_TIME
        else:
            raise ModifierError("Cannot set a modifier-only flag on a non-modifier token")

    def get_silence_time(self) -> float:
        return self.silence_time

    def set_pitch_modifier(self, PITCH_MODIFIER: float):
        if self.is_modifier:
            self.pitch_modifier = PITCH_MODIFIER
        else:
            raise ModifierError("Cannot set a modifier-only flag on a non-modifier token")

    def get_pitch_modifier(self) -> float:
        return self.pitch_modifier

    
class TokenList:
    def __init__(self, input_data=None):

        if input_data is None:
            self.tokens = []
        elif isinstance(input_data, str): # check if it's a string
            self.tokens = self.list_to_tokens(input_data.split())
        elif isinstance(input_data, list): # check if it's a list of tokens
            if all(isinstance(item, Token) for item in input_data):
                self.tokens = input_data
            else: #it's probably a list of strings if it's not a list of tokens
                self.tokens = self.list_to_tokens(input_data) 
        else:
            raise TypeError("TokenList requires a string, list of strings, or list of Tokens")

    def __iter__(self):
        return iter(self.tokens)

    def list_to_tokens(self, LIST_OF_RAW_TEXT: list[str]) -> list[Token]:
        output_list: list[Token] = []

        for text in LIST_OF_RAW_TEXT:
            text_token = Token(TEXT=text)
            output_list.append(text_token)

        return output_list
    
    def to_dict_list(self):
        output_list = []

        for token in self.tokens:
            if token.is_modifier:
                output_list.append({'text': token.text, 'modifies_previous_token': token.modifies_previous_token, 'silence_time': token.silence_time, 'pitch_modifier': token.pitch_modifier})
            else:
                output_list.append({'text': token.text})
        return output_list
    
    def to_json(self):
        return self.to_dict_list()

    def __str__(self):
        return str(self.to_dict_list())






def main():
    tokens = TokenList("hello world")

    print(tokens)
if __name__ == "__main__":
    main()