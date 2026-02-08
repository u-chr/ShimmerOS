from pathlib import Path
async def getURL(ssl_ctx,continuation,progressbar,completeDownload):
    await continuation("https://lmstudio.ai/download/latest/win32/x64",(Path.home() / "Downloads" / "LM-Studio-x64.exe"))

