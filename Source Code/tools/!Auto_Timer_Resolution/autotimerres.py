import customtkinter as ctk
from tkinter import StringVar
from os.path import join, exists
from os import environ, system, remove
from subprocess import Popen, PIPE, CREATE_NO_WINDOW, DETACHED_PROCESS, CREATE_NEW_PROCESS_GROUP, HIGH_PRIORITY_CLASS
import threading
from random import randint
import re
from time import sleep, time
from utils import resource_path
lastres = 5000
bestdelta = 1000
bestres = -1
results = {}
def userstopatr(stress,label,bestlabel,NtSetTimerResolution):
    label.after(0,label.master.destroy)
    stress.terminate()
    saveTRESShortcut(bestres)
    NtSetTimerResolution(0, False, ctypes.wintypes.ULONG()) #disable temporary timer res
    Popen([r"C:\Users\lop\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup\SetTimerResolution.exe.lnk"],shell=True)
def stopatr(stress,label,bestlabel,NtSetTimerResolution):
    NtSetTimerResolution(0, False, ctypes.wintypes.ULONG()) #disable temporary timer res
    bestlabel.after(0,bestlabel.destroy)
    if stress != None:
        stress.terminate()
    if label.master.master.atrautoApplyCheckbox.get():
        label.configure(text="Done, trying to apply...")
        saveTRESShortcut(bestres)
        label.configure(text=(f"Successfully applied {bestres}!" if exists(shortcut_location) else f"Failed, manually apply {bestres}. Guide in Discord."))
        Popen([r"C:\Users\lop\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup\SetTimerResolution.exe.lnk"],shell=True)
    else:
        label.configure(text=f"Best resolution is {bestres} ({bestdelta})")

import ctypes
ntdll = ctypes.WinDLL("ntdll")
NtSetTimerResolution = ntdll.NtSetTimerResolution
NtSetTimerResolution.argtypes = [ctypes.wintypes.ULONG,ctypes.wintypes.BOOLEAN,ctypes.POINTER(ctypes.wintypes.ULONG)]

def benchmark(res,samples,label,bestlabel):
    global results
    global bestdelta
    global lastres
    global bestres
    
    if label.master.winfo_exists():
        bestlabel.configure(text=f"Best: {bestres} {bestdelta}" if bestres!=-1 else "")
    NtSetTimerResolution(res, True, ctypes.wintypes.ULONG())
    label.configure(text=f"Benchmarking: {res}")
    with Popen((resource_path("TimerResolution\\MeasureSleep").split(" ") + ["--samples",samples]),stdout=PIPE,text=True,creationflags=CREATE_NO_WINDOW | CREATE_NEW_PROCESS_GROUP | DETACHED_PROCESS | HIGH_PRIORITY_CLASS) as MeasureSleep:
        label.master.master.openSubprocesses.append(MeasureSleep)
        output = MeasureSleep.stdout.read()
        label.master.master.openSubprocesses.remove(MeasureSleep)
    print(output)
    match = re.search(r"Max: (\d+\.\d+)",output)
    if match:
        r = float(match.group(1))
        results[res] = r
        if r < bestdelta:
            bestdelta = r
            bestres = res

def handleNtSetTimerResolution(minres,maxres,samples,label,stress):
    global results
    global bestdelta
    global lastres
    global bestres
    try:
        Popen(["taskkill","/f","/im","SetTimerResolution.exe"],creationflags=CREATE_NO_WINDOW)
        bestlabel = ctk.CTkLabel(label.master, fg_color="transparent", text="")
        bestlabel.pack()
        stopbtn = ctk.CTkButton(label.master,text="Apply current best",fg_color="#ff3333",hover_color="#ff6666",text_color="#ffffff",command=lambda: userstopatr(stress,label,bestlabel,NtSetTimerResolution))
        stopbtn.pack(pady=5)
        for res in range(minres,maxres+1,5):
            benchmark(res,samples,label,bestlabel)
        for k,v in results.items():
            if v < bestdelta:
                bestdelta = v
                bestres = k
        results = {}
        for res in range(bestres-3,bestres+3):
            if res >= 5000 and res <= 15625:
                benchmark(res,samples,label,bestlabel)
        for k,v in results.items():
            if v < bestdelta:
                bestdelta = v
                bestres = k
        stopatr(stress,label,bestlabel,NtSetTimerResolution)
    except FileNotFoundError as e:
        print(f"error during timer res\n{str(e)}")
        if stress != None:
            stress.terminate()



import win32com.client as cli
import pythoncom
shortcut_location = join(environ["APPDATA"],r"Microsoft\Windows\Start Menu\Programs\Startup",f"SetTimerResolution.exe.lnk")
def saveTRESShortcut(bestres):
    pythoncom.CoInitialize()
    global shortcut_location
    shell = cli.Dispatch("WScript.Shell")
    shortcut = shell.CreateShortCut(shortcut_location)
    shortcut.Targetpath = resource_path("TimerResolution\\SetTimerResolution.exe")
    shortcut.Arguments = f"--no-console --resolution {bestres}"
    shortcut.save()
    pythoncom.CoUninitialize()

def default(self,btn):
    global shortcut_location
    if exists(shortcut_location):
        remove(shortcut_location)
    btn.configure(text="Applied.")
    Popen(["taskkill","/f","/im","SetTimerResolution.exe"],creationflags=CREATE_NO_WINDOW)
    btn.master.after(1500, lambda: btn.configure(text="Confirm"))



running = False

def on_close(self):
    print("close atrtoplevel")
    global results
    global bestdelta
    global lastres
    global bestres
    results = {}
    bestdelta = 1000
    bestres = -1
    lastres = 5000
    self.stop.set()
    self.after(0,self.ATRtoplevel.destroy)
    for process in self.openSubprocesses:
        print(f"Terminating {process}")
        process.terminate()

