from pathlib import Path
async def getURL(ssl_ctx,continuation,progressbar,completeDownload):
    await continuation("https://justgetflux.com/flux-setup.exe",(Path.home() / "Downloads" / "flux-setup.exe"))