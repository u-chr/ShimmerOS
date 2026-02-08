from pathlib import Path
async def getURL(ssl_ctx,continuation,progressbar,completeDownload):
    await continuation("https://cdn.fastly.steamstatic.com/client/installer/SteamSetup.exe",(Path.home() / "Downloads" / "SteamSetup.zip"))
