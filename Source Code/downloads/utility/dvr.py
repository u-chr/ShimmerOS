from pathlib import Path
async def getURL(ssl_ctx,continuation,progressbar,completeDownload):
    await continuation("https://davinci-resolve.loplxl.workers.dev/",(Path.home() / "Downloads" / "Davinci_Resolve.zip"))

