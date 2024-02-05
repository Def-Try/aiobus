import g4f

usable = []

for provider in [
    getattr(g4f.Provider, i)
    for i in g4f.Provider.__all__
    if getattr(g4f.Provider, i).working
]:
    print("Trying:", provider.__name__)
    try:
        print(
            "...",
            g4f.ChatCompletion.create(
                model="gpt-3.5-turbo",
                provider=provider,
                messages=[{"role": "user", "content": "Hello"}],
            ),
        )
        usable.append(provider.__name__)
    except Exception as e:
        print("... Fail:", e)

print(*usable)
