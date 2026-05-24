from pathlib import Path


def load_word_list():
    word_file = Path(__file__).resolve().parent / "words.txt"
    if not word_file.exists():
        return set()
    with word_file.open("r", encoding="utf-8") as f:
        return {line.strip().upper() for line in f if line.strip()}
