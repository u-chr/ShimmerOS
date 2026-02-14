from pathlib import Path
async def getURL(ssl_ctx,continuation,progressbar,completeDownload):
    await continuation("https://github.com/stoatchat/for-desktop/releases/latest/download/stoat-desktop-setup.exe",Path.home() / "Downloads" / "stoat-desktop-setup.exe")