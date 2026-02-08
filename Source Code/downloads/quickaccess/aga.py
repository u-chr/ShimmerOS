from os import getcwd,path,remove
import customtkinter as ctk
import aiohttp
import asyncio
import threading
import ssl
from utils import resource_path
import zipfile
from psutil import cpu_count
ssl_ctx = ssl.create_default_context(cafile=resource_path("dependencies/cacert.pem"))
async def getURL(self,btn,modulename,w):
    appFrame = btn.master
    appFrame.application = ["",modulename]
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
            outputloc = path.dirname(DLpath)
            zip_ref.extractall(outputloc)
        remove(DLpath)
        config_ini_path = path.join(outputloc,"AutoGpuAffinity","config.ini")
        print(f"Editing {config_ini_path}")
        logi = cpu_count(logical=True)
        phys = cpu_count(logical=False)
        cpus = []
        if logi != phys: #hyperthreading is on
            for cpu in range(logi):
                if cpu % 2 == 0:
                    cpus.append(cpu)
        with open(config_ini_path,"r",encoding="utf-8") as f:
            lines = f.readlines()
        with open(config_ini_path,'w') as f:
            for line in lines:
                if line.strip().startswith("custom_cpus="):
                    f.write(f"custom_cpus={cpus}\n")
                else:
                    f.write(line)
    threading.Thread(target=lambda: asyncio.run(async_download("https://github.com/valleyofdoom/AutoGpuAffinity/releases/latest/download/AutoGpuAffinity.zip",path.join(getcwd()[:2],"\\Shimmer","Software","quickaccess","AutoGpuAffinity.zip"),progressbar)), daemon=True).start() #asynchronous download
