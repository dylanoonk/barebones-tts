import re
from tokenization import TokenList, Token
# I moved these out here to keep from having to recompile all of the regexs everytime the replace_punctuation_and_expand_abreviations() runs

COMMON_REPLACEMENT_RULES = [
    # Titles
    (re.compile(r'\bmr\.'), 'mister'),
    (re.compile(r'\bmrs\.'), 'missus'),
    (re.compile(r'\bms\.'), 'miss'),
    (re.compile(r'\bdr\.'), 'doctor'),
    (re.compile(r'\bprof\.'), 'professor'),
    (re.compile(r'\brev\.'), 'reverend'),
    (re.compile(r'\bgen\.'), 'general'),
    (re.compile(r'\bsen\.'), 'senator'),
    (re.compile(r'\brep\.'), 'representative'),
    (re.compile(r'\bgov\.'), 'governor'),
    (re.compile(r'\bcol\.'), 'colonel'),
    (re.compile(r'\bcapt\.'), 'captain'),
    
    # Common abbreviations
    (re.compile(r'\be\.g\.'), 'for example'),
    (re.compile(r'\bi\.e\.'), 'that is'),
    (re.compile(r'\betc\.'), 'et cetera'),
    (re.compile(r'\bvs\.'), 'versus'),
    (re.compile(r'\bvs\b'), 'versus'),
    (re.compile(r'\bet al\.'), 'and others'),
    (re.compile(r'\bapprox\.'), 'approximately'),
    (re.compile(r'\bdept\.'), 'department'),
    (re.compile(r'\bfig\.'), 'figure'),
    (re.compile(r'\bno\.'), 'number'),
    (re.compile(r'\bpg\.'), 'page'),
    (re.compile(r'\bvol\.'), 'volume'),
    (re.compile(r'\bch\.'), 'chapter'),
    (re.compile(r'\bsec\.'), 'section'),
    
    # Time
    (re.compile(r'\b(a\.m\.|am)'), 'A M'),
    (re.compile(r'\b(p\.m\.|pm)'), 'P M'),
    
    # Units (avoiding numbers)
    (re.compile(r'(?<=\d)\s*ft\.'), ' feet'),
    (re.compile(r'(?<=\d)\s*in\.'), ' inches'),
    (re.compile(r'(?<=\d)\s*lb\.'), ' pounds'),
    (re.compile(r'(?<=\d)\s*lbs\.'), ' pounds'),
    (re.compile(r'(?<=\d)\s*oz\.'), ' ounces'),
    
    # Organizations
    (re.compile(r'\bcorp\.'), 'corporation'),
    (re.compile(r'\bco\.'), 'company'),
    (re.compile(r'\binc\.'), 'incorporated'),
    (re.compile(r'\bltd\.'), 'limited'),
    (re.compile(r'\bl\.l\.c\.'), 'L L C'),
    
    # Directions
    (re.compile(r'\bn\.'), 'north'),
    (re.compile(r'\bs\.'), 'south'),
    (re.compile(r'\be\.'), 'east'),
    (re.compile(r'\bw\.'), 'west'),
    (re.compile(r'\bne\b'), 'north east'),
    (re.compile(r'\bnw\b'), 'north west'),
    (re.compile(r'\bse\b'), 'south east'),
    (re.compile(r'\bsw\b'), 'south west'),
      
]
    
