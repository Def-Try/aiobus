import math
import os
import random
import string
from difflib import ndiff


class Language:
    def initdict(self):
        pass

    def __init__(self):
        self.dictionary = {}
        self.doupper = True
        self.initdict()
        if self.doupper:
            self.dictionary = {
                **self.dictionary,
                **{k.upper(): v.upper() for k, v in self.dictionary.items()},
            }
        self.reversed_dictionary = {
            value: key for key, value in self.dictionary.items()
        }

    def translate(self, mode, text):
        if not self.doupper:
            text = text.lower()
        st = ""
        if mode == "to":
            for ch in text:
                st += self.dictionary.get(ch, ch)
        if mode == "from":
            ptr = 0
            ptr_ = 0
            while ptr < len(text):
                chunk = ""
                while ptr_ < len(text):
                    chunk += text[ptr_]
                    if self.reversed_dictionary.get(chunk):
                        st += self.reversed_dictionary[chunk]
                        chunk = None
                        break
                    ptr_ += 1
                if chunk is None:
                    ptr = ptr_ + 1
                    ptr_ = ptr
                    continue
                st += text[ptr]
                ptr += 1
                ptr_ = ptr
        return st


class Nyatalk(Language):
    def initdict(self):
        pass

    def translate(self, mode, text):
        if mode == "from":
            return text
        stutter, emote = True, True
        result = ""
        for ch in text:
            if ch == "л":
                result += "в"
            elif ch == "р":
                result += "л"
            elif ch == "в":
                result += "ф"
            elif ch == "ю":
                result += "ую"
            elif ch == "у":
                result += "ю"
            elif ch == "ж":
                result += "з"
            elif ch == "r":
                result += "l"
            elif ch == "l":
                result += "w"
            elif ch == "u":
                result += "yu"
            else:
                result += ch
        result = result.strip()
        if stutter:
            text = result
            result = ""
            n = random.randint(1, 3)
            for word in text.split(" "):
                if not word:
                    result += " "
                    continue
                n += 1
                if n < 3:
                    result += word + " "
                    continue
                n = random.randint(-1, 3)
                result += word[0] + "-" + word + " "
            result = result.strip()
        if emote:
            result += " " + random.choice(["UwU", "OwO", "owo", "Pwp", "TwT", "~w~"])
        return result


class Codespeak:
    def __init__(self):
        with open(os.path.dirname(__file__) + "/russian.txt", encoding="utf-8") as f:
            self.dictionary = [i.strip() for i in f.readlines()]
        self.terminators = " .,:;-!?()[]{}\\/#@*_"
        self.epsilon = 1
        random.Random(4).shuffle(self.dictionary)

    def translate(self, mode, text):
        word = ""
        tx = ""
        for ch in text + ".":
            word += ch
            if ch not in self.terminators:
                continue
            word = word[:-1].lower().strip()
            if word not in self.dictionary:
                tx += word + ch
                word = ""
                continue
            tx += (
                self.dictionary[
                    (
                        self.dictionary.index(word)
                        + (self.epsilon * (1 if mode == "to" else -1))
                    )
                    % len(self.dictionary)
                ]
                + ch
            )
            word = ""
        tx = tx[:-1]
        tx += word
        return tx


class Nekomimetic(Language):
    def initdict(self):
        self.dictionary = {
            "a": "ne",
            "b": "ko",
            "c": "nya",
            "d": "mi",
            "e": "mo",
            "f": "fu",
            "g": "uf",
            "h": "ama",
            "i": "san",
            "j": "kum",
            "k": "bo",
            "l": "op",
            "m": "do",
            "n": "ki",
            "o": "ka",
            "p": "ke",
            "q": "ic",
            "r": "ha",
            "s": "an",
            "t": "zaa",
            "u": "to",
            "v": "ori",
            "w": "mu",
            "x": "ba",
            "y": "yo",
            "z": "aa",
            "а": "не",
            "б": "ко",
            "в": "нья",
            "г": "ми",
            "д": "мг",
            "е": "фу",
            "ё": "уф",
            "ж": "ама",
            "з": "сан",
            "и": "кюн",
            "и́": "бо",
            "к": "оп",
            "л": "до",
            "м": "ки",
            "н": "ка",
            "о": "ке",
            "п": "ик",
            "р": "ха",
            "с": "ан",
            "у": "то",
            "ф": "ори",
            "х": "мю",
            "ц": "ба",
            "ч": "уо",
            "ш": "аа",
            "щ": "ни",
            "ъ": "ку",
            "ы": "йю",
            "ь": "ии",
            "э": "ня",
            "ю": "тю",
            "я": "йа",
        }


class Common(Language):
    def translate(self, _, text):
        return text


