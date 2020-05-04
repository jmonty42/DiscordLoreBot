from commands.authorize import authorize


async def unauthorize(**kwargs):
    kwargs["unauthorize"] = True
    await authorize(**kwargs)
