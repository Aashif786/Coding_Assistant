NUMBER_WORDS = {
    "zero": "0",
    "one": "1",
    "two": "2",
    "three": "3",
    "four": "4",
    "five": "5",
    "six": "6",
    "seven": "7",
    "eight": "8",
    "nine": "9",
    "ten": "10",
    "twenty": "20",
    "thirty": "30",
    "forty": "40",
    "fifty": "50",
    "sixty": "60",
}

COMMON_FIXES = {
    "lane": "line",
    "lame": "line",
    "nine": "line",
}

def normalize_text(text: str) -> str:
    words = text.lower().split()
    normalized = []

    for word in words:
        if word in COMMON_FIXES:
            normalized.append(COMMON_FIXES[word])
        elif word in NUMBER_WORDS:
            normalized.append(NUMBER_WORDS[word])
        else:
            normalized.append(word)

    return " ".join(normalized)
