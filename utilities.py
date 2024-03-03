def ignores_allowed_channels():
    def wrapper(command):
        command.ignores_allowance = True
        return command
    return wrapper