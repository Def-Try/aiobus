import json
from config import CONFIG

DEFAULT_LOCALE = CONFIG["locale"]

LOCALES = ["en-US", "ru"]
LOADED_LOCALES = []

LOCALISATIONS = {}

def merge(main_dict, to_merge):
	for key, item in to_merge.items():
		if type(main_dict.get(key)) is dict:
			merge(main_dict.get(key), to_merge.get(key))
			continue
		if not main_dict.get(key): main_dict[key] = to_merge.get(key)

for l in LOCALES:
	with open("localisation/"+l+".locale", 'r', encoding='utf-8') as f:
	    locale = json.loads(f.read())
	    def prepare_locale(locale, lang):
	        for k, v in locale.items():
	            if type(v) == str:
	                locale[k] = {lang: v}
	                continue
	            prepare_locale(v, lang)
	    prepare_locale(locale, l)
	    merge(LOCALISATIONS, locale)

def localise(string, locale=None):
	localstring = string.split(".")
	localisations = LOCALISATIONS
	for i in localstring:
		localisations = localisations.get(i, None)
		if localisations is None: break
	if localisations is None and locale is None:
		return LOCALISATIONS["error"]["locale_string_unknown"]
	if localisations is None:
		return LOCALISATIONS["error"]["locale_string_unknown"].get(locale, 
			LOCALISATIONS["error"]["locale_string_unknown"].get(DEFAULT_LOCALE, 
				"error.locale_string_unknown."+locale))
	if locale is None:
		return localisations
	return localisations.get(locale, localisations.get(DEFAULT_LOCALE, string+"."+locale))