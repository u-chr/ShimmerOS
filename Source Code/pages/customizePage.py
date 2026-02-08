import customtkinter as ctk
from PIL import Image
from utils import resource_path
from os import listdir
from pathlib import Path
from ctypes import windll
class customizePage(ctk.CTkFrame):
    def selectWallpaper(self,wallpaperLabel):
        self.assurance_label.configure(text="Setting new wallpaper...")
        self.hue_control.configure(state="disabled")
        image = wallpaperLabel.hue_image
        save_path = resource_path("assets/wallpaper.png")
        image.save(save_path)
        windll.user32.SystemParametersInfoW(20, 0, save_path, 0x01 | 0x02)
        self.hue_control.configure(state="normal")
        self.assurance_label.configure(text="Set new wallpaper!")
        self.after(1000,self.assurance_label.configure,text="")

    def changeHueText(self,shift):
        self.hue_label.configure(text=f"Hue Shift: {int(shift):03d}")
    def changeHue(self,shift):
        self.assurance_label.configure(text="Computing hue change...")
        self.after(30, self.hueShift, self.hue_control.get())
    def hueShift(self,shift):
        for child in self.wallpapers_sframe.winfo_children():
            old_image = child.image
            hsv = old_image.convert("HSV")
            h,s,v = hsv.split()
            h = h.point(lambda p: (p + int(shift)) % 256)
            new_image = Image.merge("HSV", (h, s, v)).convert("RGB")
            child.cget("image").configure(dark_image=new_image)
            child.hue_image = new_image
        self.assurance_label.configure(text="")
    def __init__(self, master):
        sf = master.width/1250
        super().__init__(master=master.main_area, fg_color="transparent")
        self.titleBar = ctk.CTkLabel(self, text="Customize (scroll down for more)", font=ctk.CTkFont(size=32,weight="bold"), bg_color="#1d1a23", height=50)
        self.titleBar.pack(side="top", fill="x")
        self.settings_bar = ctk.CTkFrame(self, height=sf*50, fg_color="#1d1a23", corner_radius=0)

        self.hue_label = ctk.CTkLabel(self.settings_bar, text="Hue Shift: 0")
        self.hue_control = ctk.CTkSlider(self.settings_bar, to=255, width=sf*250, command=self.changeHueText)
        self.hue_control.bind("<ButtonRelease-1>", self.changeHue)
        self.hue_control.set(0)
        self.hue_label.grid(row=0,column=0,padx=5,sticky="w")
        self.hue_control.grid(row=0,column=1,padx=5,sticky="w")

        self.assurance_label = ctk.CTkLabel(self.settings_bar, text="")
        self.assurance_label.grid(row=0,column=2,sticky="w",pady=20)

        self.settings_bar.grid_columnconfigure(0,weight=0)
        self.settings_bar.grid_columnconfigure(1,weight=1)
        self.settings_bar.grid_columnconfigure(2,weight=1)

        self.settings_bar.pack(side="top", fill="x")
        self.wallpapers_sframe = ctk.CTkScrollableFrame(self)
        wallpaper_path = resource_path("assets/wallpapers")
        for wallpaper in listdir(wallpaper_path):
            this_path = Path(wallpaper_path) / wallpaper
            display = Image.open(this_path)
            size = display.size
            scale_factor = 1010/size[0]
            img = Image.open(this_path)
            wallpaperDisplay = ctk.CTkLabel(self.wallpapers_sframe,image=ctk.CTkImage(dark_image=img,
                size=(size[0] * scale_factor, size[1] * scale_factor)),text="",cursor="hand2")
            wallpaperDisplay.image = img
            wallpaperDisplay.hue_image = img
            wallpaperDisplay.bind("<Button-1>",lambda e, wp = wallpaperDisplay: self.selectWallpaper(wp))
            wallpaperDisplay.pack(side="top",pady=5)
        self.wallpapers_sframe.pack(expand=True,fill="both")
                