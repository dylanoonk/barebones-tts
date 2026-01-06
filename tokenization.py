class Token:
    def __init__(self, TEXT: str = "", IS_MODIFIER: bool = False, MODIFIES_PREVIOUS_TOKEN: bool = False, IS_SPEAKABLE: bool = False, SILENCE_TIME: float = 0.0, PITCH_MODIFIER: float = 0.0):
        self._text: str = TEXT.strip()
        self._is_modifier: bool = IS_MODIFIER
        self._is_speakable: bool = IS_SPEAKABLE

        if self._is_modifier:
            self._modifies_previous_token: bool = MODIFIES_PREVIOUS_TOKEN
            self._silence_time: float = SILENCE_TIME
            self._pitch_modifier: float = PITCH_MODIFIER
        pass

    def set_text(self, TEXT: str):
        self._text = TEXT
        
    def get_text(self) -> str:
        return self._text

    def set_modifier_flag(self, IS_MODIFIER: bool):
        self._is_modifier = IS_MODIFIER

    def get_modifier_flag(self) -> bool:
        return self._is_modifier

    def set_modifies_previous_token_flag(self, MODIFIES_PREVIOUS_TOKEN: bool):
        self._modifies_previous_token = MODIFIES_PREVIOUS_TOKEN

    def get_modifies_previous_token_flag(self) -> bool:
        return self._modifies_previous_token
    
    def set_silence_time(self, SILENCE_TIME: float):
            self._silence_time = SILENCE_TIME

    def get_silence_time(self) -> float:
        return self._silence_time

    def set_pitch_modifier(self, PITCH_MODIFIER: float):
            self._pitch_modifier = PITCH_MODIFIER

    def get_pitch_modifier(self) -> float:
        return self._pitch_modifier
    
    def set_speakable_flag(self, IS_SPEAKABLE: bool):
        self._is_speakable = IS_SPEAKABLE

    def get_speakable_flag(self) -> bool:
        return self._is_speakable

    
class TokenList:
    def __init__(self, input_data=None):

        if input_data is None:
            self._tokens: list[Token] = []
        elif isinstance(input_data, str): # check if it's a string
            self._tokens: list[Token] = self.list_to_tokens(input_data.split())
        elif isinstance(input_data, list): # check if it's a list of tokens
            if all(isinstance(item, Token) for item in input_data):
                self._tokens: list[Token] = input_data
            else: #it's probably a list of strings if it's not a list of tokens
                self._tokens: list[Token] = self.list_to_tokens(input_data) 
        else:
            raise TypeError("TokenList requires a string, list of strings, or list of Tokens")

    def __iter__(self):
        return iter(self._tokens)

    def list_to_tokens(self, LIST_OF_RAW_TEXT: list[str]) -> list[Token]:
        output_list: list[Token] = []

        for text in LIST_OF_RAW_TEXT:
            text_token = Token(TEXT=text)
            output_list.append(text_token)

        return output_list
    
    def to_dict_list(self):
        output_list = []

        for token in self._tokens:
            if token._is_modifier:
                output_list.append({'text': token._text, 'modifies_previous_token': token._modifies_previous_token, 'is_speakable': token._is_speakable, 'silence_time': token._silence_time, 'pitch_modifier': token._pitch_modifier})
            else:
                output_list.append({'text': token._text})
        return output_list
    
    def to_json(self):
        return self.to_dict_list()

    def __str__(self):
        return str(self.to_dict_list())
    
    def get(self, index: int) -> Token:
        TOKEN_LIST_SIZE: int = len(self._tokens)
        if index > TOKEN_LIST_SIZE or index < 0:
            raise IndexError(f"Attempted to access out of bounds token {index}")

        return self._tokens[index]
    
    def set(self, index: int, token: Token):
        TOKEN_LIST_SIZE: int = len(self._tokens)
        if index > TOKEN_LIST_SIZE + 1 or index < 0: # add one to token list size because in that case, it will just be appended at the end of the list
            raise IndexError(f"Attempted to access out of bounds token {index}")
        
        if index == TOKEN_LIST_SIZE + 1:
            self.append(token)
        else:
            self._tokens[index] = token

    def set_list(self, token_list: list[Token]):
        self._tokens = token_list

    def append(self, token: Token):
        self._tokens.append(token)









def main():
    tokens = TokenList("hello world")

    print(tokens)
if __name__ == "__main__":
    main()