def apply(self):
    self.stop = threading.Event()
    createnewtl = False
    try:
        if not self.ATRtoplevel.winfo_exists():
            createnewtl = True
    except Exception:
        createnewtl = True
    if createnewtl:
        self.ATRtoplevel = ctk.CTkToplevel(self, fg_color="#201d26")
        self.ATRtoplevel.protocol("WM_DELETE_WINDOW", lambda: on_close(self))
        self.ATRtoplevel.geometry("675x200")
        self.ATRtoplevel.title("Apply Timer Resolution")

        #create a frame to hold entries, then pack the frame and submit button
        minres = StringVar(value=5000)
        maxres = StringVar(value=5100)
        samples = StringVar(value=50)


        self.varsFrame = ctk.CTkFrame(self.ATRtoplevel, fg_color="#201d26")


        minresFrame = ctk.CTkFrame(self.varsFrame, fg_color="transparent", width=115)
        minresLabel = ctk.CTkLabel(minresFrame, text="Minimum Resolution")
        minresEntry = ctk.CTkEntry(minresFrame, textvariable=minres, justify="center")

        minresLabel.pack()
        minresEntry.pack()
        minresFrame.grid(row=0,column=0)

        
        maxresFrame = ctk.CTkFrame(self.varsFrame, fg_color="transparent", width=115)
        maxresLabel = ctk.CTkLabel(maxresFrame, text="Maximum Resolution")
        maxresEntry = ctk.CTkEntry(maxresFrame, textvariable=maxres, justify="center")

        maxresLabel.pack()
        maxresEntry.pack()
        maxresFrame.grid(row=0,column=1)


        samplesFrame = ctk.CTkFrame(self.varsFrame, fg_color="transparent", width=115)
        samplesLabel = ctk.CTkLabel(samplesFrame, text="Samples")
        samplesEntry = ctk.CTkEntry(samplesFrame, textvariable=samples, justify="center")

        samplesLabel.pack()
        samplesEntry.pack()
        samplesFrame.grid(row=0,column=2)


        self.atrautoApplyCheckbox = ctk.CTkCheckBox(self.varsFrame,text="Auto Apply")
        self.atrautoApplyCheckbox.select()
        self.atrautoApplyCheckbox.grid(row=0,column=3)


        self.atrstressCheckbox = ctk.CTkCheckBox(self.varsFrame,text="Stress Test")
        self.atrstressCheckbox.select()
        self.atrstressCheckbox.grid(row=0,column=4)


        for i in range(4):
            self.varsFrame.grid_columnconfigure(i, weight=1, uniform="col")
        self.varsFrame.pack(side="top", pady=(10,0), fill="x")


        statusLabel = ctk.CTkLabel(self.ATRtoplevel, text="", font=ctk.CTkFont(size=24))
        statusLabel.pack(side="top", pady=(10,0))

        
        self.confirmBtn = ctk.CTkButton(self.ATRtoplevel, text="Confirm", font=ctk.CTkFont(size=20), fg_color="#1a1720", hover_color="#16131c")
        self.timerresthread = threading.Thread(target=confirm, args=(minres, maxres, samples, self.confirmBtn, statusLabel), daemon=True)
        self.confirmBtn.configure(command=lambda: parseAndStart(minres,maxres,samples,self.confirmBtn))

        self.confirmBtn.pack(side="top", pady=(10,0))

        threading.Thread(target=heartbeat,args=(self.ATRtoplevel,self.stop), daemon=True).start()
    self.ATRtoplevel.attributes("-topmost", True)
    self.ATRtoplevel.after(10,lambda: self.ATRtoplevel.attributes("-topmost", False))
    

TRES_DIR = r"TimerResolution"


def confirm(minres,maxres,samples,btn,label):
    if label.master.master.atrstressCheckbox.get():
        label.after(0,label.master.master.atrstressCheckbox.destroy)
        label.master.master.varsFrame.grid_columnconfigure(4,weight=0)
        with Popen(resource_path("TimerResolution\\stress").split(" "),creationflags=CREATE_NO_WINDOW) as st:
            label.master.master.openSubprocesses.append(st)
            label.configure(text="Loading... (3s wait)")
            sleep(3)
            threading.Thread(target=handleNtSetTimerResolution,args=(int(minres.get()),int(maxres.get()),samples.get(),label,st), daemon=True).start()
    else:
        label.after(0,label.master.master.atrstressCheckbox.destroy)
        label.master.master.varsFrame.grid_columnconfigure(4,weight=0)
        threading.Thread(target=handleNtSetTimerResolution,args=(int(minres.get()),int(maxres.get()),samples.get(),label,None), daemon=True).start()

def error(btn,msg):
    btn.configure(text=msg)
    btn.master.after(3000, lambda: btn.configure(text="Confirm"))

def heartbeat(toplevel: ctk.CTkToplevel, stopflag):
    while True:
        #print("heartbeat") #for debugging
        try:
            if not toplevel.winfo_exists():
                stopflag.set()
                break
            else:
                sleep(0.5)
        except RuntimeError as e:
            print(e)
            stopflag.set()
            break

def parseAndStart(minres,maxres,samples,btn):
    try:
        min = int(minres.get())
        max = int(maxres.get())
        sam = int(samples.get())
    except Exception:
        error(btn,"Integers only.")
        return
    if sam <= 0:
        error(btn,"Samples must be greater than 0.")
    elif min >= max:
        error(btn,"Minimum must be less than maximum.")
    elif min < 5000:
        error(btn,"Minimum must be greater than 4999.")
    elif max > 15625:
        error(btn,"Maximum must be less than 15626.")
    else:
        btn.after(0,btn.destroy)
        btn.master.master.timerresthread.start()
