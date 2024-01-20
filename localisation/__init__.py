import json
try:
    from config import CONFIG
except ImportError:
    print("Unable to load config.")
    CONFIG = {"locale": "en-US"}


DEFAULT_LOCALE = CONFIG["locale"]

LOCALES = ["en-US", "ru"]

LOCALISATIONS = {}


def merge(main_dict, to_merge):
    for key, item in to_merge.items():
        if type(main_dict.get(key)) is dict:
            merge(main_dict.get(key), to_merge.get(key))
            continue
        if not main_dict.get(key):
            main_dict[key] = to_merge.get(key)


for l in LOCALES:
    with open("localisation/"+l+"/locale.txt", 'r', encoding='utf-8') as f:
        filelist = [i.strip() for i in f.readlines()]
    for file in filelist:
        with open("localisation/"+l+"/strings/"+file, 'r', encoding='utf-8') as f:
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
        if localisations is None:
            break
    if localisations is None:
        localisations = {loc: string+"."+loc for loc in LOCALES}
    if locale is None:
        return localisations
    return localisations.get(locale, localisations.get(DEFAULT_LOCALE, string+"."+locale))
