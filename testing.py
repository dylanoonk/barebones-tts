from colorama import Fore, init
from text_normalization import replace_punctuation_and_expand_abreviations
from text_normalization import numbers_to_words
from text_normalization import normalize_text, set_modifiers_from_table
from tokenization import TokenList, Token

import os


init()

def run_test(test_func, input_val, expected_output, test_name, DEBUG=False):
    actual_output = test_func(input_val)

    if DEBUG:
        print(f"{Fore.YELLOW}Input:    '{Fore.WHITE + str(input_val) + Fore.YELLOW}'")
        print(f"{Fore.YELLOW}Expected: '{Fore.WHITE + str(expected_output) + Fore.YELLOW}'")
        print(f"{Fore.YELLOW}Actual:   '{Fore.WHITE + str(actual_output) + Fore.YELLOW}'")

    if actual_output == expected_output:
        if DEBUG:
            print(f"{Fore.GREEN}Test \"{Fore.WHITE + str(input_val) + Fore.GREEN}\" Passed!")
            print(Fore.RESET + "-" * os.get_terminal_size().columns)
        return True
    else:
        print(f"\n\n{Fore.RED}Test failed for {test_name}: \"{Fore.WHITE + str(input_val) + Fore.RED}\"\nExpected: \"{Fore.WHITE + str(expected_output) + Fore.RED}\"\nGot: {' '* 5}\"{Fore.WHITE + str(actual_output) + Fore.RED}\"")
        print(Fore.RESET + "-" * os.get_terminal_size().columns)
        return False

def test_replace_punctuation_and_expand_abreviations(DEBUG=False):
    TEST_CASES = [ # test_case, expected, output
        # Common Abbreviations
        ("Dr. Smith is here.", "doctor smith is here [PERIOD_SILENCE]"),
        ("I.e., this is important.", "that is [COMMA_SILENCE] this is important [PERIOD_SILENCE]"),
        ("He is a prof. at the univ. Dept. of History.", "he is a professor at the univ [PERIOD_SILENCE] department of history [PERIOD_SILENCE]"),
        ("It's 9 A.M. sharp.", "it's 9 a m sharp [PERIOD_SILENCE]"),
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
        ("price: $500.00", "price colon 500 point 00 dollars"), # Demonstrates $
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
        ("Dr. Smith said, \"It's 2 P.M. vs. 3 P.M.\"", "doctor smith said [COMMA_SILENCE] [QUOTE] it's 2 p m versus 3 p m [QUOTE]"),
        ("He bought 10 lbs. of fruit.", "he bought 10 pounds of fruit [PERIOD_SILENCE]"),
        ("The address is 123 Main St. NW.", "the address is 123 main st [PERIOD_SILENCE] north west [PERIOD_SILENCE]"),
        ("Figure No. 1: (approx. 5ft. x 3in.).", "figure number 1 colon open parenthesis approximately 5 feet x 3 inches close parenthesis [PERIOD_SILENCE]"),
        ("Project [Alpha]. Phase II.", "project open bracket alpha close bracket [PERIOD_SILENCE] phase ii [PERIOD_SILENCE]"),
        ("What's up?", "what's up [QUESTION]"),
        ("Well, I suppose... yes!", "well [COMMA_SILENCE] i suppose dot dot dot yes [EXCLAMATION]"),
        ("The cost is $1,234.56. Only 50% left!", "the cost is 1234 point 56 dollars [PERIOD_SILENCE] only 50 percent left [EXCLAMATION]"),
        ("Call 1-800-ABC-DEF.", "call 1 800 abc def [PERIOD_SILENCE]"),
    ]

    print(f"\n{Fore.CYAN}--- Running replace_punctuation_and_expand_abreviations tests ---{Fore.RESET}")
    all_passed = True
    for input_text, expected_output in TEST_CASES:
        if not run_test(replace_punctuation_and_expand_abreviations, input_text, expected_output, "replace_punctuation_and_expand_abreviations", DEBUG):
            all_passed = False
    if all_passed:
        print(f"{Fore.GREEN}All Tests Passed For {Fore.WHITE}replace_punctuation_and_expand_abreviations(){Fore.RESET}")
    else:
        print(f"{Fore.RED}Some Tests Failed For {Fore.WHITE}replace_punctuation_and_expand_abreviations(){Fore.RESET}")


