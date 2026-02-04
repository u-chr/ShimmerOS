import customtkinter as ctk
from PIL import Image
from utils import resource_path
class homePage(ctk.CTkFrame):
    def __init__(self, master):
        sf = master.width/1250
        super().__init__(master=master.main_area, fg_color="transparent")
        self.homePage_image = ctk.CTkLabel(
            self,image=ctk.CTkImage(
                dark_image=Image.open(resource_path("assets\\" + ("peak" if self.master.master.settings["peak_os_mode"] else "") + "options.png")),
                size=(sf*900,sf*315)),text="")
        self.homePage_label = ctk.CTkLabel(self, text="Welcome to Peak OS!\nIn this software, you can get downloads, tweaks and tools.\n\nThanks for using Peak OS and if you run into any issues, please contact us on GitHub.\nMore info on the about page." if self.master.master.settings["peak_os_mode"] else "Welcome to Shimmer OS!\nIn this software, you can get downloads, tweaks and tools.\n\nThanks for using Shimmer OS and if you run into any issues, please contact us on GitHub.\nMore info on the about page.",
            font=ctk.CTkFont(size=23),wraplength=sf*950)
        self.homePage_image.pack(side="top", pady=(20,14))
        self.homePage_label.pack(side="top",padx=10)