PUNCTUATION_REPLACEMENT_RULES = [
    # These three have to run first to avoid some edge cases where they replace some of the tokens
    (re.compile(r'\[',), ' open bracket '),
    (re.compile(r'\]'), ' close bracket '),
    (re.compile(r'(?<=\d),(?=\d)'), ''), # Remove commas in numbers

    # Dollar sign 
    (re.compile(r'\$(\d+(?:\.\d+)?)'), r'\1$'), # Swaps around the dollar sign to the end
    (re.compile(r'(?<!\d)\$(?!\d)'), ' dollar sign '),

    # Dots
    (re.compile(r'\.\.\.'), ' dot dot dot '),
    (re.compile(r'(?<=\d)\.(?=\d)'), ' point '),
    (re.compile(r'(?<=\w)\.(?=\w)'), ' dot '),
    
    (re.compile(r'(\d+)\$'), r'\1 dollars '),

    # Sentence endings
    (re.compile(r'\.'), ' [PERIOD_SILENCE] '),
    (re.compile(r'\?'), ' [QUESTION] '),
    (re.compile(r'!'), ' [EXCLAMATION] '),
    
    # Pauses
    (re.compile(r','), ' [COMMA_SILENCE] '),
    (re.compile(r':'), ' colon '),
    (re.compile(r';'), ' semi colon '),
    
    # Dashes and hyphens
    (re.compile(r'—'), ' dash '),  # em dash
    (re.compile(r'–'), ' dash '),  # en dash
    (re.compile(r'--'), ' dash '),
    (re.compile(r'(?<=\w)-(?=\w)'), ' '),  # hyphen between words (remove)
    (re.compile(r'(?<=\s)-(?=\s)'), ' dash '),  # spaced dash
    
    # Parentheses and brackets
    (re.compile(r'\('), ' open parenthesis '),
    (re.compile(r'\)'), ' close parenthesis '),

    
    (re.compile(r'"'), ' [QUOTE] '),
    
    # Slashes
    (re.compile(r'/'), ' slash '),
    (re.compile(r'\\'), ' back slash '),
    
    # Ampersand
    (re.compile(r'&'), ' and '),
    
    # At symbol
    (re.compile(r'@'), ' at '),
    
    # Hashtag
    (re.compile(r'#'), ' hashtag '),

    # Percent sign
    (re.compile(r'%'), ' percent '),
    
    # Asterisk
    (re.compile(r'\*'), ' asterisk '),
]

MULTIPLE_SPACES_PATTERN = re.compile(r'\s+')

