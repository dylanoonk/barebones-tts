from colorama import Fore, init
from text_normalization import replace_punctuation_and_expand_abreviations
from text_normalization import numbers_to_words
from formant_synth import FormantSynthesizer


init()

def test_replace_punctuation_and_expand_abreviations(DEBUG=False):
    TEST_CASES = [ # test_case, expected, output
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
        ("Dr. Smith said, \"It's 2 P.M. vs. 3 P.M.\"", "doctor smith said [COMMA_SILENCE] [QUOTE] it's 2 P M versus 3 P M [QUOTE]"),
        ("He bought 10 lbs. of fruit.", "he bought 10 pounds of fruit [PERIOD_SILENCE]"),
        ("The address is 123 Main St. NW.", "the address is 123 main st [PERIOD_SILENCE] north west [PERIOD_SILENCE]"),
        ("Figure No. 1: (approx. 5ft. x 3in.).", "figure number 1 colon open parenthesis approximately 5 feet x 3 inches close parenthesis [PERIOD_SILENCE]"),
        ("Project [Alpha]. Phase II.", "project open bracket alpha close bracket [PERIOD_SILENCE] phase ii [PERIOD_SILENCE]"),
        ("What's up?", "what's up [QUESTION]"),
        ("Well, I suppose... yes!", "well [COMMA_SILENCE] i suppose dot dot dot yes [EXCLAMATION]"),
        ("The cost is $1,234.56. Only 50% left!", "the cost is 1234 point 56 dollars [PERIOD_SILENCE] only 50 percent left [EXCLAMATION]"),
        ("Call 1-800-ABC-DEF.", "call 1 800 abc def [PERIOD_SILENCE]"),
    ]

    for input_text, expected_output in TEST_CASES:
        actual_output = replace_punctuation_and_expand_abreviations(input_text)

        if DEBUG:
            print(f"{Fore.YELLOW}Input:    '{Fore.WHITE + input_text + Fore.YELLOW}'")
            print(f"{Fore.YELLOW}Expected: '{Fore.WHITE + expected_output + Fore.YELLOW}'")
            print(f"{Fore.YELLOW}Actual:   '{Fore.WHITE + actual_output + Fore.YELLOW}'")

        assert actual_output == expected_output, f"\n\n{Fore.RED}Test failed for input: \"{Fore.WHITE + input_text + Fore.RED}\"\nExpected: \"{Fore.WHITE + expected_output + Fore.RED}\"\nGot: {' '* 5}\"{Fore.WHITE + actual_output + Fore.RED}\""
        if DEBUG:
            print(f"{Fore.GREEN}Test \"{Fore.WHITE + input_text + Fore.GREEN}\" Passed!")

    print(f"{Fore.GREEN}All Tests Passed For {Fore.WHITE}replace_punctuation_and_expand_abreviations()")


def test_numbers_to_words(DEBUG=False):
    TEST_CASES = [
        (0, "zero"),
        (1, "one"),
        (10, "ten"),
        (11, "eleven"),
        (19, "nineteen"),
        (20, "twenty"),
        (21, "twenty one"),
        (50, "fifty"),
        (99, "ninety nine"),
        (100, "one hundred"),
        (101, "one hundred one"),
        (115, "one hundred fifteen"),
        (200, "two hundred"),
        (999, "nine hundred ninety nine"),
        (1000, "one thousand"),
        (1001, "one thousand one"),
        (1200, "one thousand two hundred"),
        (1234, "one thousand two hundred thirty four"),
        (10000, "ten thousand"),
        (100000, "one hundred thousand"),
        (123456, "one hundred twenty three thousand four hundred fifty six"),
        (1000000, "one million"),
        (1000001, "one million one"),
        (1234567, "one million two hundred thirty four thousand five hundred sixty seven"),
        (123456789, "one hundred twenty three million four hundred fifty six thousand seven hundred eighty nine"),
        (1234567890, "one billion two hundred thirty four million five hundred sixty seven thousand eight hundred ninety"),
        (7000000, "seven million"),
        (80000, "eighty thousand"),
        (505, "five hundred five"),
        (7777, "seven thousand seven hundred seventy seven"),
        (9876543210, "nine billion eight hundred seventy six million five hundred forty three thousand two hundred ten"),
        (1000000000000, "one trillion"),
        (1000000000001, "one trillion one"),
        (2000000000000, "two trillion"),
    ]

    for input_number, expected_output in TEST_CASES:
        actual_output = numbers_to_words(input_number)

        if DEBUG:
            print(f"{Fore.YELLOW}Input:    '{Fore.WHITE + input_number + Fore.YELLOW}'")
            print(f"{Fore.YELLOW}Expected: '{Fore.WHITE + expected_output + Fore.YELLOW}'")
            print(f"{Fore.YELLOW}Actual:   '{Fore.WHITE + actual_output + Fore.YELLOW}'")

        assert actual_output == expected_output, f"\n\n{Fore.RED}Test failed for input: \"{Fore.WHITE + input_number + Fore.RED}\"\nExpected: \"{Fore.WHITE + expected_output + Fore.RED}\"\nGot: {' '* 5}\"{Fore.WHITE + actual_output + Fore.RED}\""
        if DEBUG:
            print(f"{Fore.GREEN}Test \"{Fore.WHITE + input_number + Fore.GREEN}\" Passed!")
    print(f"{Fore.GREEN}All Tests Passed For {Fore.WHITE}numbers_to_words()")

def main():
    test_replace_punctuation_and_expand_abreviations(DEBUG=True)
    test_numbers_to_words()

if __name__ == "__main__":
    main()