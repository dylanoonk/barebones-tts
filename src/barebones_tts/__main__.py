import argparse

from colorama import init, Fore

from .core import barebones_tts


def main() -> None:
    parser = argparse.ArgumentParser(
        prog="barebones-tts",
        description="Text-to-speech from first principles.",
    )
    parser.add_argument(
        "text",
        nargs="*",
        help="text to speak; if omitted, enters interactive mode",
    )
    parser.add_argument(
        "-w", "--wav",
        action="store_true",
        help="also save the audio to a .wav file",
    )
    args = parser.parse_args()

    init()
    tts = barebones_tts()

    if args.text:
        input_text = " ".join(args.text)
        tts.speak(input_text)
        if args.wav:
            tts.save(input_text)
        return

    try:
        while True:
            input_text = input(f"{Fore.GREEN}> ").strip()
            tts.speak(input_text)

            if args.wav:
                tts.save(input_text)
    except KeyboardInterrupt:
        print(f"{Fore.RESET}\nGoodbye.")


if __name__ == "__main__":
    main()
