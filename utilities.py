def ignores_allowed_channels():
    def wrapper(command):
        setattr(command, "ignores_allowance", True)
        return command

    return wrapper


async def get_placeholder(s, url, media=False):
    if media:
        if url.endswith(".png"):
            return await download_file(
                s,
                "https://upload.wikimedia.org/wikipedia/commons/thumb/6/65/No-Image-Placeholder.svg/1665px-No-Image-Placeholder.svg.png",
                True,
            )
    return "Not available"


async def download_file(session, url, media=False):
    try:
        async with session.get(url) as remotefile:
            if remotefile.status == 200:
                data = await remotefile.read()
                if len(data) > 24 * 1000 * 1000:  # 25MB file limit of discord
                    data = await get_placeholder(session, media=media)
                return {"error": "", "data": data}
            return {"error": remotefile.status, "data": ""}
    except Exception as e:
        return {"error": e, "data": ""}
