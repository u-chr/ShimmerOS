from pathlib import Path
async def getURL(ssl_ctx,continuation,progressbar,completeDownload):
    await continuation("https://aka.ms/xboxinstaller",(Path.home() / "Downloads" / "XboxInstaller.exe"))