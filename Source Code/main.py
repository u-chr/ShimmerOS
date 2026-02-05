#!/usr/bin/env python3
version = "1.5.2.6"

from functools import cache
import customtkinter as ctk
ctk.set_appearance_mode("dark")
from hashlib import sha256
import threading
import aiohttp
import asyncio
from datetime import datetime
from subprocess import Popen, DETACHED_PROCESS, CREATE_NEW_PROCESS_GROUP
from os import listdir,getcwd,mkdir
from os.path import isdir,join,exists
from math import ceil
import ctypes
from sys import exit

drive = getcwd()[:2]
SHIMMERP = join(drive,"/Shimmer/")
SOFTWAREP = join(SHIMMERP,"Software")
QA_P = join(SOFTWAREP,"quickaccess")
TWEAKSP = join(SOFTWAREP,"Tweaks")
for path in [SHIMMERP, SOFTWAREP, QA_P]:
    if not exists(path):
        mkdir(path)
createTweaks = False
if exists(TWEAKSP):
    createTweaks = True

class newGUI(ctk.CTk):
    def closeAutoUpdater(self):
        print("close auto updater")
        self.updateTL.destroy()
    async def showlogs(self):
        createnewtl = False
        try:
            if not self.logsTL.winfo_exists():
                createnewtl = True
        except Exception:
            createnewtl = True
        if createnewtl:
            self.logsTL = ctk.CTkToplevel(self, fg_color="#201d26")
            self.logsTL.protocol("WM_DELETE_WINDOW", lambda: self.logsTL.destroy())
            self.logsTL.geometry("400x200")
            self.logsTL.title("Current Logs")
            self.logsTL.logbox = ctk.CTkTextbox(self.logsTL,fg_color="transparent")
            self.logsTL.logbox.pack(side="top",fill="x",expand=True, pady=5,padx=5)
            self.logsTL.logbox.insert("end", self.logger.logs)
            self.logsTL.logbox.see("end")
            self.logsTL.logbox.configure(state="disabled")
        self.logsTL.attributes("-topmost", True)
        self.logsTL.after(10,lambda: self.logsTL.attributes("-topmost", False))
    async def AutoUpdater(self):
        print("Auto updater called")
        try:
            self.updateTL.attributes("-topmost", True)
            self.updateTL.after(10,lambda: self.updateTL.attributes("-topmost", False))
            print("Auto updater already exists, bringing to front.")
            return
        except Exception as e:
            print("No updater TL, creating...")
            self.updateTL = ctk.CTkToplevel(self, fg_color="#201d26")
            self.updateTL.protocol("WM_DELETE_WINDOW", self.closeAutoUpdater)
            self.updateTL.geometry("400x200")
            self.updateTL.title("Check for updates")

            self.processLabel = ctk.CTkTextbox(self.updateTL,fg_color="transparent",state="disabled")
            self.processLabel.pack(side="top",fill="x",expand=True, pady=5,padx=5)
            self.updateTL.attributes("-topmost", True)
            self.updateTL.after(10,lambda: self.updateTL.attributes("-topmost", False))
        def log(msg):
            print(msg) #to send it to log files
            self.processLabel.configure(state="normal")
            self.processLabel.insert("end", msg+"\n")
            self.processLabel.see("end")
            self.processLabel.configure(state="disabled")
            self.updateTL.update()

        log("Checking if update is required...")
        log("Current version: " + self.CurrentVersion)
        status = [0,0]
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get("https://api.github.com/repos/loplxl/ShimmerOS/releases/tags/" + self.CurrentVersion) as resp:
                    resp.raise_for_status()
                    jsonresp = await resp.json()
                    status[0] = jsonresp["updated_at"]
                async with session.get("https://api.github.com/repos/loplxl/ShimmerOS/releases/latest") as resp2:
                    resp2.raise_for_status()
                    global jsonresp2
                    jsonresp2 = await resp2.json()
                    status[1] = jsonresp2["updated_at"]
        except Exception as e:
            log(f"Failed to get version info.\n{e}")
            return
        print(status)
        log(f"Current version update time: {status[0]}")
        log(f"Latest version update time: {status[1]}")

        current = datetime.fromisoformat(status[0].replace("Z", "+00:00"))
        latest  = datetime.fromisoformat(status[1].replace("Z", "+00:00"))

        if latest <= current:
            log("All up to date!")
            return
        log("Outdated Shimmer, updating...")
        log("Checking if auto updater is installed...")
        
        UPD_DIR = join(SOFTWAREP,"Updater")
        UPD_PATH = join(UPD_DIR,"ShimmerUpdater.exe")

        installed = False
        while not installed:
            install = False
            if not exists(UPD_PATH):
                log("Auto updater not installed. Installing...")
                install = True
            else:
                #check uncorrupted / latest version
                h256 = sha256()
                h256.update(open(UPD_PATH,'rb').read())
                hash = h256.hexdigest()
                try:
                    async with aiohttp.ClientSession() as session:
                        async with session.get("https://api.github.com/repos/loplxl/ShimmerUpdater/releases/latest") as resp3:
                            resp3.raise_for_status()
                            Uresp = await resp3.json()
                except Exception as e:
                    log("Failed to hash ShimmerUpdater" + e)
                    return
                expectedhash = Uresp["assets"][0]["digest"][7:]
                log("Current: " + hash)
                log("Expected: " + expectedhash)
                if str(hash) != str(expectedhash):
                    log("Auto updater outdated or corrupted. Installing...")
                    install = True
                else:
                    log("Auto updater not corrupted and up to date, proceeding...")
                    break
            break
            if install:
                async with aiohttp.ClientSession() as session:
                    async with session.get("https://github.com/loplxl/ShimmerUpdater/releases/latest/download/ShimmerUpdater.exe") as resp:
                        resp.raise_for_status()
                        with open(UPD_PATH, "wb") as f:
                            async for chunk in resp.content.iter_chunked(8192):
                                f.write(chunk)
            
            await asyncio.sleep(1) #wait 1s before loop to ensure everything is normal
        log("Auto updater is up to date")
        for process in gui.openSubprocesses:
            log(f"Terminating {process}")
            process.terminate()
        gui.destroy()
        ctypes.windll.shell32.ShellExecuteW(None,"open","cmd.exe",f'/k "{UPD_PATH}"',UPD_DIR,1)
        exit(0)

    def loadTweaks(self):
        self.basepath = TWEAKSP
        self.dirs = sorted([d for d in listdir(self.basepath) if isdir(join(self.basepath,d))],key=str.casefold)

    @cache
    def shrink(self, widget, width, size):
        text = max(widget.cget("text").splitlines(),key=len) + "." #add a tiny bit of extra length
        
        s = []
        low = max(1, size - 10)
        high = size
        best = low
        while low <= high:
            mid = (low + high) // 2
            #if debug:
            #    print(f"Testing: {mid}")
            font = ctk.CTkFont(size=mid)
            if font.measure(text) <= width:
                best = mid
                low = mid + 1
            else:
                high = mid - 1

            s = best
        widget.configure(font=ctk.CTkFont(size=s))

    def __init__(self):
        
        from logger.logger import ConsoleLogger
        self.logger = ConsoleLogger(master=self)
        global settingsPage
        from pages.settingsPage import settingsPage
        settingsPage.setupSettings(settingsPage,self)
        from pages.sidebar import sidebar
        global homePage
        from pages.homePage import homePage
        print("hello log viewer")
        self.CurrentVersion = version
        self.dirs = "loading"
        self.drive = drive
        print(f"Running from drive {self.drive}")
        if createTweaks:
            threading.Thread(target=self.loadTweaks, daemon=True).start()
        super().__init__(fg_color="#201d26")
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=0)  # sidebar (fixed)
        self.grid_columnconfigure(1, weight=1)  # main area (resizable)

        self.openSubprocesses = []
        self.currentTab = "initialising"
        #1250x700 on 1920x1080
        self.width = ceil(self.winfo_screenwidth()/1920*1250)
        self.height = ceil(self.winfo_screenheight()/1080*700)
        self.minsize(self.width,self.height)
        print(f"Allowing {self.width}x{self.height}")
        self.geometry(f"{self.width}x{self.height}+100+100") #+100+100 stops the gui from moving each time you open it
        try:
            if self.settings["peak_os_mode"]:
                self.title("Peak")
            else:
                self.title("Shimmer")
        except Exception:
            self.title("Shimmer")
        self.cachedFrames = {
            "home": None,
            "downloads": None,
            "tweaks": None,
            "tools": None,
            "about": None,
            "settings": None
        }
        self.homePage_init()
        self.cachedFrames["home"] = self.main_area.page
        self.sb = sidebar(master=self,createTweaks=createTweaks)
        self.sb.grid(row=0,column=0,sticky="ns")
        self.attributes("-topmost", True)
        self.after(10,lambda: self.attributes("-topmost", False))
    
    def homePage_init(self):
        if self.currentTab != "home":
            if self.currentTab == "initialising":
                self.main_area = ctk.CTkFrame(self, fg_color="transparent")
                self.main_area.grid_rowconfigure(0, weight=1)
                self.main_area.grid_columnconfigure(1, weight=1)
                self.main_area.grid(row=0,column=1,sticky="nsew")
            self.currentTab = "home"
            # hide page 
            for child in self.main_area.winfo_children():
                child.grid_forget()
            if self.cachedFrames["home"] is None:
                self.cachedFrames["home"] = homePage(master=self)

            # show home page
            self.main_area.page = self.cachedFrames["home"]
            self.main_area.page.grid(row=0,column=1,sticky="nsew")

    def downloadsPage_init(self):
        if self.currentTab != "downloads":
            from pages.downloadsPage import downloadsPage
            self.currentTab = "downloads"
            # hide page
            for child in self.main_area.winfo_children():
                child.grid_forget()
            
            if self.cachedFrames["downloads"] is None:
                self.cachedFrames["downloads"] = downloadsPage(master=self)
            
            # show downloads page
            self.main_area.page = self.cachedFrames["downloads"]
            self.main_area.page.grid(row=0,column=1,sticky="nsew")
    
    def tweaksPage_init(self):
        if self.currentTab != "tweaks":
            from pages.tweaksPage import tweaksPage
            self.currentTab = "tweaks"

            # hide page
            for child in self.main_area.winfo_children():
                child.grid_forget()

            if self.cachedFrames["tweaks"] is None:
                self.cachedFrames["tweaks"] = tweaksPage(master=self)
            
            # show tweaks page
            self.main_area.page = self.cachedFrames["tweaks"]
            self.main_area.page.grid(row=0,column=1,sticky="nsew")
    
    def toolsPage_init(self):
        if self.currentTab != "tools":
            from pages.toolsPage import toolsPage
            self.currentTab = "tools"
            # hide page
            for child in self.main_area.winfo_children():
                child.grid_forget()
            
            if self.cachedFrames["tools"] is None:
                self.cachedFrames["tools"] = toolsPage(master=self)
            
            # show tools page
            self.main_area.page = self.cachedFrames["tools"]
            self.main_area.page.grid(row=0,column=1,sticky="nsew")
     
    def quickaccessPage_init(self):
        if self.currentTab != "quickaccess":
            from pages.quickaccessPage import quickaccessPage
            self.currentTab = "quickaccess"
            # hide page
            for child in self.main_area.winfo_children():
                child.grid_forget()

            # show quickaccess page
            self.main_area.page = quickaccessPage(master=self)
            self.main_area.page.grid(row=0,column=1,sticky="nsew")

    def aboutPage_init(self):
        if self.currentTab != "about":
            from pages.aboutPage import aboutPage
            self.currentTab = "about"
            # hide page
            for child in self.main_area.winfo_children():
                child.grid_forget()
            
            if self.cachedFrames["about"] is None:
                self.cachedFrames["about"] = aboutPage(master=self)
            
            # show about page
            self.main_area.page = self.cachedFrames["about"]
            self.main_area.page.grid(row=0,column=1,sticky="nsew")
        
    def settingsPage_init(self):
        if self.currentTab != "settings":
            self.currentTab = "settings"
            # hide page
            for child in self.main_area.winfo_children():
                child.grid_forget()
            
            if self.cachedFrames["settings"] is None:
                self.cachedFrames["settings"] = settingsPage(master=self)
            
            # show settings page
            self.main_area.page = self.cachedFrames["settings"]
            self.main_area.page.grid(row=0,column=1,sticky="nsew")
    
def on_close(gui):
    try:
        gui.stop.set()
    except Exception:
        pass
    gui.destroy()
    for process in gui.openSubprocesses:
        print(f"Terminating {process}")
        process.terminate()
gui = newGUI()
gui.protocol("WM_DELETE_WINDOW", lambda: on_close(gui))
gui.mainloop()
