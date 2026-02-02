from pathlib import Path
async def getURL(ssl_ctx,continuation,progressbar,completeDownload):
    await continuation("https://github.com/eskezje/SCEWIN-GUI/releases/latest/download/SCEWIN-GUI.exe",(Path.home() / "Downloads" / "SCEWIN-GUI.exe"))