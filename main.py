import tkinter as tk
import tkinter.font
import sys
from datetime import datetime, timedelta
import time
#%%

class App(tk.Tk):
    
    def __init__(self):
        super().__init__()
        self._general_properties()
        self._set_widgets()
        self._current_time()
        
    def _general_properties(self):
        self.font = tk.font.nametofont("TkDefaultFont")
        self.font.config(size=12, family="Times", weight="bold")
        self.title("My Notes") 
        self.resizable(False, False)
        # self.attributes("-topmost", 1)        
        
    def _set_widgets(self):
        my_font = ("times", 52, "bold")
        self.label_time = tk.Label(self, font=my_font, bg="yellow")
        self.label_time.pack(side=tk.LEFT)
        
        self.but_exit = tk.Button(self, text="exit", command=self._app_exit)
        self.but_exit.pack(side=tk.LEFT)
        
        self.but_task = tk.Button(self, text="task", command=self._create_task)
        self.but_task.pack(side=tk.BOTTOM)
    
    def _current_time(self):
        time_string = time.strftime("%H:%M:%S %p")
        self.label_time.config(text=time_string)
        self.after(1000, self._current_time)
        
    def _create_task(self):
        win = tk.Toplevel(self)
        win.attributes("-topmost", 1)
        win.title("Create task")
        win.geometry("300x300")
        tk.Label(win, text="Input your task").pack()
        # import pdb; pdb.set_trace()
        
    def _app_exit(self):
        self.destroy()
        sys.exit()
        
        
if __name__ == "__main__":        
    root = App()
    root.mainloop()

#%%
        