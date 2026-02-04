from os.path import exists,join
from os import getcwd
import json
SOFTWARE_DIR = join(getcwd()[2:],"/Shimmer","Software")
SETTINGS_DIR = join(SOFTWARE_DIR,"settings.json")
import customtkinter as ctk
available = ["install_driver_on_complete",
             "delete_driver_files_after_debloat",
             "peak_os_mode"]
def verifysettings(settings):
    e = 0
    for option in available:
        if not option in settings:
            settings[option] = 2
            e += 1
    print(f"{e} errors in settings file.")
    return settings



class settingsPage(ctk.CTkFrame):
    def setupSettings(self,gui):
        self.gui = gui
        if not exists(SETTINGS_DIR):
            open(SETTINGS_DIR,'x').close
            self.gui.settings = {
                "install_driver_on_complete": 1,
                "delete_driver_files_after_debloat": 1,
                "peak_os_mode": 0
            }
            with open(SETTINGS_DIR,'w') as f:
                json.dump(self.gui.settings,f,indent=4)
        else:
            with open(SETTINGS_DIR,'r') as f:
                self.gui.settings = json.load(f)
        self.gui.settings = verifysettings(self.gui.settings)
        print(f"Loaded settings:\n{self.gui.settings}")
    def updateSettings(self,change,match=[]):
        newValue = change.get()
        for key in match:
            requirement = key[1] #2 means apply to key if 1 or 2, otherwise, apply if equal to requirement
            if requirement == 2 or requirement == newValue:
                self.gui.settings[key[0]] = newValue
                if newValue == 1:
                    key[2].select()
                else:
                    key[2].deselect()
        with open(SETTINGS_DIR,'w') as f:
            print("Settings updated.")
            json.dump(self.gui.settings,f,indent=4)
    def __init__(self, master):
        super().__init__(master=master.main_area, fg_color="transparent")
        shrink = master.shrink
        self.titleBar = ctk.CTkLabel(self, text="Settings", font=ctk.CTkFont(size=32,weight="bold"), bg_color="#1d1a23", height=50)
        shrink(self.titleBar,round(master.width/1250*1020),32)
        self.titleBar.pack(side="top", fill="x", pady=(0,5))

        self.install_driver_on_complete = ctk.IntVar(value=self.gui.settings["install_driver_on_complete"])
        idocCheckbox = ctk.CTkCheckBox(self,text="Install driver after debloat",
                                       variable=self.install_driver_on_complete,)
        idocCheckbox.pack()


        self.delete_driver_files_after_debloat = ctk.IntVar(value=self.gui.settings["delete_driver_files_after_debloat"])
        ddfadCheckbox = ctk.CTkCheckBox(self,text="Delete driver files after auto-install",
                                       variable=self.delete_driver_files_after_debloat,
                                       command=lambda: self.updateSettings(self.delete_driver_files_after_debloat,
                                       match=["delete_driver_files_after_debloat"]))
        ddfadCheckbox.pack()


        self.peak_os_mode = ctk.IntVar(value=self.gui.settings["peak_os_mode"])
        pomCheckbox = ctk.CTkCheckBox(self,text="Change 'Shimmer' to 'Peak' in software (for the funsies)",
                                       variable=self.peak_os_mode,
                                       command=lambda: self.updateSettings(self.peak_os_mode,
                                       match=["peak_os_mode"]))
        pomCheckbox.pack()


        idocCheckbox.configure(command=lambda: self.updateSettings(
                                    self.install_driver_on_complete,
                                    match=[["install_driver_on_complete",2,idocCheckbox],
                                            ["delete_driver_files_after_debloat",0,ddfadCheckbox]]))
        ddfadCheckbox.configure(command=lambda: self.updateSettings(
                                    self.delete_driver_files_after_debloat,
                                    match=[["delete_driver_files_after_debloat",2,ddfadCheckbox]]))
        pomCheckbox.configure(command=lambda: self.updateSettings(
                                    self.peak_os_mode,
                                    match=[["peak_os_mode",2,pomCheckbox]]))