class Uncommon(Language):
    def initdict(self):
        self.dictionary = {
            "a": "be",
            "b": "me",
            "c": "fe",
            "d": "ce",
            "e": "oi",
            "f": "ne",
            "g": "ko",
            "h": "co",
            "i": "yu",
            "j": "nu",
            "k": "bu",
            "l": "ho",
            "m": "re",
            "n": "ru",
            "o": "ae",
            "p": "ju",
            "q": "cy",
            "r": "hi",
            "s": "tu",
            "t": "za",
            "u": "ao",
            "v": "wu",
            "w": "vu",
            "x": "de",
            "y": "ou",
            "z": "se",
            "а": "бе",
            "б": "ме",
            "в": "фе",
            "г": "це",
            "д": "не",
            "е": "ои",
            "ё": "ое",
            "ж": "ту",
            "з": "ре",
            "и": "оу",
            "й": "вю",
            "к": "зу",
            "л": "ню",
            "м": "бу",
            "н": "ну",
            "о": "еи",
            "п": "ме",
            "р": "те",
            "с": "ве",
            "т": "ры",
            "у": "яи",
            "ф": "ха",
            "х": "на",
            "ц": "ко",
            "ч": "та",
            "ш": "жо",
            "щ": "шо",
            "ъ": "йй",
            "ы": "ая",
            "ь": "ии",
            "э": "оа",
            "ю": "яа",
            "я": "яо",
        }


class Standart(Language):
    def initdict(self):
        self.doupper = False
        self.dictionary = {
            "a": "ᔑ",
            "b": "ʖ",
            "c": "ᓵ",
            "d": "↸",
            "e": "ᒷ",
            "f": "⎓",
            "g": "⊣",
            "h": "⍑",
            "i": "╎",
            "j": "⋮",
            "k": "ꖌ",
            "l": "ꖎ",
            "m": "ᒲ",
            "n": "リ",
            "o": "𝙹",
            "p": "!¡",
            "q": "ᑑ",
            "r": "∷",
            "s": "ᓭ",
            "t": "ℸ ̣",
            "u": "⚍",
            "v": "⍊",
            "w": "∴",
            "x": " ̇/",
            "y": "||",
            "z": "⨅",
        }


class DroneLang(Language):
    def initdict(self):
        self.doupper = False
        alphabet = string.printable + "абвгдеёжзийклмнопрстуфхцчшщъыьэюя"
        for i, letter in enumerate(alphabet):
            self.dictionary[letter] = "." + format(
                i, f"0{len(alphabet).bit_length()}b"
            ).replace("0", ".").replace("1", "|")
        for i, letter in enumerate(alphabet.upper()):
            self.dictionary[letter] = "|" + format(
                i, f"0{len(alphabet).bit_length()}b"
            ).replace("0", ".").replace("1", "|")


class Squirrelatin(Language):
    def _tobase(self, b, n):
        e = n // b
        q = n % b
        if n == 0:
            return "0"
        if e == 0:
            return str(q)
        return self._tobase(b, e) + str(q)

    def tobase(self, b, n, p):
        cv = self._tobase(b, n)
        return "0" * max(0, p - len(cv)) + cv

    def initdict(self):
        self.doupper = False
        alphabet = "abcdefghijklmnopqrstuvwxyzабвгдеёжзийклмнопрстуфхцчшщъыьэюя"
        pad = math.ceil(math.log(len(alphabet), 4))
        for i, letter in enumerate(alphabet):
            self.dictionary[letter] = "х" + "".join(
                ["хцчф"[int(j)] for j in self.tobase(4, i, pad)]
            )
        for i, letter in enumerate(alphabet.upper()):
            self.dictionary[letter] = "Х" + "".join(
                ["хцчф"[int(j)] for j in self.tobase(4, i, pad)]
            )


class AutoTranslatorFrom:
    def __init__(self, languages):
        self.languages = languages

    @staticmethod
    def levenshtein_distance(str1, str2, ):
        counter = {"+": 0, "-": 0}
        distance = 0
        for edit_code, *_ in ndiff(str1, str2):
            if edit_code == " ":
                distance += max(counter.values())
                counter = {"+": 0, "-": 0}
            else: 
                counter[edit_code] += 1
        distance += max(counter.values())
        return distance

    def translate(self, mode, text):
        if mode == "to": return text
        scores = {}
        for language in self.languages:
            textt = language.translate("from", text)
            scores[language] = 1 - self.levenshtein_distance(text, textt) / max(len(text), len(textt))
        best = list(scores.keys())[list(scores.values()).index(max(scores.values()))]
        return best.translate("from", text)



languages = {
    "nekomimetic": Nekomimetic(),
    "dronelang": DroneLang(),
    "galactic_common": Common(),
    "galactic_uncommon": Uncommon(),
    "galactic_standart": Standart(),
    "squirrelatin": Squirrelatin(),
    "codespeak": Codespeak(),
    "nyatalk": Nyatalk(),
}
languages["autofrom"] = AutoTranslatorFrom(languages)
