import tkinter as tk 
import tkinter.font
import sys
from datetime import datetime, timedelta
from collections import namedtuple
import csv
import os
from functools import partial

#%%
class TaskWindow(tk.Tk):
    
    _pattern_time = "%Y-%m-%d %H:%M:%S"
    
    def __init__(self):
        super().__init__()
    
    def _window_task(self, text=None):
        self.win_task = tk.Toplevel(self)
        self.win_task.title("Task")
        self.win_task.attributes("-topmost", 1)
        self.win_task.geometry("300x300")
        
        font_txt = ("times", 13, "normal")
        self.txt_task = tk.Text(self.win_task, bg="light yellow", font=font_txt, height=8)

        if text:
            text = text
        else:
            text = "Input your note"
            self.txt_task.bind("<FocusIn>", self._clear_placeholder)    
        
        self.txt_task.insert("1.0", text)
        self.txt_task.pack(fill=tk.X) #side=tk.LEFT, expand=True) # #expand=True,)
        tk.Label(self.win_task, text="Remind me in").pack(fill=tk.X)
        tk.Button(self.win_task, text="exit", command=self._app_exit).pack(side=tk.BOTTOM)   # !!!!!!!!!!!!!          
        tk.Button(self.win_task, text="5 sec", command=partial(self._save_note, delta="seconds=5")).pack(side=tk.LEFT)
        tk.Button(self.win_task, text="15 min", command=partial(self._save_note, delta="minutes=15")).pack(side=tk.LEFT)
        tk.Button(self.win_task, text="1.5 hour", command=partial(self._save_note, delta="hours=1|minutes=30")).pack(side=tk.LEFT)        
        
    def _clear_placeholder(self, event):
        self.txt_task.delete("0.0", "end")
        
    def _save_note(self, delta):
        txt = self.txt_task.get(1.0, "end")
        start = datetime.now()

        with open("tasks.csv", "a", newline='') as csvfile:
            fieldnames = ("start", "delta", "task")
            dct = {
                "start": f"{start.strftime('%Y-%m-%d %H:%M:%S')}",
                "delta": delta,
                "task": f"{txt}"
                }
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writerow(dct)
        
        self.win_task.destroy()
        
    def _app_exit(self):
        self.destroy()
        sys.exit()
        
if __name__ == "__main__":
    
    # fname = "tasks.csv"
    # if not os.path.isfile(fname):
    #     raise FileNotFoundError("It must be created tasks.csv file in the cwd with header 'start,delta,task'")
        
    root = TaskWindow()
    root.font = tk.font.nametofont("TkDefaultFont")
    root.font.config(size=14, family="Times", weight="bold")
    root._window_task()
    root.mainloop()