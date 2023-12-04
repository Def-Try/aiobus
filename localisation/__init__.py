import json

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