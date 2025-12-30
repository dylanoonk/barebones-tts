import re

# I moved these out here to keep from having to recomile all of the regexs everytime the replace_punctuation_and_expand_abreviations() runs

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
    
    # Remove commas in numbers
    (re.compile(r'(?<=\d),(?=\d)'), ''),

    (re.compile(r'(?<=\d)\.(?=\d)'), ' point '),
    (re.compile(r'(?<=\w)\.(?=\w)'), ' dot '),
      
]
    
PUNCTUATION_REPLACEMENT_RULES = [
    # These two have to run first to avoid some edge cases where they replace some of the tokens
    (re.compile(r'\[',), ' open bracket '),
    (re.compile(r'\]'), ' close bracket '),

    # Ellipsis (must come before single period)
    (re.compile(r'\.\.\.'), ' dot dot dot '),
    
    # Sentence endings
    (re.compile(r'\.'), ' [PERIOD_SILENCE] '),
    (re.compile(r'\?'), ' [QUESTION] '),
    (re.compile(r'!'), ' [EXCLAMATION] '),
    
    # Pauses
    (re.compile(r','), ' [COMMA_SILENCE]'),
    (re.compile(r':'), ' colon '),
    (re.compile(r';'), ' semi colon '),
    
    # Dashes and hyphens
    (re.compile(r'—'), ' dash '),  # em dash
    (re.compile(r'–'), ' dash '),  # en dash
    (re.compile(r'(?<=\w)-(?=\w)'), ' '),  # hyphen between words (remove)
    (re.compile(r'(?<=\s)-(?=\s)'), ' dash '),  # spaced dash
    
    # Parentheses and brackets
    (re.compile(r'\('), ' open parenthesis '),
    (re.compile(r'\)'), ' close parenthesis '),

    
    (re.compile(r'"'), ' [QUOTE] '),
    
    # Slashes
    (re.compile(r'/'), ' slash '),
    (re.compile(r'\\'), ' back slash'),
    
    # Ampersand
    (re.compile(r'&'), ' and '),
    
    # At symbol
    (re.compile(r'@'), ' at '),
    
    # Hashtag
    (re.compile(r'#'), ' hashtag '),
    
    # Dollar sign
    (re.compile(r'\$'), ' dollar '),
    
    # Percent sign
    (re.compile(r'%'), ' percent '),
    
    # Asterisk
    (re.compile(r'\*'), ' asterisk '),
]

def numbers_to_words(number: int) -> str:
    """
    Okay this is sorta shitass but it takes in an integer and returns the word version of that integer.
    
    :param int number: The number you want to turn into words
    :return: The number specified in word form
    :rtype: str
    
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
        return "zero"
    
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

    return " ".join(reversed(words)).strip()

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

    text = re.sub(re.compile(r'\s+'), ' ', text).strip()

    return text
    

def normalize_text(text):
    text = str.lower(text)

    return text




def main():
    pass


if __name__ == '__main__':
    main()