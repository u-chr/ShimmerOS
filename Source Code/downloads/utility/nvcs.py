from bs4 import BeautifulSoup
from pathlib import Path
import subprocess
async def getURL(ssl_ctx,continuation,progressbar,completeDownload):
    try:
        proc = subprocess.Popen(["curl", "https://sourceforge.net/projects/nvcleanstall/files/latest/download"],stdout=subprocess.PIPE, creationflags=subprocess.CREATE_NO_WINDOW)
        html = proc.communicate()[0]
        print(html)
        soup = BeautifulSoup(html,"html.parser")
    except Exception as e:
        print(f"Error during download: {e}")
        await completeDownload(progressbar,progressbar.master,msg="Error",text_color="#ff5555")
        return
    url = soup.find("a")['href']
    download_path = Path.home() / "Downloads" / f"{url.split('?ts=')[0].rsplit('/',1)[1]}"
    await continuation(url,download_path)
