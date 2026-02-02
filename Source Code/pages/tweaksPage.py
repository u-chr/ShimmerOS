import customtkinter as ctk
from os.path import join,abspath,exists,isdir
from os import listdir,getcwd
SOFTWARE_DIR = join(getcwd()[2:],"/Shimmer","Software")
from subprocess import Popen,check_output
from time import sleep
import threading
import json
import wmi

types = ["intel","nvidia","amd"]
gpumans = []
cpumans = []

c = wmi.WMI()
for cpu in c.Win32_Processor():
    name = cpu.Name.lower()
    for t in types:
        if t in name:
            cpumans.append(t)

for gpu in c.Win32_VideoController():
    name = gpu.Name.lower()
    for t in types:
        if t in name:
            gpumans.append(t)

print(f"Detected GPU: {gpumans}")
print(f"Detected CPU: {cpumans}")

class tweaksPage(ctk.CTkFrame):
    def rmbBind(self,widget,description,directory):
        widget.bind("<Button-3>",lambda e: self.helpbox(description,directory))
        for child in widget.winfo_children():
            self.rmbBind(child, description, directory)
    helpTLs = {}
    def helpbox(self, description, directory):
        if directory in self.helpTLs:
            helpTL = self.helpTLs[directory]
            helpTL.attributes("-topmost", True)
            helpTL.after(10,lambda: helpTL.attributes("-topmost", False))
            print("TL already open, taking top")
            return
        print("Creating new TL")
        helpTL = ctk.CTkToplevel(self, fg_color="#201d26")
        helpTL.geometry("400x200")
        helpTL.title(directory)
        def on_close(d=directory):
            if d in self.helpTLs:
                self.helpTLs[d].destroy()
                del self.helpTLs[d]
        helpTL.protocol("WM_DELETE_WINDOW",on_close)
        self.helpTLs[directory] = helpTL
        helpLabel = ctk.CTkLabel(helpTL,text=description,wraplength=395)
        helpLabel.pack(side="top",fill="x")
        helpTL.attributes("-topmost", True)
        helpTL.after(10,lambda: helpTL.attributes("-topmost", False))
    def __init__(self, master):
        super().__init__(master=master.main_area, fg_color="transparent")
        self.titleBar = ctk.CTkLabel(self, text="Tweaks", font=ctk.CTkFont(size=32,weight="bold"), bg_color="#1d1a23", height=50)
        self.titleBar.pack(side="top", fill="x")

        #create scrollable sidebar frame to display all the dirs
        warningFrame = ctk.CTkFrame(self, fg_color="#232029")
        warningLabel1 = ctk.CTkLabel(warningFrame,text="⚠️ WARNING ⚠️",font=ctk.CTkFont(size=32))
        warningLabel1.pack(side="top",pady=(45,0))
        warningLabel2 = ctk.CTkLabel(warningFrame,text="Do not blindly apply tweaks that you dont know what they do. Only follow official guides.\nWe are not responsible for any damage (however unlikely) you cause upon yourself.",font=ctk.CTkFont(size=22),wraplength=master.width/1250*950)
        warningLabel2.pack(side="top",pady=(15,0))
        def proceed():
            warningFrame.destroy()
            self.dirbar.pack(side="left", padx=8, pady=8, fill="both", expand=True)
        proceedBtn = ctk.CTkButton(warningFrame,text="I understand the risks",fg_color="#33ff33",hover_color="#00ff00",command=proceed,text_color="#000000")
        proceedBtn.pack(side="top",pady=25)
        returnBtn = ctk.CTkButton(warningFrame,text="Return Home",fg_color="#ff3333",hover_color="#ff0000",command=self.master.master.homePage_init,text_color="#000000")
        returnBtn.pack(side="top",pady=(10,25))
        warningFrame.pack(fill="both",expand=True)

        
        self.dirbar = ctk.CTkScrollableFrame(self, fg_color="#232029")
        r=0
        c=0
        while not master.dirs or master.dirs == "loading":
            sleep(0.01)
        
        bpath = self.master.master.basepath
        global DATA_DIR
        DATA_DIR = join(SOFTWARE_DIR,"tweakdata.json")
        global data
        if not exists(DATA_DIR):
            print("Creating tweak data")
            with open(DATA_DIR,'w') as f:
                data = {
                    "Animations_Support": 0,
                    "Bluetooth_Support": 1,
                    "Clipboard_History": 0,
                    "Core_Isolation": 0,
                    "DCOM": 1,
                    "Filesystem_Encryption": 0,
                    "Force_FSE": 0,
                    "MPO": 1,
                    "Hyper-V": 0,
                    "Intel_TSX": 1,
                    "Internet_Optimizations": 0,
                    "NoLazyMode": 0,
                    "Notification_Center": 1,
                    "Notifications": 0,
                    "Power_Saving": 0,
                    "Printing_Support": 0,
                    "Serial_Port": 1,
                    "Start_Menu": 1,
                    "SystemProfile_Tweaks": 0,
                    "Transparency_Effects": 0,
                    "UAC": 0,
                    "VPN_Support": 1,
                    "Wi-Fi_Support": 1,
                    "Windows_Update": 1,
                    "Virtual_Disk_Support": 0,
                    "HAGS": 0
                }
                json.dump(data,f,indent=4)
        else:
            with open(DATA_DIR,'r') as f:
                data = json.load(f)
        for directory in master.dirs:
            filesdir = join(bpath,directory)
            files = listdir(filesdir)
            print("Loading " + str(filesdir))

            try:
                with open(join(filesdir,"help.json"),'r') as f:
                    helpdata = json.load(f)
                    description = helpdata["description"]
                    file = helpdata["target"]
            except Exception as e:
                file = str(e)
            try:
                with open(join(filesdir,"help.json"),'r') as f:
                    requirement = helpdata["requirement"]
            except Exception as e:
                requirement = None
            try:
                with open(join(filesdir,"help.json"),'r') as f:
                    CPUReq = helpdata["cpu"]
            except Exception as e:
                CPUReq = "none"
            if not (CPUReq == "none" or CPUReq in cpumans):
                continue

            try:
                with open(join(filesdir,"help.json"),'r') as f:
                    GPUReq = helpdata["gpu"]
            except Exception as e:
                GPUReq = "none"
            if not (GPUReq == "none" or GPUReq in cpumans):
                continue

            requirementNotMet = False
            if requirement == "nsudo" and not exists(join(SOFTWARE_DIR,"quickaccess","NSudo.exe")):
                requirementNotMet = True
            localFrame = ctk.CTkFrame(self.dirbar,cursor="hand2")
            localFrame.nameLabel = ctk.CTkLabel(localFrame, text=directory.replace("_"," "), font=ctk.CTkFont(size=24))
            localFrame.nameLabel.pack(side="left", padx=[10,0], pady=10)
            if requirementNotMet: 
                localFrame.nameLabel.configure(text=f"not met requirement for {directory.replace("_"," ")}: {requirement} download it in downloads page, then reopen app", font=ctk.CTkFont(size=20))
            else:
                if "on.bat" in files and "off.bat" in files:
                    localFrame.switchvar = ctk.StringVar()
                    localFrame.switch = ctk.CTkSwitch(localFrame,width=116,text=None,variable=localFrame.switchvar,onvalue="on",offvalue="off",progress_color="transparent",
                                command=lambda d=directory, f=localFrame: threading.Thread(target=self.ONOFFtweakClicked,args=(d,f),daemon=True).start())
                    try:
                        s = data[directory]
                        if s:
                            localFrame.switch.select()
                            localFrame.switch.configure(text="Enabled",fg_color="#55bb55",text_color="#55ff55",text_color_disabled="#55ff55")
                        else:
                            localFrame.switch.configure(text="Disabled",fg_color="#3865a8",text_color="#5599ff",text_color_disabled="#5599ff")
                    except Exception:
                        print(f"Stored tweaks data does not contain information on {directory}.")
                        localFrame.switch.configure(text="Unset",fg_color="#bb5555",text_color="#ff5555",text_color_disabled="#ff5555")
                    localFrame.switch.pack(side="right",padx=(0,8))
                    self.rmbBind(localFrame,description,join(filesdir,file))
                elif "action.bat" in files:
                    localFrame.onButton = ctk.CTkButton(localFrame, text="Apply", fg_color="#477843", hover_color="#376833", command=lambda d=directory, f=localFrame: self.SingleBattweakclicked(d,f), width=116, font=ctk.CTkFont(size=16))
                    localFrame.onButton.pack(side="right",padx=8)
                    self.rmbBind(localFrame,description,join(filesdir,file))
                else:
                    localFrame.errorLabel = ctk.CTkLabel(localFrame, text=file)
                    localFrame.errorLabel.pack(side="right",padx=8)
            localFrame.grid(row=r, column=c, sticky="nsew", padx=3, pady=6)
            self.dirbar.grid_columnconfigure(c, weight=1)
            if not requirementNotMet:
                master.shrink(localFrame.nameLabel, round((master.width/1250*1030-141)/2) - 116, 30)
            else:
                master.shrink(localFrame.nameLabel, round((master.width/1250*1030)/2), 30)
            c += 1
            if c > 1:
                c = 0
                r += 1

    def colourlabel(self,proc,label,colour):
        proc.wait()
        self.after(0,lambda: label.configure(text_color=colour))
        label.master.switch.configure(state="normal")
    
    def ONOFFtweakClicked(self,directory,frame):
        frame.switch.configure(state="disabled")
        state = frame.switchvar.get()
        if state == "on":
            frame.switch.configure(text="Enabled",fg_color="#55bb55",text_color="#55ff55",text_color_disabled="#55ff55")
            with open(DATA_DIR,'w') as f:
                data[directory] = 1
                json.dump(data,f,indent=4)
        else:
            frame.switch.configure(text="Disabled",fg_color="#3865a8",text_color="#5599ff",text_color_disabled="#5599ff")
            with open(DATA_DIR,'w') as f:
                data[directory] = 0
                json.dump(data,f,indent=4)
        path = abspath(join(self.master.master.basepath, directory, f"{state}.bat"))
        print(f"Running |{path}|.")
        self.colourlabel(Popen([f'{path}'], shell=True, text=True),frame.nameLabel,("#aaffaa"))
    def regTweakClicked(self,directory,frame):
        print(f"Running |{directory}|.")
        proc = Popen(["regedit","/s",directory], shell=True)
        proc.wait()
        frame.nameLabel.configure(text_color="#aaffaa")
    def ps1TweakClicked(self,directory,frame):
        print(f"Running |{directory}|.")
        cmd = ["powershell.exe", '-ExecutionPolicy', 'Unrestricted', directory]
        proc = Popen(cmd, shell=True)
        proc.wait()
        frame.nameLabel.configure(text_color="#aaffaa")
    def SingleBattweakclicked(self,directory,frame):
        path = abspath(join(self.master.master.basepath, directory, f"action.bat"))
        print(f"Running |{path}|.")
        proc = Popen([f'{path}'], shell=True, text=True)
        proc.wait()
        frame.nameLabel.configure(text_color="#aaffaa")
