import tkinter as tk
import tkinter.font
import sys
from datetime import datetime, timedelta
import time
#%%

class App(tk.Tk):
    
    def __init__(self):
        super().__init__()
        self.general_properties()
        self.set_widgets()
        self.my_time()
        
    def general_properties(self):
        self.font = tk.font.nametofont("TkDefaultFont")
        self.font.config(size=12, family="Times", weight="bold")
        self.title("My Notes") 
        self.resizable(False, False)
        # self.attributes("-topmost", 1)        
        
    def set_widgets(self):
        my_font = ("times", 52, "bold")
        self.label_time = tk.Label(self, font=my_font, bg="yellow")
        self.label_time.pack(side=tk.LEFT)
        
        self.but_exit = tk.Button(self, text="exit", command=self.app_exit)
        self.but_exit.pack(side=tk.LEFT)
        
        self.but_task = tk.Button(self, text="task", command=self.window_task)
        self.but_task.pack(side=tk.BOTTOM)
    
    def my_time(self):
        time_string = time.strftime("%H:%M:%S %p")
        self.label_time.config(text=time_string)
        self.after(1000, self.my_time)
        
    def window_task(self):
        win = tk.Toplevel(self)
        win.title("Task")
        win.geometry("300x300")
        tk.Label(win, text="Input your task").pack()
        
    def app_exit(self):
        self.destroy()
        sys.exit()
        
        
        
root = App()
root.mainloop()

#%%
        