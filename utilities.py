def ignores_allowed_channels():
    def wrapper(command):
        setattr(command, "ignores_allowance", True)
        return command

    return wrapper


async def download_file(session, url):
    try:
        async with session.get(url) as remotefile:
            if remotefile.status == 200:
                data = await remotefile.read()
                return {"error": "", "data": data}
            return {"error": remotefile.status, "data": ""}
    except Exception as e:
        return {"error": e, "data": ""}
