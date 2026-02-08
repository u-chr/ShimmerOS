import aiohttp
from pathlib import Path
async def getURL(ssl_ctx,continuation,progressbar,completeDownload):
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get("https://api.github.com/repos/mullvad/mullvadvpn-app/releases",ssl=ssl_ctx) as resp:
                resp.raise_for_status()
                releases = await resp.json()
    except Exception as e:
        print(f"Error during download: {e}")
        await completeDownload(progressbar,progressbar.master,msg="Error",text_color="#ff5555")
        return
    url = None
    for release in releases:
        for assets in release.get("assets", []):
            if assets["name"].endswith("_x64.exe"):
                url = assets["browser_download_url"]
                break
        if url:
            break
    await continuation(url,(Path.home() / "Downloads" / f"{url.rsplit("/",1)[1]}"))
