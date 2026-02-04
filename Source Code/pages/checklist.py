import customtkinter as ctk

class ChecklistTL(ctk.CTkToplevel):
    def __init__(self, master):
        super().__init__(master=master, fg_color="#1d1a23")
        self.geometry("400x400")
        self.title("Tweak Checklist")
        self.attributes("-topmost", True)
        self.after(10, lambda: self.attributes("-topmost", False))
        self.protocol("WM_DELETE_WINDOW", self.on_close)
    def on_close(self):
        self.master.checklist = None
        self.destroy()