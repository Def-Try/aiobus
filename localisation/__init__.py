import json

try:
    from config import CONFIG
except ImportError:
    print("Unable to load config.")
    CONFIG = {"locale": "en-US"}


DEFAULT_LOCALE = CONFIG["locale"]
LOCALES = ["en-US", "ru"]
CHECK_LOCALES = False
LOCALISATIONS = {}


def merge(main_dict, to_merge):
    for key, item in to_merge.items():
        if isinstance(main_dict.get(key), dict):
            merge(main_dict.get(key), item)
            continue
        if not main_dict.get(key):
            main_dict[key] = item


def prepare_locale(loc_, lang):
    for k, v in loc_.items():
        if isinstance(v, str):
            loc_[k] = {lang: v}
            continue
        prepare_locale(v, lang)


for l in LOCALES:
    with open("localisation/" + l + "/locale.txt", "r", encoding="utf-8") as f:
        filelist = [i.strip() for i in f.readlines()]
    file = ""
    for file in filelist:
        with open("localisation/" + l + "/strings/" + file, "r", encoding="utf-8") as f:
            loc = json.loads(f.read())

            prepare_locale(loc, l)
            merge(LOCALISATIONS, loc)
            del loc
        del f
    del filelist
    del file
del l


def localise(string, locale=None):
    localstring = string.split(".")
    localisations = LOCALISATIONS
    for i in localstring:
        localisations = localisations.get(i, None)
        if localisations is None:
            break
    if localisations is None:
        localisations = {loc: string + "." + loc for loc in LOCALES}
    if locale is None:
        return localisations
    return localisations.get(
        locale, localisations.get(DEFAULT_LOCALE, string + "." + locale)
    )

if CHECK_LOCALES:
    def diff(source, diff_):
        has = []
        for i in source:
            if i not in diff_:
                has.append(i)
        return has

    def check(localedict, localepath):
        for k, v in localedict.items():
            if isinstance(v, dict):
                if any(i in v for i in LOCALES):
                    if not all(i in v for i in LOCALES):
                        print(
                            localepath + "." + k,
                            "does not have a translation string for locale(s)",
                            ", ".join(diff(LOCALES, v)),
                        )
                check(v, localepath + "." + k)
                continue

    check(LOCALISATIONS, "root")

    del check
    del diff

del json
del CONFIG
del CHECK_LOCALES
del merge
del prepare_locale
