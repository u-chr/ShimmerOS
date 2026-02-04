import customtkinter as ctk
from PIL import Image
from utils import resource_path
from webbrowser import open as openLink
class aboutPage(ctk.CTkFrame):
    def __init__(self, master):
        sf = master.width/1250
        super().__init__(master=master.main_area, fg_color="transparent")
        self.aboutPage_image = ctk.CTkLabel(self,image=ctk.CTkImage(
                dark_image=Image.open(resource_path("assets\\about.png")),
                size=(sf*900,sf*315)),text="")
        self.aboutPage_image.pack(side="top", pady=(20,0))

        self.LinksTitle = ctk.CTkLabel(self, text="Links", font=ctk.CTkFont(size=28))
        self.LinksTitle.pack(side="top", pady=(9,4))

        #Github Link
        self.OSOGHFrame = ctk.CTkFrame(self, fg_color="transparent")

        self.GHNameLabel = ctk.CTkLabel(self.OSOGHFrame, text="GitHub:", font=ctk.CTkFont(size=16))
        self.GHLinkLabel = ctk.CTkLabel(self.OSOGHFrame, text="github.com/loplxl/ShimmerOS",
            font=ctk.CTkFont(size=16), cursor="hand2", text_color="#5555ff")

        self.GHNameLabel.pack(side="left", padx=(0,10))
        self.GHLinkLabel.pack(side="left")

        self.GHLinkLabel.bind("<Enter>", lambda e: e.widget.master.configure(text_color="#5555aa"))
        self.GHLinkLabel.bind("<Leave>", lambda e: e.widget.master.configure(text_color="#5555ff"))
        self.GHLinkLabel.bind("<Button-1>", lambda e: openLink("https://github.com/loplxl/ShimmerOS"))
        self.OSOGHFrame.pack(side="top", pady=(8,0))


        #Discord Link
        self.DCFrame = ctk.CTkFrame(self, fg_color="transparent")

        self.DCNameLabel = ctk.CTkLabel(self.DCFrame, text="Discord:", font=ctk.CTkFont(size=16))
        self.DCLinkLabel = ctk.CTkLabel(self.DCFrame, text="https://discord.gg/Tgc4Ka4FQ7",
            font=ctk.CTkFont(size=16), cursor="hand2", text_color="#5555ff")

        self.DCNameLabel.pack(side="left", padx=(0,10))
        self.DCLinkLabel.pack(side="left")

        self.DCLinkLabel.bind("<Enter>", lambda e: e.widget.master.configure(text_color="#5555aa"))
        self.DCLinkLabel.bind("<Leave>", lambda e: e.widget.master.configure(text_color="#5555ff"))
        self.DCLinkLabel.bind("<Button-1>", lambda e: openLink("https://discord.gg/Tgc4Ka4FQ7"))
        self.DCFrame.pack(side="top", pady=(5,0))

        self.creditsTitle = ctk.CTkLabel(self, text="Credits", font=ctk.CTkFont(size=28))
        self.creditsTitle.pack(side="top", pady=(15,4))

        self.creditsLabel1 = ctk.CTkLabel(self, text="Hickensa (SapphireOS/Tool) for being the main inspiration for uchr's development of " + ("Peak" if self.master.master.settings["peak_os_mode"] else "Shimmer") + " OS, and my development of this tool.", font=ctk.CTkFont(size=16), cursor="hand2",wraplength=sf*1020)
        self.creditsLabel1.bind("<Button-1>", lambda e: openLink("https://github.com/HickerDicker"))
        self.creditsLabel1.pack(side="top", pady=(8,0))

        self.creditsLabel2 = ctk.CTkLabel(self, text="Chr for making " + ("Peak" if self.master.master.settings["peak_os_mode"] else "Shimmer") + " OS!", font=ctk.CTkFont(size=16), cursor="hand2")
        self.creditsLabel2.bind("<Button-1>", lambda e: openLink("https://github.com/u2chr2"))
        self.creditsLabel2.pack(side="top", pady=(2,0))

        self.versionLabel = ctk.CTkLabel(self, text=f"Version: {self.master.master.CurrentVersion}", font=ctk.CTkFont(size=16))
        self.versionLabel.pack(side="bottom", pady=(2,10))
