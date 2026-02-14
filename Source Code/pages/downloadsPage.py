downloads = { #category / [name to display,module location,font size]
    ("Shimmer quick access"): [
        ["$xAuto Gpu Affinity","quickaccess.aga",14], #$x means that getURL is a procedure, not a function
        ["Autoruns","quickaccess.autoruns",20],
        ["GoInterruptPolicy","quickaccess.goip",15],
        ["$xNSudo","quickaccess.nsudo",22],
        ["Dynamic Timer Resolution","quickaccess.dynamictr",20]
    ],
    "Firefox based browsers": [
        ["⭐ Tor","firefox.tor",24],
        ["⭐ Mullvad","firefox.mullvad",22],
        ["Zen","firefox.zen",24],
        ["Waterfox","firefox.waterfox",22],
        ["Firefox","firefox.firefox",22],
        ["Librewolf","firefox.librewolf",22],
        ["Floorp","firefox.floorp",22]
    ],
    "Chromium based browsers": [
        ["⭐ Brave","chromium.brave",22],
        ["⭐ Helium","chromium.helium",22],
        ["Google Chrome","chromium.chrome",20],
        ["Vivaldi","chromium.vivaldi",22],
        ["Ungoogled\nChromium","chromium.ungoogled",14],
        ["Epic Privacy\nBrowser","chromium.epic",14],
        ["Yandex","chromium.yandex",22],
        ["Arc","chromium.arc",24]
    ],
    "Communication": [
        ["⭐ Signal","utility.signal",22],
        ["⭐ Stoat","utility.stoat",22],
        ["Legcord","utility.legcord",22],
        ["Discord","utility.discord",22],
        ["Vencord","utility.vencord",22]
    ],
    "Gaming": [
        ["Steam","utility.steam",24],
        ["Epic Games","utility.epic",22],
        ["BakkesMod","utility.bakkesmod",24],
        ["Prism Launcher","utility.prism",20],
        ["Lunar Client","utility.lunar",20],
        ["MegaHack v9","utility.mhv9",20],
        ["MegaHack v8","utility.mhv8",20],
        ["MegaHack v7","utility.mhv7",20],
        ["Geode","utility.geode",22],
        ["Xbox App","utility.xbox",20]
    ],
    "Utilities": [
        ["⭐ CapFrameX","utility.cfx",20],
        ["⭐ Mullvad VPN","utility.mullvadvpn",20],
        ["⭐ AB Download Manager","utility.abdm",18],
        ["⭐ LM Studio","utility.lmstudio",20],
        ["Malwarebytes","utility.mwb",20],
        ["Bleachbit","utility.bleachbit",21],
        ["qBittorrent","utility.qbt",20],
        ["Free Download\nManager","utility.fdm",16],
        ["WebView2","utility.webview2",20]
    ],
    "Media": [
        ["⭐ VLC","utility.vlc",24],
        ["⭐ OBS Studio","utility.obs",20],
        ["⭐ JPEGView","utility.jpegview",22],
        ["⭐ Davinci Resolve","utility.dvr",20],
        ["⭐ Lightshot","utility.lightshot",21],
        ["ShareX","utility.sharex",22],
        ["Medal","utility.medal",22],
        ["HandBrake","utility.handbrake",20]
    ],
    "Customisation": [
        ["⭐ f.lux","utility.flux",22],
        ["Rainmeter","utility.rainmeter",21],
        ["Windhawk","utility.windhawk",20],
        ["StartAllBack","utility.startallback",18]
    ],
    "Coding": [
        ["rustup.rs","utility.rustup",20],
        ["MinGW MSYS2","utility.mgwmsys2",20],
        ["Latest Python","utility.python",20]
    ],
    "Text Editors": [
        ["⭐ VSCodium","utility.vscodium",20],
        ["⭐ Neovim","utility.neovim",20],
        ["Visual Studio Code","utility.vscode",16],
        ["Notepad++","utility.nppp",22],
        ["Sublime Text","utility.sublimetext",20],
        ["Atom","utility.atom",24],
        ["JetBrains CLion","utility.jetbrainsclion",20],
        ["JetBrains DataGrip","utility.jetbrainsdatagrip",20],
        ["JetBrains DataSpell","utility.jetbrainsdataspell",20],
        ["JetBrains GoLand","utility.jetbrainsgoland",20],
        ["JetBrains\nIntelliJ IDEA","utility.jetbrainsijidea",15],
        ["JetBrains PhpStorm","utility.jetbrainsphp",20],
        ["JetBrains PyCharm","utility.jetbrainspycharm",20],
        ["JetBrains Rider","utility.jetbrainsrider",20],
        ["JetBrains\nReSharper Ultimate","utility.jetbrainsrsu",15],
        ["JetBrains RubyMine","utility.jetbrainsrubymine",20],
        ["JetBrains RustRover","utility.jetbrainsrustrover",20],
        ["JetBrains TeamCity","utility.jetbrainsteamcity",20],
        ["JetBrains WebStorm","utility.jetbrainsweb",20]
    ],
    "Hardware Tools": [
        ["⭐ Display Driver\nUninstaller","utility.ddu",14],
        ["⭐ Equilazer APO","utility.eqapo",20],
        ["SoundSwitch","utility.soundswitch",20],
        ["Voicemeeter Banana","utility.vmbanana",20],
        ["CPU-Z","utility.cpuz",24],
        ["GPU-Z","utility.gpuz",24],
        ["ASRock Timing\nConfigurator","utility.asrocktc",14],
        ["Custom Resolution\nUtility","utility.cru",14],
        ["MoreClockTool","utility.mct",19],
        ["Radeon Software\nSlimmer","utility.rsslimmer",14],
        ["NVCleanStall","utility.nvcs",20],
        ["CrystalDiskInfo","utility.cdinfo",20],
        ["GUI SCEWIN","utility.guiscewin",20],
        ["RawAccel","utility.rawaccel",20]
    ],
    "System Tools": [
        ["⭐ Bulk Crap\nUninstaller","utility.bcu",17],
        ["⭐ Everything Search","utility.everything",18],
        ["Process Lasso","utility.processlasso",19],
        ["Revo Uninstaller","utility.revouninstaller",17],
        ["WinRAR","utility.winrar",22],
        ["Powershell 7","utility.powershell",20],
        ["Teracopy","utility.teracopy",22],
        ["WizTree","utility.wiztree",22],
        ["AutoHotkey v2.0","utility.ahk2",20],
        ["AutoHotkey v1.1","utility.ahk1",20]
    ]
}
computed_downloads = {}
categoryFrames = []
import customtkinter as ctk
import threading
import asyncio
import aiohttp
import importlib
import ssl
from time import sleep
from utils import resource_path
ssl_ctx = ssl.create_default_context(cafile=resource_path("dependencies\\cacert.pem"))

