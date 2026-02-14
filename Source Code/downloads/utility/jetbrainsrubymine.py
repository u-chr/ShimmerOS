from pathlib import Path
from .jetbrains_worker import get_url
async def getURL(ssl_ctx,continuation,progressbar,completeDownload):
    try:
        url = await get_url("RM",ssl_ctx)
        print(url)
    except Exception as e:
        print(f"Error during download: {e}")
        await completeDownload(progressbar,progressbar.master,msg="Error",text_color="#ff5555")
        return
    await continuation(url,Path.home() / "Downloads" / url.rsplit("/",1)[1])