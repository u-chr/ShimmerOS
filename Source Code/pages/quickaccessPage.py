import customtkinter as ctk
from os import getcwd,listdir,mkdir
from os.path import join,exists
from subprocess import Popen, DETACHED_PROCESS, CREATE_NEW_PROCESS_GROUP, CREATE_NEW_CONSOLE

names = {
    "autoruns.exe": ("Autoruns",22),
    "GoInterruptPolicy.exe": ("GoInterruptPolicy",20),
    "NSudo.exe": ("NSudo",22),
    "AutoGpuAffinity": ("Auto Gpu Affinity",20,"AutoGpuAffinity\\AutoGpuAffinity.exe"),
    "dynamic-timer-resolution.exe": ("Dynamic Timer Resolution",20,"dynamic-timer-resolution")
}

extras = {
    "USB Latency Analyzer": [["cmd","/c","powershell","-NoExit","-NoProfile","-ExecutionPolicy","Bypass","-Command","irm https://tools.mariusheier.com/cpudirect.ps1 | iex"],20],
    "Measure Timer Resolution": [[f"{getcwd()[:2]}/Shimmer/Software/_internal/TimerResolution/MeasureSleep.exe"],20]
}
class quickaccessPage(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master=master.main_area, fg_color="transparent")
        self.titleBar = ctk.CTkLabel(self, text="Quick Access", font=ctk.CTkFont(size=32,weight="bold"), bg_color="#1d1a23", height=50)
        self.titleBar.pack(side="top", fill="x", pady=(0,5))
        folderLoc = join(getcwd()[:2] + "\\","Shimmer","Software","quickaccess")
        if not exists(folderLoc):
            mkdir(folderLoc)
            downloadedApps = []
        else:
            downloadedApps = listdir(folderLoc)

        launchFrame = ctk.CTkFrame(self, fg_color="transparent")
        column = -1
        row = 0
        for app in downloadedApps:
            print(f"Adding {app}")
            column += 1
            if column % 4 == 0:
                row += 1
                column = 0

            appFrame = ctk.CTkFrame(launchFrame)
            appFrame.grid_propagate(False)

            w = round((master.width/1250*1020-35)/4)
            appFrame.configure(height=40,width=w)

            appFrame.grid_columnconfigure(0, weight=1)
            appFrame.grid_rowconfigure(0, weight=1)

            data = names[app] #data[0] is name to display, data[1] is the size of font
            try:
                loc = f"{folderLoc}\\{data[2]}"
            except IndexError:
                loc = f"{folderLoc}\\{app}"
            appLaunchButton = ctk.CTkButton(appFrame, text=data[0], width=90, font=ctk.CTkFont(size=data[1]))
            def launch(loc):
                print(f"Launching {loc}")
                try:
                    Popen([loc],creationflags=DETACHED_PROCESS | CREATE_NEW_PROCESS_GROUP)
                except FileNotFoundError:
                    print(f"{loc} doesnt exist")
            appLaunchButton.configure(command=lambda loc=loc: launch(loc))
            master.shrink(appLaunchButton,w-20,data[1])
            appLaunchButton.grid(row=0,column=0,sticky="nsew")
            appFrame.grid(row=row,column=column,padx=5,pady=5,sticky="ew")
        
        for name, data in extras.items():
            cmd, font_size = data
            print(f"Adding {name}")
            column += 1
            if column % 4 == 0:
                row += 1
                column = 0

            appFrame = ctk.CTkFrame(launchFrame)
            appFrame.grid_propagate(False)

            w = round((master.width / 1250 * 1020 - 35) / 4)
            appFrame.configure(height=40, width=w)

            appFrame.grid_columnconfigure(0, weight=1)
            appFrame.grid_rowconfigure(0, weight=1)

            appLaunchButton = ctk.CTkButton(appFrame,text=name,width=90,font=ctk.CTkFont(size=font_size))
            master.shrink(appLaunchButton, w-10, font_size)
            def launch(cmd=cmd):
                print(f"Launching: {cmd}")
                Popen(cmd,creationflags=CREATE_NEW_CONSOLE)
            appLaunchButton.configure(command=launch)

            appLaunchButton.grid(row=0, column=0, sticky="nsew")
            appFrame.grid(row=row, column=column, padx=5, pady=5, sticky="ew")
        launchFrame.pack()
