import g4f

for provider in [getattr(g4f.Provider, i) for i in g4f.Provider.__all__ if getattr(g4f.Provider, i).working]:
    print("Trying:", provider.__name__)
    try:
        print("...", g4f.ChatCompletion.create(
            model="gpt-3.5-turbo",
            provider=provider,
            messages=[{"role": "user", "content": "Hello"}],
        ))
    except: print("...Fail")
