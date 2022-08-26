import tkinter as tk
import tkinter.font    # type: ingore
import sys
import time
import os
import csv
from datetime import datetime
from taskwindow import TaskWindow
from colors import COLORS
from hinting import Schemes

class App(tk.Tk):
    
    _pattern_time = "%Y-%m-%d %H:%M:%S"  # type: str
    
    def __init__(self) -> None:
        super().__init__()
                
        self.tasks = {}

        self.fname: str = "tasks.csv" # file where tasks are stored
        if not os.path.isfile(self.fname):
            with open(self.fname, "w") as file:
                writer = csv.writer(file, lineterminator="\n")
                writer.writerow(["start", "task"])
                
        self.buttons = []
        self._general_properties()
        self._set_widgets()
        self._set_colorscheme("deep blue")
        self._current_time()
        self._check_tasks()

    def _general_properties(self) -> None:
        self.font = tkinter.font.nametofont("TkDefaultFont")
        self.font.config(size=12, family="Times", weight="bold")
        self.title("My Notes") 
        self.resizable(False, False)
        
    def _set_widgets(self) -> None:
        my_font = ("times", 24)
        self.label_time = tk.Label(self, font=my_font, bg="yellow")
        self.label_time.pack(side=tk.LEFT)
        
        but_exit = tk.Button(self, text="exit", command=self._app_exit)
        but_exit.pack(side=tk.LEFT)
        self.buttons.append(but_exit)
        
        but_task = tk.Button(self, text="task", command=self._window_task)
        but_task.pack(side=tk.LEFT)
        self.buttons.append(but_task)
        
    def _set_colorscheme(self, s: Schemes):
        scheme  = COLORS[s]
        self.configure(**scheme["main"]) 
        self.label_time.configure(**scheme["label_time"])
        
        for button in self.buttons:
            button.configure(**scheme["button"])

        
    def _current_time(self) -> None:
        time_string = time.strftime("%H:%M:%S %p")
        self.label_time.config(text=time_string)
        self.after(1000, self._current_time)

    def _window_task(self) -> None:
        TaskWindow()
            
    def _check_tasks(self) -> None:

        fname_temp = "temp.csv"
        
        with open(self.fname) as infile, open(fname_temp, "w") as outfile:
            reader = csv.reader(infile)
            header = next(reader)
            writer = csv.DictWriter(outfile, header)
            writer.writeheader()
            
            for start_str, task  in reader:
                now = datetime.now()
                start = datetime.strptime(start_str, self._pattern_time)
    
                if now > start:
                    TaskWindow(task=task)
                else: 
                    start_str = start.strftime(self._pattern_time)
                    writer.writerow({"start": start_str, "task": task})
                    
        os.rename(fname_temp, self.fname)
        
        self.after(1000, self._check_tasks)            
    
    def _app_exit(self):
        self.destroy()
        sys.exit()
        
        
if __name__ == "__main__":        
    root = App()
    root.mainloop()
    
