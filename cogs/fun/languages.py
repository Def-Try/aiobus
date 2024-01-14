import string
import transliterate

class Converter:
	def raw_to_usable(self, text):
		return (transliterate.detect_language(text, fail_silently=True) or 'ru')+transliterate.translit(text, (transliterate.detect_language(text, fail_silently=True) or 'ru'), reversed=True)
	def usable_to_raw(self, text):
		return transliterate.translit(text[2:], text[:2])

class Language:

	dictionary = {}
	doupper = True
	__converter = Converter()

	def initdict(self): pass
	def __init__(self):
		self.initdict()
		if self.doupper:
			self.dictionary = {**self.dictionary, **{k.upper(): v.upper() for k,v in self.dictionary.items()}}
		self.reversed_dictionary = {value: key for key, value in self.dictionary.items()}

	def translate(self, mode, text):
		if not self.doupper: text = text.lower()
		if mode == "to":
			text = self.__converter.raw_to_usable(text)
			st = ""
			for ch in text:
				st += self.dictionary.get(ch, ch)
			return st
		if mode == "from":
			st = ""
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
			st = self.__converter.usable_to_raw(st)
			return st

class Nekomimetic(Language):
	dictionary = {
		"a": "ne", "b": "ko", "c": "nya", "d": "mi",
		"e": "mo", "f": "fu", "g": "uf", "h": "ama", 
		"i": "san", "j": "kum", "k": "bo", "l": "op", 
		"m": "do", "n": "ki", "o": "ka", "p": "ke", 
		"q": "ic", "r": "ha", "s": "an", "t": "zaa", 
		"u": "to", "v": "ori", "w": "mu", "x": "ba", 
		"y": "yo", "z": "aa"
	}

class Furrytongue(Language):
	dictionary = {
		"a": "ne", "b": "ko", "c": "nya", "d": "mi",
		"e": "mo", "f": "fu", "g": "uf", "h": "ama", 
		"i": "san", "j": "kum", "k": "bo", "l": "op", 
		"m": "do", "n": "ki", "o": "ka", "p": "ke", 
		"q": "ic", "r": "ha", "s": "an", "t": "zaa", 
		"u": "to", "v": "ori", "w": "mu", "x": "ba", 
		"y": "yo", "z": "aa"
	}

class Common(Language):
	def translate(self, _, text): return text

class Uncommon(Language):
	dictionary = {
		"a": "be", "b": "me", "c": "fe", "d": "ce",
		"e": "oi", "f": "ne", "g": "ko", "h": "co", 
		"i": "yu", "j": "nu", "k": "bu", "l": "ho", 
		"m": "re", "n": "ru", "o": "ae", "p": "ju", 
		"q": "cy", "r": "hi", "s": "tu", "t": "za", 
		"u": "ao", "v": "wu", "w": "vu", "x": "de", 
		"y": "ou", "z": "se"
	}

class Standart(Language):

	doupper = False

	dictionary = {
		"a": "ᔑ", "b": "ʖ", "c": "ᓵ", "d": "↸",
		"e": "ᒷ", "f": "⎓", "g": "⊣", "h": "⍑", 
		"i": "╎", "j": "⋮", "k": "ꖌ", "l": "ꖎ", 
		"m": "ᒲ", "n": "リ", "o": "𝙹", "p": "!¡", 
		"q": "ᑑ", "r": "∷", "s": "ᓭ", "t": "ℸ ̣", 
		"u": "⚍", "v": "⍊", "w": "∴", "x": " ̇/", 
		"y": "||", "z": "⨅"
	}

class DroneLang(Language):

	doupper = False

	def initdict(self):
		alphabet = string.printable
		for i, letter in enumerate(alphabet):
			self.dictionary[letter] = "."+format(i, f"0{len(alphabet).bit_length()}b").replace("0", ".").replace("1", "|")
		for i, letter in enumerate(alphabet.upper()):
			self.dictionary[letter] = "|"+format(i, f"0{len(alphabet).bit_length()}b").replace("0", ".").replace("1", "|")

languages = {
	"nekomimetic": Nekomimetic(),
	"dronelang": DroneLang(),
	"galactic_common": Common(),
	"galactic_uncommon": Uncommon(),
	"galactic_standart": Standart(),
	"furrytongue": Furrytongue()
	}