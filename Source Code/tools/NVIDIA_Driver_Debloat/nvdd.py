import customtkinter as ctk
from webbrowser import open as openLink
from os import path,getcwd,listdir,remove
from subprocess import Popen,run
from pathlib import Path
from shutil import rmtree
import threading
import asyncio
def on_close(self):
    print("close nvddtoplevel")
    self.NVDDtoplevel.destroy()
def apply(self):
    createnewtl = False
    try:
        if not self.NVDDtoplevel.winfo_exists():
            createnewtl = True
    except Exception:
        createnewtl = True
    if createnewtl:
        self.NVDDtoplevel = ctk.CTkToplevel(self, fg_color="#201d26")
        self.NVDDtoplevel.protocol("WM_DELETE_WINDOW", lambda: on_close(self))
        self.NVDDtoplevel.geometry("400x200")
        self.NVDDtoplevel.title("NVIDIA Driver Debloat")
        instructionsLabel = ctk.CTkLabel(self.NVDDtoplevel,text="Click this label and navigate to the Manual Driver Search. Download your recommended Game Ready driver and then use the box below to point this tool to the executable.",wraplength=395,cursor="hand2")
        instructionsLabel.bind("<Button-1>", lambda e: openLink("https://www.nvidia.com/en-gb/geforce/drivers/"))
        instructionsLabel.pack(side="top",pady=8)
        async def pick(statusLabel):
            try:
                EXE_PATH = ctk.filedialog.askopenfilename(title="Select the NVIDIA Driver to debloat",filetypes=[("Executable files", "*.exe")])
                if not EXE_PATH:
                    return
                self.after(0,instructionsLabel.destroy)
                self.after(0,btn.destroy)
                statusLabel.configure(text="Extracting driver...")
                self.NVDDtoplevel.attributes("-topmost", True)
                self.NVDDtoplevel.after(10,lambda: self.NVDDtoplevel.attributes("-topmost", False))
                sevenzippath = Path(path.join(getcwd()[:2],"/Program Files/","7-Zip/","7z.exe"))
                EXTRACTED_DIR = path.join(path.dirname(EXE_PATH),"SHIMMER_NVIDIA_DEBLOAT")
                run([
                    str(sevenzippath),
                    "x",
                    str(EXE_PATH),
                    f"-o{EXTRACTED_DIR}",
                    "-y"
                ])
                statusLabel.configure(text="Extracting complete\nDeleting unnecessary files...")
                ignores = ["setup.cfg","setup.exe","Display.Driver","NVI2"]
                for dir in listdir(EXTRACTED_DIR):
                    if not dir in ignores:
                        print(f"Deleting {dir}...")
                        itemLocation = path.join(EXTRACTED_DIR,dir)
                        if path.isdir(itemLocation):
                            rmtree(itemLocation)
                        else:
                            remove(itemLocation)
                statusLabel.configure(text="Removing EULA and tracking data...")
                filter = [r'<file name="eula.txt"/>',r'<file name="${{EulaHtmlFile}}"/>',r'<file name="${{FunctionalConsentFile}}"/>',r'<file name="${{PrivacyPolicyFile}}"/>']
                with open(path.join(EXTRACTED_DIR,"setup.cfg"),'r', encoding='utf-8', errors='ignore') as f:
                    filtered = [line for line in f.readlines() if line.strip() not in filter]
                with open(path.join(EXTRACTED_DIR,"setup.cfg"),'w', encoding='utf-8') as f:
                    f.writelines(filtered)

                with open(path.join(EXTRACTED_DIR,"NVI2","presentations.cfg"),'r', encoding='utf-8', errors='ignore') as f:
                    filtered = [line for line in f.readlines() if ("ProgressPresentationUrl" not in line and "ProgressPresentationSelectedPackageUrl" not in line)]
                with open(path.join(EXTRACTED_DIR,"NVI2","presentations.cfg"),'w', encoding='utf-8') as f:
                    f.writelines(filtered)
                statusLabel.configure(text="Debloat completed successfully!")
                if self.NVDDtoplevel.master.settings["install_driver_on_complete"]:
                    SETUPEXE = Path(EXTRACTED_DIR) / "setup.exe"
                    print("Running " + str(SETUPEXE))
                    Popen(SETUPEXE)
                if self.NVDDtoplevel.master.settings["delete_driver_files_after_debloat"]:
                    rmtree(EXTRACTED_DIR)
                    remove(EXE_PATH)
            except Exception as e:
                statusLabel.configure(text=f"Unexpected error occured: {e}")
        statusLabel = ctk.CTkLabel(self.NVDDtoplevel,text="",font=ctk.CTkFont(size=20),wraplength=380)
        statusLabel.pack(side="top",pady=8)
        btn = ctk.CTkButton(self.NVDDtoplevel,text="Select Driver",command=lambda: threading.Thread(target=lambda: asyncio.run(pick(statusLabel)), daemon=True).start())
        btn.pack(side="top",pady=8)
    self.NVDDtoplevel.attributes("-topmost", True)
    self.NVDDtoplevel.after(10,lambda: self.NVDDtoplevel.attributes("-topmost", False))