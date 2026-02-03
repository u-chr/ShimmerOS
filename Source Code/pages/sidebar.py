import customtkinter as ctk
from PIL import Image
from utils import resource_path
import threading
import asyncio
class sidebar(ctk.CTkFrame):
    def __init__(self,master,createTweaks):
        width=master.width/1250*220
        super().__init__(master=master,fg_color="#27242d",width=width)
        self.icon = ctk.CTkLabel(
            self,
            image=ctk.CTkImage(
                dark_image=Image.open(resource_path("assets\\icon.png")),
                size=(width/220*180,width/220*180)),
            text=""
        )
        self.pack_propagate(False)
        self.icon.pack(side="top", anchor="n")

        self.settings_icon = ctk.CTkButton(
            self,
            image=ctk.CTkImage(
                dark_image=Image.open(resource_path("assets\\settings.png")),
                size=(24, 24)
            ),
            text="",
            width=24,
            height=24,
            fg_color="transparent",
            hover_color="#27242d",
            command=master.settingsPage_init)

        self.settings_icon.place(x=0, y=0)

        
        #7 buttons take up 315 px
        #315 : 650 with 1920
        #315/650 of height dedicated to buttons
        btnheight = round(master.height * (315/650)/8)
        print(f"sidebar buttons allowed {btnheight}px height")

        #create buttons
        homeButton = ctk.CTkButton(self, text="Home", command=master.homePage_init, fg_color="#1f1c25", hover_color="#23202b", font=ctk.CTkFont(size=24),height=btnheight)
        downloadsButton = ctk.CTkButton(self, text="Downloads", command=master.downloadsPage_init, fg_color="#1f1c25", hover_color="#23202b", font=ctk.CTkFont(size=24),height=btnheight)
        toolsButton = ctk.CTkButton(self, text="Tools", command=master.toolsPage_init, fg_color="#1f1c25", hover_color="#23202b", font=ctk.CTkFont(size=24),height=btnheight)
        quickaccessButton = ctk.CTkButton(self, text="Quick Access", command=master.quickaccessPage_init, fg_color="#1f1c25", hover_color="#23202b", font=ctk.CTkFont(size=24),height=btnheight)
        aboutButton = ctk.CTkButton(self, text="About", command=master.aboutPage_init, fg_color="#1f1c25", hover_color="#23202b", font=ctk.CTkFont(size=24),height=btnheight)
        
        logsButton = ctk.CTkButton(self, text="View current logs", command=lambda: threading.Thread(target=asyncio.run(master.showlogs()),daemon=True).start(), fg_color="#1f1c25", hover_color="#23202b", font=ctk.CTkFont(size=20),height=btnheight)
        updateButton = ctk.CTkButton(self, text="Check for updates", command=lambda: threading.Thread(target=asyncio.run(master.AutoUpdater()),daemon=True).start(), fg_color="#1f1c25", hover_color="#23202b", font=ctk.CTkFont(size=20),height=btnheight)
        
        master.shrink(homeButton,width-20,24)
        master.shrink(downloadsButton,width-20,24)
        master.shrink(toolsButton,width-20,24)
        master.shrink(quickaccessButton,width-20,24)
        master.shrink(aboutButton,width-20,24)
        master.shrink(logsButton,width-20,24)
        master.shrink(updateButton,width-20,24)
        
        homeButton.pack(side="top", anchor="n", padx=5, pady=3, fill='x')
        downloadsButton.pack(side="top", anchor="n", padx=5, pady=3, fill='x')
        if createTweaks:
            tweaksButton = ctk.CTkButton(self, text="Tweaks", command=master.tweaksPage_init, fg_color="#1f1c25", hover_color="#23202b", font=ctk.CTkFont(size=24),height=btnheight)
            master.shrink(tweaksButton,width-20,24)
            tweaksButton.pack(side="top", anchor="n", padx=5, pady=3, fill='x')
        toolsButton.pack(side="top", anchor="n", padx=5, pady=3, fill='x')
        quickaccessButton.pack(side="top", anchor="n", padx=5, pady=3, fill='x')
        aboutButton.pack(side="top", anchor="n", padx=5, pady=3, fill='x')
        updateButton.pack(side="bottom", anchor="s", padx=5, pady=3, fill='x')
        logsButton.pack(side="bottom", anchor="s", padx=5, pady=(3,6), fill='x')