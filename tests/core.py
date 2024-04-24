import linecache
import traceback
from dataclasses import dataclass
from dataclasses import field


@dataclass
class User:
    id: int = 1234567890
    mention: str = f"<@{id}>"


@dataclass
class Bot:
    cogs: list = field(default_factory=lambda: [])

    def add_cog(self, cog):
        self.cogs.append(cog)


@dataclass
class Interaction:
    locale: str = "en-US"


@dataclass
class Context:
    content: str = ""
    interaction: Interaction = field(default_factory=lambda: Interaction())

    async def respond(self, content: str):
        self.content = content


def parametrized(dec):
    def layer(*args, **kwargs):
        def repl(f):
            return dec(f, *args, **kwargs)

        return repl

    return layer


def importfile(file):
    with open(file, "r") as f:
        g = {}
        exec(f.read(), g)
    del g["__builtins__"]
    return g


green = "\033[32m"
red = "\033[31m"
nc = "\033[0m"


@parametrized
def discordtest(callable, name):
    def wrapper(*args, **kwargs):
        print(f"Running {name}... ", end="")
        try:
            _ = callable(*args, **kwargs)
            print(f"[ {green}OK{nc} ]")
            return True, _
        except Exception as e:
            print(f"[{red}FAIL{nc}]")
            return False, e

    wrapper.test = True
    wrapper.name = name
    return wrapper


__tests = []


def add_tests(tests):
    global __tests
    __tests += tests


def run():
    fails = []
    for n, test in enumerate(__tests):
        print(f"{n+1}/{len(__tests)} ", end="")
        if hasattr(test, "test") and test.test:
            ret = test()
            if not ret[0]:
                fails.append([test.name, ret[1]])
        else:
            print(f"Running {test.__name__}... ", end="")
            try:
                test()
                print(f"[ {green}OK{nc} ]")
            except Exception as e:
                print(f"[{red}FAIL{nc}]")
                fails.append([test.__name__, e])
    if len(fails) == 0:
        print(f"[ {green}ALL TESTS OK{nc} ]")
        return
    print(f"[ {red}{len(fails)} TEST{'s' if len(fails) % 10 != 1 else ''} FAILED{nc} ]")
    print("-" * 25)
    print("What went wrong (most deep call first):")
    for fail in fails:
        print(f"[ {red}{fail[0]}{nc} ]")
        tb = fail[1].__traceback__
        e = fail[1]
        lfile = ""
        lfunc = ""
        ft = True
        while tb.tb_next is not None:
            print("-" * 25)
            tb = tb.tb_next
            if not ft:
                if e.__cause__:
                    e = e.__cause__
                    print(f"Has a direct {red}cause{nc} of next exception")
                elif e.__context__:
                    e = e.__context__
                print(
                    f"{type(e).__name__}: {e.message if hasattr(e, 'message') else str(e)}"
                )
            else:
                print(
                    f"{type(e).__name__}: {e.message if hasattr(e, 'message') else str(e)}"
                )

            ft = False
            caller = tb.tb_frame.f_code.co_name
            line = tb.tb_lineno
            file = tb.tb_frame.f_code.co_filename

            linecache.lazycache(file, tb.tb_frame.f_globals)

            if file != lfile:
                print(f'  In file "{red}{file}{nc}"')
                lfile = file
            if caller != lfunc:
                print(f"  In function {red}{caller}{nc}")
                lfunc = caller

            print(f"{line-1:4d}  |" + linecache.getline(file, line - 1).rstrip())
            print(
                f"{line:4d} {red}>{nc}|" + linecache.getline(file, line).rstrip() + nc
            )
            print(f"{line+1:4d}  |" + linecache.getline(file, line + 1).rstrip())
