
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


def main():
    print(numbers_to_words(1234567890))


if __name__ == '__main__':
    main()