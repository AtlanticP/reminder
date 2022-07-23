import tkinter as tk
import tkinter.font
import sys
from datetime import datetime, timedelta
import time
from task import TaskWindow
import os
import csv
#%%
class App(TaskWindow, tk.Tk):
    
    def __init__(self):
        tk.Tk.__init__(self)
                
        self.fname = "tasks.csv" # file where tasks are stored

        if not os.path.isfile(self.fname):
            with open(self.fname, "w") as file:
                writer = csv.writer(file, lineterminator="\n")
                writer.writerow(["start", "task"])
                
        self._general_properties()
        self._set_widgets()
        self._current_time()
        self._check_tasks()
        
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
        
        self.but_task = tk.Button(self, text="task", command=self._window_task)
        self.but_task.pack(side=tk.BOTTOM)
    
    def _current_time(self):
        time_string = time.strftime("%H:%M:%S %p")
        self.label_time.config(text=time_string)
        self.after(1000, self._current_time)

    def _check_tasks(self):
        
        fname_temp = "temp.csv"
        
        with open(self.fname) as infile, open(fname_temp, "w") as outfile:
            reader = csv.reader(infile)
            header = next(reader)
            writer = csv.DictWriter(outfile, header)
            writer.writeheader()
                
            for start, delta, task in reader:
                _now = datetime.now()
                _start = datetime.strptime(start, self._pattern_time)
                # delta
                arr = [el.split("=") for el in delta.split("|")]
                params = {key: int(val) for key, val in arr}
                _delta = timedelta(**params)
    
                if _now - _start > _delta:
                    self._window_task(text=task)
                else: 
                    writer.writerow({"start": start, "delta": delta, "task": task})
                    
        os.rename(fname_temp, self.fname)
        # import pdb; pdb.set_trace()        
        
        self.after(1000, self._check_tasks)            
    
    def _app_exit(self):
        self.destroy()
        sys.exit()
        
        
if __name__ == "__main__":        
    root = App()
    root.mainloop()