def test_numbers_to_words(DEBUG=False):
    TEST_CASES = [
        (0, ["zero"]),
        (1, ["one"]),
        (10, ["ten"]),
        (11, ["eleven"]),
        (19, ["nineteen"]),
        (20, ["twenty"]),
        (21, ["twenty", "one"]),
        (50, ["fifty"]),
        (99, ["ninety", "nine"]),
        (100, ["one", "hundred"]),
        (101, ["one", "hundred", "one"]),
        (115, ["one", "hundred", "fifteen"]),
        (200, ["two", "hundred"]),
        (999, ["nine", "hundred", "ninety", "nine"]),
        (1000, ["one", "thousand"]),
        (1001, ["one", "thousand", "one"]),
        (1200, ["one", "thousand", "two", "hundred"]),
        (1234, ["one", "thousand", "two", "hundred", "thirty", "four"]),
        (10000, ["ten", "thousand"]),
        (100000, ["one", "hundred", "thousand"]),
        (123456, ["one", "hundred", "twenty", "three", "thousand", "four", "hundred", "fifty", "six"]),
        (1000000, ["one", "million"]),
        (1000001, ["one", "million", "one"]),
        (1234567, ["one", "million", "two", "hundred", "thirty", "four", "thousand", "five", "hundred", "sixty", "seven"]),
        (123456789, ["one", "hundred", "twenty", "three", "million", "four", "hundred", "fifty", "six", "thousand", "seven", "hundred", "eighty", "nine"]),
        (1234567890, ["one", "billion", "two", "hundred", "thirty", "four", "million", "five", "hundred", "sixty", "seven", "thousand", "eight", "hundred", "ninety"]),
        (7000000, ["seven", "million"]),
        (80000, ["eighty", "thousand"]),
        (505, ["five", "hundred", "five"]),
        (7777, ["seven", "thousand", "seven", "hundred", "seventy", "seven"]),
        (9876543210, ["nine", "billion", "eight", "hundred", "seventy", "six", "million", "five", "hundred", "forty", "three", "thousand", "two", "hundred", "ten"]),
        (1000000000000, ["one", "trillion"]),
        (1000000000001, ["one", "trillion", "one"]),
        (2000000000000, ["two", "trillion"]),
    ]
    print(f"\n{Fore.CYAN}--- Running numbers_to_words tests ---{Fore.RESET}")
    all_passed = True
    for input_number, expected_output in TEST_CASES:
        if not run_test(numbers_to_words, input_number, expected_output, "numbers_to_words", DEBUG):
            all_passed = False
    if all_passed:
        print(f"{Fore.GREEN}All Tests Passed For {Fore.WHITE}numbers_to_words(){Fore.RESET}")
    else:
        print(f"{Fore.RED}Some Tests Failed For {Fore.WHITE}numbers_to_words(){Fore.RESET}")

