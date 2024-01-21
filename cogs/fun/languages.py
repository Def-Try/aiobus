import string
import math


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
            "и": "кум",
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


languages = {
    "nekomimetic": Nekomimetic(),
    "dronelang": DroneLang(),
    "galactic_common": Common(),
    "galactic_uncommon": Uncommon(),
    "galactic_standart": Standart(),
    "squirrelatin": Squirrelatin(),
}