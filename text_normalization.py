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


def test_replace_punctuation_and_expand_abreviations():
    # I'll move this into a separate helper script at some point but for now I'm keeping it here
    test_cases = [
        # Common Abbreviations
        ("Dr. Smith is here.", "doctor smith is here [PERIOD_SILENCE]"),
        ("I.e., this is important.", "that is [COMMA_SILENCE] this is important [PERIOD_SILENCE]"),
        ("He is a prof. at the univ. Dept. of History.", "he is a professor at the univ [PERIOD_SILENCE] department of history [PERIOD_SILENCE]"),
        ("It's 9 A.M. sharp.", "it's 9 A M sharp [PERIOD_SILENCE]"),
        ("He lives at 123 Main St. NE.", "he lives at 123 main st [PERIOD_SILENCE] north east [PERIOD_SILENCE]"),
        ("The company, Inc. & Co. Ltd.", "the company [COMMA_SILENCE] incorporated and company limited"),
        ("approx. 10,000 ft.", "approximately 10000 feet"),
        ("No. 5 vs. No. 6", "number 5 versus number 6"),
        ("figure 2.5", "figure 2 point 5"), # Example of period as decimal, not end of sentence
        
        # Punctuation Replacement
        ("Hello, World!", "hello [COMMA_SILENCE] world [EXCLAMATION]"),
        ("Is this a test?", "is this a test [QUESTION]"),
        ("This is important...", "this is important dot dot dot"),
        ("List: item1; item2; item3.", "list colon item1 semi colon item2 semi colon item3 [PERIOD_SILENCE]"),
        ("It's a high-quality product.", "it's a high quality product [PERIOD_SILENCE]"),
        ("This is (a test).", "this is open parenthesis a test close parenthesis [PERIOD_SILENCE]"),
        ("He said, \"Hello!\"", "he said [COMMA_SILENCE] [QUOTE] hello [EXCLAMATION] [QUOTE]"),
        ("price: $500.00", "price colon dollar 500 point 00"), # Demonstrates $
        ("100% complete.", "100 percent complete [PERIOD_SILENCE]"),
        ("user@example.com", "user at example dot com"),
        ("File name: document-final.pdf", "file name colon document final dot pdf"), # Hyphen between words removed
        ("Here – is some text.", "here dash is some text [PERIOD_SILENCE]"), # En dash
        ("This is an em—dash.", "this is an em dash dash [PERIOD_SILENCE]"), # Em dash
        ("The value is x/y.", "the value is x slash y [PERIOD_SILENCE]"),
        ("A & B", "a and b"),
        ("Tag #new", "tag hashtag new"),
        ("This*is*important", "this asterisk is asterisk important"),

        # Mixed Cases
        ("Dr. Smith said, \"It's 2 P.M. vs. 3 P.M.\"", "doctor smith said [COMMA_SILENCE] [QUOTE] it's 2 P M versus 3 P M [QUOTE]"),
        ("He bought 10 lbs. of fruit.", "he bought 10 pounds of fruit [PERIOD_SILENCE]"),
        ("The address is 123 Main St. NW.", "the address is 123 main st [PERIOD_SILENCE] north west [PERIOD_SILENCE]"),
        ("Figure No. 1: (approx. 5ft. x 3in.).", "figure number 1 colon open parenthesis approximately 5 feet x 3 inches close parenthesis [PERIOD_SILENCE]"),
        ("Project [Alpha]. Phase II.", "project open bracket alpha close bracket [PERIOD_SILENCE] phase ii [PERIOD_SILENCE]"),
        ("What's up?", "what's up [QUESTION]"),
        ("Well, I suppose... yes!", "well [COMMA_SILENCE] i suppose dot dot dot yes [EXCLAMATION]"),
        ("The cost is $1,234.56. Only 50% left!", "the cost is dollar 1234 point 56 [PERIOD_SILENCE] only 50 percent left [EXCLAMATION]"),
        ("Call 1-800-ABC-DEF.", "call 1 800 abc def [PERIOD_SILENCE]"),
    ]

    for input_text, expected_output in test_cases:
        actual_output = replace_punctuation_and_expand_abreviations(input_text)
        print(f"Input:    '{input_text}'")
        print(f"Expected: '{expected_output}'")
        print(f"Actual:   '{actual_output}'")
        assert actual_output == expected_output, f"Test failed for input: '{input_text}'\nExpected: '{expected_output}', Got: '{actual_output}'"
        print("Test Passed!\n")

def main():
    test_replace_punctuation_and_expand_abreviations()


if __name__ == '__main__':
    main()