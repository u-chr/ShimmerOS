import customtkinter as ctk
from webbrowser import open as openLink
from os import path,getcwd,listdir,remove,rename,mkdir
from subprocess import Popen, DETACHED_PROCESS, CREATE_NEW_PROCESS_GROUP, PIPE,run
from shutil import rmtree
import threading
import asyncio
from pathlib import Path
def on_close(self):
    print("close amdvddtoplevel")
    self.AMDVDDtoplevel.destroy()
def apply(self):
    createnewtl = False
    try:
        if not self.AMDVDDtoplevel.winfo_exists():
            createnewtl = True
    except Exception:
        createnewtl = True
    if createnewtl:
        self.AMDVDDtoplevel = ctk.CTkToplevel(self, fg_color="#201d26")
        self.AMDVDDtoplevel.protocol("WM_DELETE_WINDOW", lambda: on_close(self))
        self.AMDVDDtoplevel.geometry("400x150")
        self.AMDVDDtoplevel.title("AMD Video Driver Debloat")
        instructionsLabel = ctk.CTkLabel(self.AMDVDDtoplevel,text="Click this label to open AMD driver download page. Download your recommended driver (Adrenalin Edition needed) and then use the box below to point this tool to the executable.",wraplength=395,cursor="hand2")
        instructionsLabel.bind("<Button-1>", lambda e: openLink("https://www.amd.com/en/support/download/drivers.html#search-browse-drivers"))
        instructionsLabel.pack(side="top",pady=8)
        async def pick(statusLabel):
            try:
                EXE_PATH = Path(ctk.filedialog.askopenfilename(title="Select the AMD video Driver to debloat",filetypes=[("Executable files", "*.exe")]))
                if str(EXE_PATH) == '.':
                    self.AMDVDDtoplevel.attributes("-topmost", True)
                    self.AMDVDDtoplevel.after(10,lambda: self.AMDVDDtoplevel.attributes("-topmost", False))
                    return
                CLEAN_DIR = EXE_PATH.parent / "SHIMMER_AMD_DEBLOAT"
                if path.exists(CLEAN_DIR):
                    rmtree(CLEAN_DIR)
                instructionsLabel.configure(text="Select which components to remove:")
                confframe = ctk.CTkFrame(self.AMDVDDtoplevel)

                amdocl = ctk.StringVar(value="amdocl")
                amdocl_cb = ctk.CTkCheckBox(confframe,text="AMDOCL\nNeeded for Adobe, Davinci, HandBrake, etc",variable=amdocl,onvalue="amdocl",offvalue="DISABLED")
                amdocl_cb.select()
                amdocl_cb.grid(row=0,padx=5,pady=5,sticky="w")

                amdpcibridge = ctk.StringVar(value="amdpcibridge")
                amdpcibridge_cb = ctk.CTkCheckBox(confframe,text="amdpcibridge\nAllows CPU to communicate with AXI based PCIe hardware",variable=amdpcibridge,onvalue="amdpcibridge",offvalue="DISABLED")
                amdpcibridge_cb.select()
                amdpcibridge_cb.grid(row=1,padx=5,pady=5,sticky="w")

                amdwin = ctk.StringVar(value="amdwin")
                amdwin_cb = ctk.CTkCheckBox(confframe,text="amdwin\nSpeeds up GPU frame capturing on Windows",variable=amdwin,onvalue="amdwin",offvalue="DISABLED")
                amdwin_cb.select()
                amdwin_cb.grid(row=2,padx=5,pady=5,sticky="w")

                amdxe = ctk.StringVar(value="amdxe")
                amdxe_cb = ctk.CTkCheckBox(confframe,text="amdxe\nUpdate checking and data tracking.",variable=amdxe,onvalue="amdxe",offvalue="DISABLED")
                amdxe_cb.select()
                amdxe_cb.grid(row=3,padx=5,pady=5,sticky="w")

                amdfdans = ctk.StringVar(value="amdfdans")
                amdfdans_cb = ctk.CTkCheckBox(confframe,text="amdfdans\nAMD Dynamic Audio Noise Suppression Service",variable=amdfdans,onvalue="amdfdans",offvalue="DISABLED")
                amdfdans_cb.select()
                amdfdans_cb.grid(row=4,padx=5,pady=5,sticky="w")

                amdfendr = ctk.StringVar(value="amdfendr")
                amdfendr_cb = ctk.CTkCheckBox(confframe,text="amdfendr\nAMD Crash Defender Service",variable=amdfendr,onvalue="amdfendr",offvalue="DISABLED")
                amdfendr_cb.select()
                amdfendr_cb.grid(row=5,padx=5,pady=5,sticky="w")

                HDABus = ctk.StringVar(value=0)
                HDABus_cb = ctk.CTkCheckBox(confframe,text="HDABus\nMonitor HDMI Audio Support",variable=HDABus,onvalue=1,offvalue=0)
                HDABus_cb.deselect()
                HDABus_cb.grid(row=6,padx=5,pady=5,sticky="w")

                self.AMDVDDtoplevel.geometry("400x365")
                confframe.pack(side="top",fill="both",expand=True)
                def cont():
                    try:
                        self.after(0,confframe.destroy)
                        self.after(0,instructionsLabel.destroy)
                        self.after(0,btn.destroy)
                        EXTRACTED_DIR = Path(EXE_PATH.parent) / "SHIMMER_AMD_DEBLOAT_TEMP"
                        sevenzippath = Path(path.join(getcwd()[:2],"/Program Files/","7-Zip/","7z.exe"))
                        statusLabel.pack(side="top",pady=8)
                        statusLabel.configure(text="Extracting driver...")
                        run([
                            str(sevenzippath),
                            "x",
                            str(EXE_PATH),
                            f"-o{EXTRACTED_DIR}",
                            "-y"
                        ])
                        statusLabel.configure(text="Extracting complete\nDeleting unnecessary files...")
                        DRIVER_DIR = Path(EXTRACTED_DIR) / "Packages" / "Drivers" / "Display" / "WT6A_INF"
                        delete = [amdocl.get(),amdpcibridge.get(),amdwin.get(),amdxe.get(),amdfdans.get(),amdfendr.get(),HDABus.get()]
                        print(f"Deleting:\n{delete}")
                        mkdir(CLEAN_DIR)
                        global INF
                        INF = None
                        for dir in listdir(DRIVER_DIR):
                            src = Path(DRIVER_DIR) / dir
                            print(f"Checking {dir}...")
                            if dir.endswith(".inf"):
                                INF = dir
                            elif dir in delete:
                                
                                print(f"Deleting {dir}...\n")
                                if src.is_dir():
                                    rmtree(src)
                                else:
                                    remove(src)
                                continue
                            print(f"Moving {dir}...\n")
                            rename(src,Path(CLEAN_DIR) / dir)
                        
                        self.AMDVDDtoplevel.attributes("-topmost", True)
                        self.AMDVDDtoplevel.after(10,lambda: self.AMDVDDtoplevel.attributes("-topmost", False))
                        if INF:
                            print("Debloat successful")
                            statusLabel.configure(text="Debloat successful!")
                            if self.AMDVDDtoplevel.master.settings["install_driver_on_complete"]:
                                statusLabel.configure(text="Installing...")
                                Dproc = Popen(["pnputil","/add-driver",path.join(CLEAN_DIR,INF),"/install"],creationflags=DETACHED_PROCESS | CREATE_NEW_PROCESS_GROUP,stdout=PIPE,stderr=PIPE,text=True,close_fds=True)
                                Dproc.wait()
                                if Dproc.returncode == 0:
                                    statusLabel.configure(text="Successfully completed!")
                                else:
                                    Dproc.communicate()
                                    if Dproc.returncode == 5:
                                        statusLabel.configure(text="Not admin")
                                    if Dproc.returncode == 259:
                                        statusLabel.configure(text="Better driver already installed\nuninstall the old one first.")
                                    else:
                                        statusLabel.configure(text=f"Failed with code {Dproc.returncode}")
                                if HDABus.get() == 1:
                                    print("installing hdabus")
                                    proc = Popen(["pnputil","/add-driver",DRIVER_DIR.parent.parent / "Audio" / "HDABus" / "WT64A","/install"],creationflags=DETACHED_PROCESS | CREATE_NEW_PROCESS_GROUP,stdout=PIPE,stderr=PIPE,text=True,close_fds=True)
                                    proc.wait()
                                    if proc.returncode == 0:
                                        statusLabel.configure(text=statusLabel.cget("text") + "\nHDABus succesfully installed.")
                                    else:
                                        proc.communicate() #forgot what this does its probably useless
                                        if proc.returncode == 5:
                                            statusLabel.configure(text=statusLabel.cget("text") + "\nHDABus installation failed: not admin")
                                        if proc.returncode == 259:
                                            statusLabel.configure(text=statusLabel.cget("text") + "\nHDABus already installed.")
                                        else:
                                            statusLabel.configure(text=statusLabel.cget("text") + f"\nHDABus installation failed with code {proc.returncode}")
                            if self.AMDVDDtoplevel.master.settings["delete_driver_files_after_debloat"]:
                                print("Attempting to delete files..")
                                rmtree(CLEAN_DIR)
                                remove(EXE_PATH)
                                rmtree(EXTRACTED_DIR)
                                        
                        else:
                            raise Exception("INF file not found")
                    except Exception as e:
                        print(f"Unexpected error occured: {e}")
                        statusLabel.configure(text=f"Unexpected error occured: {e}")
                btn.configure(text="Confirm",command=lambda: threading.Thread(target=cont,daemon=True).start())
                self.AMDVDDtoplevel.attributes("-topmost", True)
                self.AMDVDDtoplevel.after(10,lambda: self.AMDVDDtoplevel.attributes("-topmost", False))
            except AttributeError: #user didnt select a driver
                pass
            except Exception as e:
                print(f"Unexpected error occured: {e}")
                statusLabel.configure(text=f"Unexpected error occured: {e}")
        statusLabel = ctk.CTkLabel(self.AMDVDDtoplevel,text="",font=ctk.CTkFont(size=20),wraplength=380)
        btn = ctk.CTkButton(self.AMDVDDtoplevel,text="Select Driver",command=lambda: threading.Thread(target=lambda: asyncio.run(pick(statusLabel)), daemon=True).start())
        btn.pack(side="top",pady=8)
    self.AMDVDDtoplevel.attributes("-topmost", True)
    self.AMDVDDtoplevel.after(10,lambda: self.AMDVDDtoplevel.attributes("-topmost", False))
