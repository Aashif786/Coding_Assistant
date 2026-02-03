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
    "ten": "10",
    "eleven": "11",  
    "level": "11",  
    "learn": "11",  
    "twelve": "12",
    "thirteen": "13",
    "fourteen": "14",
    "fifteen": "15",
    "sixteen": "16",
    "seventeen": "17",
    "eighteen": "18",
    "nineteen": "19",
    "twenty": "20",
    "plenty": "20",
    "ready": "20",
    "twenties": "20",
    "thirty": "30",
    "forty": "40",
    "fifty": "50",
    "sixty": "60",
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
    
    # Removed "nine": "line" to allow number 9
    # Removed specific "line X" mappings that were incorrect
    "player": "delete line",
    "more lying": "delete line",
    "removal and": "delete line",
    "remove them": "delete line",
    "removal": "delete line",
    "the late": "delete line",
    "bill": "delete line",

    "through": "three",
    "tree": "three",
    "too": "two",
    "to": "two",
    "fore": "four",
    "fight": "five",
    "fives": "five",
    "sex": "six",
    "sick": "six",
    "ate": "eight",
    "teen": "ten",

    "funk": "function",
    "fun": "function",
    "shun": "function",

    "plus": "print",
    "prince": "print",

    "clasp": "class",
    "glass": "class",

    "wile": "while",
    "vile": "while",

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
