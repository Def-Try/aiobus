from __init__ import LOCALISATIONS, LOCALES

def diff(source, diff):
	has = []
	for i in source:
		if i not in diff: has.append(i)
	return has

def check(localedict, localepath):
	for k,v in localedict.items():
		if isinstance(v, dict):
			if any([i in v for i in LOCALES]):
				if not all([i in v for i in LOCALES]):
					print(localepath+"."+k, "does not have a translation string for locale(s)", ", ".join(diff(LOCALES, v)))
			check(v, localepath+"."+k)
			continue
		#print(localepath+"."+k)

check(LOCALISATIONS, "root")