def numbers_to_words(number: int) -> list[str]:
    """
    Okay this is sorta shitass but it takes in an integer and returns the word version of that integer.
    
    :param int number: The number you want to turn into words
    :return: The number specified in word form
    :rtype: list[str]
    
    For example:

    ```
    numbers_to_words(1234567890)
    ```

    returns

    ```
    one billion two hundred thirty four million five hundred sixty seven thousand eight hundred ninety
    ```


    """
    if number == 0:
        return ["zero"]
    
    def three_digits(NUMBER):
        ONES = ["", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine", "ten", "eleven", "twelve", "thirteen", "fourteen", "fifteen", "sixteen", "seventeen", "eighteen", "nineteen"]
        TENS = ["", "", "twenty", "thirty", "forty", "fifty", "sixty", "seventy", "eighty", "ninety"]

        if NUMBER < 20:
            return ONES[NUMBER]
        elif NUMBER < 100:
            return TENS[NUMBER // 10] + ( " " + ONES[NUMBER % 10] if NUMBER % 10 != 0 else "")
        else:
            return ONES[NUMBER // 100] + " hundred" + (" " + three_digits(NUMBER % 100) if NUMBER % 100 != 0 else "")

    SCALES = ["", "thousand", "million", "billion", "trillion"]
    words = []

    for SCALE in SCALES:
        if number % 1000 != 0:
            words.append(three_digits(number % 1000) + (" " + SCALE if SCALE else ""))
        number //= 1000
        if number == 0:
            break

    return (" ".join(reversed(words)).strip()).split()


def replace_punctuation_and_expand_abreviations(text: str) -> str:
    """
    Replaces punctuation and expands abreviations into full words in the given text. This is a preprocessing step for the text normalization step. Needs to be run **BEFORE** tokenization.
    
    :param text: Text you want to expand
    :type text: str
    :return: Expanded text
    :rtype: str
    """
    text = str.lower(text)

    # I separated out COMMON_REPLACEMENT_RULES and PUNCTUATION_REPLACEMENT_RULES to avoid edge cases like "Hello, Dr. Oz. How are you?" 
    # being replaced with "hello [COMMA_SILENCE] dr [PERIOD_SILENCE] oz [PERIOD_SILENCE] how are you?" 
    # instead of the correct "hello [COMMA_SILENCE] doctor oz [PERIOD_SILENCE] how are you?"

    for pattern, replacement in COMMON_REPLACEMENT_RULES:
        text = pattern.sub(replacement, text)

    for pattern, replacement in PUNCTUATION_REPLACEMENT_RULES:
        text = pattern.sub(replacement, text)

    #text = re.sub(MULTIPLE_SPACES_PATTERN, ' ', text).strip()
    text = MULTIPLE_SPACES_PATTERN.sub(' ', text).strip()

    return text

def set_modifiers_from_table(tokens: TokenList) -> TokenList:
    MODIFIER_TABLE = { # MODIFIER_NAME: [SILENCE_TIME (ms), PITCH_MODIFIER (%), MODIFIES_PREVIOUS_TOKEN]
        '[PERIOD_SILENCE]': [300.0, 0.0, False],
        '[COMMA_SILENCE]': [190.0, 0.0, False],
        '[QUESTION]': [280.0, 20.0, True],
        '[EXCLAMATION]': [280.0, 5.0, True],
        '[QUOTE]': [0.0, 0.0, False], # All quotes will be removed and replaced with proper words during normalization
    }

    for token in tokens:
        text = token.get_text()

        if text in MODIFIER_TABLE:
            token.set_modifier_flag(True)
            token.set_silence_time(MODIFIER_TABLE[text][0])
            token.set_pitch_modifier(MODIFIER_TABLE[text][1])
            token.set_modifies_previous_token_flag(MODIFIER_TABLE[text][2])
        else:
            token.set_speakable_flag(True)

    return tokens



def normalize_text(text: str) -> TokenList:
    """
    Takes text and transforms it into a more speakable version of it (in token form)

    ## Example

    ```python
    normalize_text('she said, "Hello World" and that I owe her $123.')
    ```

    Returns a tokenized list that looks like this:

    ```python
    [{'text': 'she'}, {'text': 'said'}, {'text': '[COMMA_SILENCE]', 'modifies_previous_token': False, 'silence_time': 190.0, 'pitch_modifier': 0.0}, {'text': 'quote'}, {'text': 'hello'}, {'text': 'world'}, {'text': 'unquote'}, {'text': 'and'}, {'text': 'that'}, {'text': 'i'}, {'text': 'owe'}, {'text': 'her'}, {'text': 'one'}, {'text': 'hundred'}, {'text': 'twenty'}, {'text': 'three'}, {'text': 'dollars'}, {'text': '[PERIOD_SILENCE]', 'modifies_previous_token': False, 'silence_time': 300.0, 'pitch_modifier': 0.0}]
    ```
    
    :param text: Text to normalize
    :type text: str
    :return: Normalized text
    :rtype: TokenList
    """

    text = replace_punctuation_and_expand_abreviations(text)
    tokens = TokenList(text)

    expanded_tokens = []
    quote_opened = False

    for token in tokens:
        if token._text.isdigit():
            token_converted_to_words = numbers_to_words(int(token._text))
            for word in token_converted_to_words:
                expanded_tokens.append(Token(TEXT=word))
        elif token._text == '[QUOTE]':
            if not quote_opened:
                expanded_tokens.append(Token(TEXT='quote'))
            else:
                expanded_tokens.append(Token(TEXT='unquote'))

            quote_opened = not quote_opened
        else:
            expanded_tokens.append(token)

    tokens.set_list(expanded_tokens)

    tokens = set_modifiers_from_table(tokens)

    return tokens

def main():
    normalized_text = normalize_text('she said, "Hello World" and that I owe her $123.')
    print(normalized_text)


if __name__ == '__main__':
    main()