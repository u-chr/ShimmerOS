import customtkinter as ctk
from utils import resource_path
from os import listdir,path
import json
import importlib

class toolsPage(ctk.CTkFrame):
    def apply(self,master,module):
        mod = importlib.import_module(f"tools.{module}")
        mod.apply(master)
    def revert(self,master,module,btn):
        mod = importlib.import_module(f"tools.{module}")
        mod.default(master,btn)
    def __init__(self, master):
        super().__init__(master=master.main_area, fg_color="transparent")
        self.titleBar = ctk.CTkLabel(self, text="Tools", font=ctk.CTkFont(size=32,weight="bold"), bg_color="#1d1a23", height=50)
        self.titleBar.pack(side="top", fill="x")

        self.toolsFrame = ctk.CTkFrame(self, fg_color="transparent")
        self.toolsFrame.pack(side="top", fill="both", expand=True)
        #auto timer res
        
        TOOLS_DIR = resource_path("tools\\")
        self.frames = []
        w = round((master.width-master.sb.winfo_width()-24)/2)
        print(f"giving tools frames width {w}")
        for dir in listdir(TOOLS_DIR):
            if dir != "__pycache__" and not dir.endswith(".py"):
                try:
                    with open(path.join(TOOLS_DIR,dir,"help.json")) as f:
                        helpdata = json.load(f)
                        Frame = ctk.CTkFrame(self.toolsFrame, width=w, height=220, corner_radius=20)
                        Frame.pack_propagate(False)
                        Label = ctk.CTkLabel(Frame, text=dir.replace("_"," ").lstrip("!"), pady=6)
                        master.shrink(Label,1,helpdata["titlesize"])
                        Label.configure(font=ctk.CTkFont(size=Label.cget("font").cget("size")-4,weight="bold"))
                        Label.pack(side="top")
                        Description = ctk.CTkLabel(Frame, text=helpdata["description"],bg_color="transparent", justify="center")
                        Description.pack(side="top", pady=(5,10))
                        master.shrink(Description,w,helpdata["descriptionsize"])
                        BtnContainer = ctk.CTkFrame(Frame, fg_color="transparent", bg_color="transparent")
                        ApplyBtn = ctk.CTkButton(BtnContainer, text="Apply", font=ctk.CTkFont(size=16), fg_color="#00aa00", hover_color="#006600", width=round(w/4), command=lambda helpdata=helpdata: self.apply(self.master.master,helpdata["toolname"]))
                        ApplyBtn.grid(row=0, column=0, padx=round(w/9), pady=10)
                        if helpdata["defaultExists"] == "yes":
                            DefaultBtn = ctk.CTkButton(BtnContainer, text="Default", font=ctk.CTkFont(size=16) , fg_color="#aa0000", hover_color="#660000", width=round(w/4))
                            DefaultBtn.configure(command=lambda helpdata=helpdata: self.revert(self.master.master,helpdata["toolname"],DefaultBtn))
                            DefaultBtn.grid(row=0, column=1, padx=round(w/9), pady=10)
                        BtnContainer.grid_columnconfigure(0, weight=1)
                        BtnContainer.pack(side="top")

                        Frame.rowconfigure(0, weight=1)
                        self.frames.append(Frame)
                except FileNotFoundError:
                    print(f"{dir} has no help.json")
                except Exception as e:
                    print(f"unexpected error loading {dir} tool\n" + str(e))
        r=0
        c=0
        for frame in self.frames:
            frame.grid(row=r, column=c, sticky="nsew", padx=6, pady=6)
            c += 1
            if c > 1:
                c = 0
                r += 1
                