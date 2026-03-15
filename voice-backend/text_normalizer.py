NUMBER_WORDS = {
    "zero": "0",
    "one": "1",
    "two": "2",
    "three": "3",
    "four": "4",
    "five": "5",
    "frame": "5",
    "free": "5",
    "six": "6",
    "seven": "7",
    "eight": "8",
    "feet": "8",
    "nine": "9",     
}

COMMON_FIXES = {
    "lane": "line",
    "lame": "line",
    "right": "line",
    "name": "line",
    "main": "line",
    "i'm": "line",
    "life": "line",
    "mine": "line",
    "lie": "line",
    "rain": "line",
    "late": "line",
    "by done": "python",
    "pissed": "paste",
    "based": "paste",
    "best": "paste",
    
    "flash": "create",
    "make": "create",
    "made": "create",
    
    "wile": "while",
    "vile": "while",
    "ford": "code",
    "and": "run",
    "why": "while",

    "poor": "for",
    "far": "for",
    "four": "for",
    "luke": "loop",

    # delete / remove normalization
    "remove": "delete line",
    "they names": "delete line",
    "removed": "delete line",
    "removing": "delete line",
    "delete": "delete line",
    "deleted": "delete line",
    "clear": "delete line",
    "clears": "delete line",
    "delet": "delete line",
    "del": "delete line",
    "thelate": "delete line",
    "delate": "delete line"
}

def normalize_text(text: str) -> str:
    text = text.lower()
    
    # Prioritize multi-word replacements first
    for key, value in COMMON_FIXES.items():
        if " " in key and key in text:
            text = text.replace(key, value)

    words = text.split()
    normalized = []

    for word in words:
        if word in COMMON_FIXES:
            normalized.append(COMMON_FIXES[word])
        elif word in NUMBER_WORDS:
            normalized.append(NUMBER_WORDS[word])
        else:
            normalized.append(word)

    return " ".join(normalized)
