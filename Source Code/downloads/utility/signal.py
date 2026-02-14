import aiohttp
from pathlib import Path
import re
async def getURL(ssl_ctx,continuation,progressbar,completeDownload):
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get("https://updates.signal.org/desktop/latest.yml",ssl=ssl_ctx) as resp:
                resp.raise_for_status()
                html = await resp.text()
    except Exception as e:
        print(f"Error during download: {e}")
        await completeDownload(progressbar,progressbar.master,msg="Error",text_color="#ff5555")
        return
    url = "https://updates.signal.org/desktop/" + re.findall(r"path: (.*.exe)\b",html)[0]
    download_path = Path.home() / "Downloads" / f"{url.rsplit("/",1)[1]}"
    await continuation(url,download_path)