from tempfile import gettempdir
from pathlib import Path
from os import getcwd,path,mkdir
import customtkinter as ctk
import aiohttp
import asyncio
import threading
import ssl
from shutil import copy2,rmtree
from utils import resource_path
import zipfile
ssl_ctx = ssl.create_default_context(cafile=resource_path("dependencies/cacert.pem"))
async def getURL(self,btn,modulename,w):
    DL_DIR = path.join(gettempdir(),"SHIMMERTEMP")
    if not path.exists(DL_DIR):
        mkdir(DL_DIR)
    appFrame = btn.master
    appFrame.application = [None,modulename]
    progressbar = ctk.CTkProgressBar(appFrame,width=round(w/4))
    self.after(0,btn.destroy)
    progressbar.set(0)
    progressbar.grid(row=0,column=1,padx=(0,10),sticky="e")
    async def async_download(url,DLpath,progressbar):
        print(f"attempting to download from {url} to {DLpath}")
        lastUpdateFrac = 0
        async def write(f,chunk):
            nonlocal lastUpdateFrac
            f.write(chunk)
            if total:
                frac = downloaded/total
                if frac-lastUpdateFrac >= 0.01 and frac <= 1: #only update ui every 1% downloaded
                    threading.Thread(target=lambda: self.after(0,progressbar.set,frac), daemon=True).start()
                    lastUpdateFrac = frac
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url,ssl=ssl_ctx) as resp:
                    resp.raise_for_status()
                    total = resp.content_length or 0
                    downloaded = 0
                    with open(DLpath, "wb") as f:
                        async for chunk in resp.content.iter_chunked(8192):
                            downloaded += len(chunk)
                            await write(f,chunk)
        except Exception as e:
            print(f"Error during download: {e}")
            completeLabel = ctk.CTkLabel(appFrame, text="Error", text_color="#ff5555", font=ctk.CTkFont(size=20))
            self.master.master.shrink(completeLabel,progressbar.winfo_width(),20)
            self.after(0,progressbar.destroy)
            completeLabel.grid(row=0,column=1,padx=(0,10))
            
            await asyncio.sleep(3)
            self.after(0,completeLabel.destroy)
            print(f"attempting to resummon {appFrame.application}")
            btn = ctk.CTkButton(appFrame, text="Download", width=round(appFrame.winfo_width()/4), font=ctk.CTkFont(size=16))
            btn.configure(command=lambda: asyncio.run(self.procedureWorker(appFrame.application,btn)))
            self.master.master.shrink(btn,round(appFrame.winfo_width()/4),size=16)
            btn.grid(row=0,column=1,padx=(0,5),sticky="e")
            return
        completeLabel = ctk.CTkLabel(appFrame, text="Complete", text_color="#55ff55", font=ctk.CTkFont(size=20))
        self.master.master.shrink(completeLabel,progressbar.winfo_width(),20)
        self.after(0,progressbar.destroy)
        completeLabel.grid(row=0,column=1,padx=(0,10))
        with zipfile.ZipFile(DLpath, 'r') as zip_ref:
            outputloc = path.join(DL_DIR,"nsudo")
            zip_ref.extractall(outputloc)
        copy2(path.join(outputloc,"NSudo Launcher","x64","NSudoLG.exe"),path.join(getcwd()[2:],"/Shimmer","Software","quickaccess","NSudo.exe"))
        rmtree(DL_DIR) #i love you shutil
    threading.Thread(target=lambda: asyncio.run(async_download("https://github.com/M2TeamArchived/NSudo/releases/download/8.2/NSudo_8.2_All_Components.zip",path.join(DL_DIR,"nsu`do.zip"),progressbar)), daemon=True).start() #asynchronous download