def test_normalize_text(DEBUG=False):
    TEST_CASES = [
        ("Hello, world!", set_modifiers_from_table(TokenList([
            Token(TEXT='hello'),
            Token(TEXT='[COMMA_SILENCE]'),
            Token(TEXT='world'),
            Token(TEXT='[EXCLAMATION]')
        ])).to_json()),
        ("Dr. Smith said vs. Jones.", set_modifiers_from_table(TokenList([
            Token(TEXT='doctor'),
            Token(TEXT='smith'),
            Token(TEXT='said'),
            Token(TEXT='versus'),
            Token(TEXT='jones'),
            Token(TEXT='[PERIOD_SILENCE]')
        ])).to_json()),
        ("I have 123 apples and 4567 bananas.", set_modifiers_from_table(TokenList([
            Token(TEXT='i'),
            Token(TEXT='have'),
            Token(TEXT='one'),
            Token(TEXT='hundred'),
            Token(TEXT='twenty'),
            Token(TEXT='three'),
            Token(TEXT='apples'),
            Token(TEXT='and'),
            Token(TEXT='four'),
            Token(TEXT='thousand'),
            Token(TEXT='five'),
            Token(TEXT='hundred'),
            Token(TEXT='sixty'),
            Token(TEXT='seven'),
            Token(TEXT='bananas'),
            Token(TEXT='[PERIOD_SILENCE]')
        ])).to_json()),
        ("It costs $12.50 and $5.", set_modifiers_from_table(TokenList([
            Token(TEXT='it'),
            Token(TEXT='costs'),
            Token(TEXT='twelve'),
            Token(TEXT='point'),
            Token(TEXT='fifty'),
            Token(TEXT='dollars'),
            Token(TEXT='and'),
            Token(TEXT='five'),
            Token(TEXT='dollars'),
            Token(TEXT='[PERIOD_SILENCE]')
        ])).to_json()),
        ('She said, "Hello World" again.', set_modifiers_from_table(TokenList([
            Token(TEXT='she'),
            Token(TEXT='said'),
            Token(TEXT='[COMMA_SILENCE]'),
            Token(TEXT='quote'),
            Token(TEXT='hello'),
            Token(TEXT='world'),
            Token(TEXT='unquote'),
            Token(TEXT='again'),
            Token(TEXT='[PERIOD_SILENCE]')
        ])).to_json()),
        ("The price is $1,234.56. Is it 100% off?", set_modifiers_from_table(TokenList([
            Token(TEXT='the'),
            Token(TEXT='price'),
            Token(TEXT='is'),
            Token(TEXT='one'),
            Token(TEXT='thousand'),
            Token(TEXT='two'),
            Token(TEXT='hundred'),
            Token(TEXT='thirty'),
            Token(TEXT='four'),
            Token(TEXT='point'),
            Token(TEXT='fifty'),
            Token(TEXT='six'),
            Token(TEXT='dollars'),
            Token(TEXT='[PERIOD_SILENCE]'),
            Token(TEXT='is'),
            Token(TEXT='it'),
            Token(TEXT='one'),
            Token(TEXT='hundred'),
            Token(TEXT='percent'),
            Token(TEXT='off'),
            Token(TEXT='[QUESTION]')
        ])).to_json()),
        ("  Hello   world!  ", set_modifiers_from_table(TokenList([
            Token(TEXT='hello'),
            Token(TEXT='world'),
            Token(TEXT='[EXCLAMATION]')
        ])).to_json()),
        ("HeLLo wOrLd.", set_modifiers_from_table(TokenList([
            Token(TEXT='hello'),
            Token(TEXT='world'),
            Token(TEXT='[PERIOD_SILENCE]')
        ])).to_json()),
        ("", TokenList([]).to_json()),
        (".,!?", set_modifiers_from_table(TokenList([
            Token(TEXT='[PERIOD_SILENCE]'),
            Token(TEXT='[COMMA_SILENCE]'),
            Token(TEXT='[EXCLAMATION]'),
            Token(TEXT='[QUESTION]')
        ])).to_json()),
        ("It's 10 ft. long and 5 lbs. heavy.", set_modifiers_from_table(TokenList([
            Token(TEXT='it\'s'),
            Token(TEXT='ten'),
            Token(TEXT='feet'),
            Token(TEXT='long'),
            Token(TEXT='and'),
            Token(TEXT='five'),
            Token(TEXT='pounds'),
            Token(TEXT='heavy'),
            Token(TEXT='[PERIOD_SILENCE]')
        ])).to_json()),
        ("Go N. then SW.", set_modifiers_from_table(TokenList([
            Token(TEXT='go'),
            Token(TEXT='north'),
            Token(TEXT='then'),
            Token(TEXT='south'),
            Token(TEXT='west'),
            Token(TEXT='[PERIOD_SILENCE]')
        ])).to_json()),
        ("Acme Corp. and Inc. are here.", set_modifiers_from_table(TokenList([
            Token(TEXT='acme'),
            Token(TEXT='corporation'),
            Token(TEXT='and'),
            Token(TEXT='incorporated'),
            Token(TEXT='are'),
            Token(TEXT='here'),
            Token(TEXT='[PERIOD_SILENCE]')
        ])).to_json()),
        ("The meeting is at 9 a.m. sharp.", set_modifiers_from_table(TokenList([
            Token(TEXT='the'),
            Token(TEXT='meeting'),
            Token(TEXT='is'),
            Token(TEXT='at'),
            Token(TEXT='nine'),
            Token(TEXT='a'),
            Token(TEXT='m'),
            Token(TEXT='sharp'),
            Token(TEXT='[PERIOD_SILENCE]')
        ])).to_json()),
        ("The number is 1,234,567.", set_modifiers_from_table(TokenList([
            Token(TEXT='the'),
            Token(TEXT='number'),
            Token(TEXT='is'),
            Token(TEXT='one'),
            Token(TEXT='million'),
            Token(TEXT='two'),
            Token(TEXT='hundred'),
            Token(TEXT='thirty'),
            Token(TEXT='four'),
            Token(TEXT='thousand'),
            Token(TEXT='five'),
            Token(TEXT='hundred'),
            Token(TEXT='sixty'),
            Token(TEXT='seven'),
            Token(TEXT='[PERIOD_SILENCE]')
        ])).to_json()),
        ("Text [in brackets] and (in parentheses).", set_modifiers_from_table(TokenList([
            Token(TEXT='text'),
            Token(TEXT='open'),
            Token(TEXT='bracket'),
            Token(TEXT='in'),
            Token(TEXT='brackets'),
            Token(TEXT='close'),
            Token(TEXT='bracket'),
            Token(TEXT='and'),
            Token(TEXT='open'),
            Token(TEXT='parenthesis'),
            Token(TEXT='in'),
            Token(TEXT='parentheses'),
            Token(TEXT='close'),
            Token(TEXT='parenthesis'),
            Token(TEXT='[PERIOD_SILENCE]')
        ])).to_json()),
        ("Contact me @user #topic.", set_modifiers_from_table(TokenList([
            Token(TEXT='contact'),
            Token(TEXT='me'),
            Token(TEXT='at'),
            Token(TEXT='user'),
            Token(TEXT='hashtag'),
            Token(TEXT='topic'),
            Token(TEXT='[PERIOD_SILENCE]')
        ])).to_json()),
        ("file/path\\to\\file.", set_modifiers_from_table(TokenList([
            Token(TEXT='file'),
            Token(TEXT='slash'),
            Token(TEXT='path'),
            Token(TEXT='back'),
            Token(TEXT='slash'),
            Token(TEXT='to'),
            Token(TEXT='back'),
            Token(TEXT='slash'),
            Token(TEXT='file'),
            Token(TEXT='[PERIOD_SILENCE]')
        ])).to_json()),
        ("a-b -- c—d–e", TokenList([
            Token(TEXT='a'),
            Token(TEXT='b'),
            Token(TEXT='dash'),
            Token(TEXT='c'),
            Token(TEXT='dash'),
            Token(TEXT='d'),
            Token(TEXT='dash'),
            Token(TEXT='e')
        ]).to_json()),
        ("A & B company.", set_modifiers_from_table(TokenList([
            Token(TEXT='a'),
            Token(TEXT='and'),
            Token(TEXT='b'),
            Token(TEXT='company'),
            Token(TEXT='[PERIOD_SILENCE]')
        ])).to_json()),
        ("one...two...", TokenList([
            Token(TEXT='one'),
            Token(TEXT='dot'),
            Token(TEXT='dot'),
            Token(TEXT='dot'),
            Token(TEXT='two'),
            Token(TEXT='dot'),
            Token(TEXT='dot'),
            Token(TEXT='dot')
        ]).to_json()),
        ("this is a normal sentence", TokenList([
            Token(TEXT='this'),
            Token(TEXT='is'),
            Token(TEXT='a'),
            Token(TEXT='normal'),
            Token(TEXT='sentence')
        ]).to_json()),
        ("Order 123!", set_modifiers_from_table(TokenList([
            Token(TEXT='order'),
            Token(TEXT='one'),
            Token(TEXT='hundred'),
            Token(TEXT='twenty'),
            Token(TEXT='three'),
            Token(TEXT='[EXCLAMATION]')
        ])).to_json()),
        ("(100)", TokenList([
            Token(TEXT='open'),
            Token(TEXT='parenthesis'),
            Token(TEXT='one'),
            Token(TEXT='hundred'),
            Token(TEXT='close'),
            Token(TEXT='parenthesis')
        ]).to_json()),
    ]
    print(f"\n{Fore.CYAN}--- Running normalize_text tests ---{Fore.RESET}")
    all_passed = True
    for input_text, expected_output in TEST_CASES:
        # Wrap normalize_text to return JSON for comparison
        actual_output = normalize_text(input_text).to_json()
        if not run_test(lambda x: normalize_text(x).to_json(), input_text, expected_output, "normalize_text", DEBUG):
            all_passed = False
    if all_passed:
        print(f"{Fore.GREEN}All Tests Passed For {Fore.WHITE}normalize_text(){Fore.RESET}")
    else:
        print(f"{Fore.RED}Some Tests Failed For {Fore.WHITE}normalize_text(){Fore.RESET}")



def main():
    test_replace_punctuation_and_expand_abreviations(DEBUG=False)
    test_numbers_to_words(DEBUG=False)
    test_normalize_text(DEBUG=False)

if __name__ == "__main__":
    main()