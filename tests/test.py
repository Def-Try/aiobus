import core

# use discordtest decorator to set test name
@core.discordtest("Example test")
def test1():
    pass

# tests without decorator are allowed too
def no_dec_test():
    pass

# if exception gets raised in test, it will be treated as failed
@core.discordtest("Exception test")
def test3():
    def inner():
        raise Exception("i'm a bad test >:3") from ValueError("nyaa")
    inner()

@core.discordtest("Real exception test")
def test4():
    x = 0
    return 1 / x

core.add_tests([test1, test3, no_dec_test, test4])
core.run()