class downloadsPage(ctk.CTkFrame):
    async def completeDownload(self,progressbar,appFrame,msg="Complete", text_color="#55ff55"):
        completeLabel = ctk.CTkLabel(appFrame, text=msg, text_color=text_color, font=ctk.CTkFont(size=20))
        self.master.master.shrink(completeLabel,progressbar.winfo_width(),20)
        self.after(0,progressbar.destroy)
        completeLabel.grid(row=0,column=1,padx=(0,10))
        if msg == "Error":
            await asyncio.sleep(3)
            self.after(0,completeLabel.destroy)
            print(f"attempting to resummon {appFrame.application[1]}")
            btn = ctk.CTkButton(appFrame, text="Download", width=round(w/4), font=ctk.CTkFont(size=16))
            btn.configure(command=lambda: self.download(btn,appFrame,appFrame.application[1]))
            self.master.master.shrink(btn,round(appFrame.winfo_width()/4),size=16)
            btn.grid(row=0,column=1,padx=(0,5),sticky="e")
    async def procedureWorker(self,app,btn):
        p = importlib.import_module(f"downloads.{app[1]}")
        await p.getURL(self,btn,app[1],w)
    def download(self,btn,appFrame,name):
        progressbar = ctk.CTkProgressBar(appFrame,width=round(w/4))
        self.after(0,btn.destroy)
        progressbar.set(0)
        app = importlib.import_module(f"downloads.{name}")
        progressbar.grid(row=0,column=1,padx=(0,10),sticky="e")

        async def async_download(url,path,progressbar):
            print(f"attempting to download from {url} to {path}")
            lastUpdateFrac = 0
            async def write(f,chunk):
                nonlocal lastUpdateFrac
                f.write(chunk)
                if total:
                    frac = downloaded/total
                    if frac-lastUpdateFrac >= 0.01 and frac <= 2: #only update ui every 2% downloaded
                        threading.Thread(target=lambda: self.after(0,progressbar.set,frac), daemon=True).start()
                        lastUpdateFrac = frac
            try:
                async with aiohttp.ClientSession() as session:
                    async with session.get(url,ssl=ssl_ctx,timeout=360000) as resp:
                        resp.raise_for_status()
                        total = resp.content_length or 0
                        downloaded = 0
                        with open(path, "wb") as f:
                            async for chunk in resp.content.iter_chunked(8192):
                                downloaded += len(chunk)
                                await write(f,chunk)
            except Exception as e:
                print(f"Error during download: {e}")
                await self.completeDownload(progressbar,progressbar.master,msg="Error",text_color="#ff5555")
                return
            self.after(0,lambda: asyncio.run(self.completeDownload(progressbar,progressbar.master)))
        async def continuation(url,path):
            threading.Thread(target=lambda: asyncio.run(async_download(url,path,progressbar)), daemon=True).start()
        threading.Thread(target=lambda: asyncio.run(app.getURL(ssl_ctx,continuation,progressbar,self.completeDownload)), daemon=True).start()
        
    def __init__(self, master):
        print("initialising downloads")
        super().__init__(master=master.main_area, fg_color="transparent")
        shrink = master.shrink
        self.titleBar = ctk.CTkLabel(self, text="Downloads (downloads go to downloads folder)", font=ctk.CTkFont(size=32,weight="bold"), bg_color="#1d1a23", height=50)
        shrink(self.titleBar,round(master.width/1250*1020),32)
        self.titleBar.pack(side="top", fill="x", pady=(0,5))
        self.scrollableDlFrame = ctk.CTkScrollableFrame(self, fg_color="#201d26")
        global w
        w = round((master.width-master.sb.winfo_width()-100)/4)
        templabel = ctk.CTkButton(self,text="Download")
        shrink(templabel,round(w/4),20)
        stdDLFont = templabel.cget("font")
        print(f"allowing download width of {w}")
        def search(args=None):
            criteria = self.searchBar.get().replace(" ","").strip().lower()
            print(f"Searching for '{criteria}'")
            self.scrollableDlFrame._parent_canvas.yview_moveto(0)
            for categoryFrame in categoryFrames:
                visible_items = False
                categoryFrame.pack_forget()
                row = 1
                column = 0
                for widget in categoryFrame.winfo_children():
                    if isinstance(widget,ctk.CTkFrame):
                        appName = widget.appNameLabel.cget("text").replace("\n","").replace(" ","").replace("⭐","").strip().lower()
                        print(f"Comparing {appName} with {criteria}")
                        if criteria in appName:
                            print("^ Matched!")
                            widget.grid(row=row,column=column,padx=5,pady=5,sticky="ew")
                            widget.grid_propagate(False)
                            widget.configure(width=w,height=40)
                            visible_items = True
                            column += 1
                            if column % 4 == 0:
                                row += 1
                                column = 0
                        else:
                            widget.grid_forget()
                if visible_items:
                    categoryFrame.pack(pady=10)
        self.searchFrame = ctk.CTkFrame(self)
        self.searchFrame.grid_columnconfigure(0,weight=1)
        self.searchFrame.grid_columnconfigure(0,weight=0)
        self.searchButton = ctk.CTkButton(self.searchFrame,text="Search",
                                          font=ctk.CTkFont(size=round(self.titleBar.cget("font").cget("size")/5*3)),
                                          height=30, width=round(master.width/1250*150), command=search)
        self.searchBar = ctk.CTkEntry(self.searchFrame, placeholder_text="Search",font=self.searchButton.cget("font"), bg_color="#1d1a23", height=30, width=round(master.width/1250*850))
        self.searchBar.grid(row=0,column=0,padx=5,pady=5,sticky="ew")
        self.searchButton.grid(row=0,column=1)
        self.searchBar.bind("<Return>",command=search)
        async def load_app(category,index,app,categoryFrame):
            row = index // 4 + 1
            column = index % 4
            appFrame = ctk.CTkFrame(categoryFrame,height=40,width=w)
            appFrame.application = app
            appFrame.grid_propagate(False)
            appFrame.grid_columnconfigure(0, weight=1)  # space for label
            appFrame.grid_columnconfigure(1, weight=0)  # button column
            appFrame.grid_rowconfigure(0, weight=1)  # button column

            isProcedure = True if app[0].startswith("$x") else False
            appFrame.appNameLabel = ctk.CTkLabel(appFrame, text=app[0] if not isProcedure else app[0][2:], font=ctk.CTkFont(size=app[2]), text_color="#ffff00" if app[0].startswith("⭐") else "#ffffff")
            threading.Thread(target=shrink,args=(appFrame.appNameLabel,round(w/4*3)-20,app[2]),daemon=True).start()
            appDownloadButton = ctk.CTkButton(appFrame, text="Download", width=round(w/4), font=stdDLFont)
            if isProcedure:
                appDownloadButton.configure(command=lambda app=app, btn=appDownloadButton: threading.Thread(target=lambda: asyncio.run(self.procedureWorker(app,btn)), daemon=True).start())
            else:
                appDownloadButton.configure(command=lambda app=app, btn=appDownloadButton: self.download(btn,btn.master,app[1]))
            appFrame.appNameLabel.grid(row=0,column=0,sticky="ew")
            appDownloadButton.grid(row=0,column=1,padx=(0,5),sticky="e")
            computed_downloads[category][app[1]][0].set()
            computed_downloads[category][app[1]][1] = [row,column,appFrame]
        for category,applications in downloads.items():
            categoryFrame = ctk.CTkFrame(self.scrollableDlFrame, fg_color="transparent")
            categoryFrames.append(categoryFrame)
            categoryTitle = ctk.CTkLabel(categoryFrame, text=category + "\n──────────────────────────", font=ctk.CTkFont(size=21))
            categoryTitle.grid(row=0, column=0, pady=(0,5), columnspan=5)
            computed_downloads[category] = {}
            for index,app in enumerate(applications):
                event = threading.Event()
                computed_downloads[category][app[1]] = [event,None]
                asyncio.run(load_app(category,index,app,categoryFrame))
            categoryFrame.pack(pady=10)
        for cat,apps in computed_downloads.items():
            for key,app in apps.items():
                if isinstance(app[0],threading.Event):
                    try:
                        app[0].wait()
                    except Exception as e:
                        print(e)
                        pass
                app[1][2].grid(row=app[1][0],column=app[1][1],padx=5,pady=5)
        self.searchFrame.pack(side="top", fill="x", padx=5,pady=2)
        self.scrollableDlFrame.pack(side="top",fill="both",expand=True)
        
