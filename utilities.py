# TODO: fix!
def ignores_allowed_channels():
    def wrapper(command):
        setattr(command, "ignores_allowance", True)
        return command
    return wrapper
