import tkinter as tk 
import tkinter.font
from datetime import datetime, timedelta
import os
from functools import partial

from picker import DateTimeWindow
#%%
class TaskWindow(DateTimeWindow):
    
    _pattern_time = "%Y-%m-%d %H:%M:%S"
    
    def _init_window_task(self, task="Input your task"):
        
        self.win_task = tk.Toplevel()
        self.win_task.title("Task")
        self.win_task.attributes("-topmost", 1)
        self.win_task.geometry("300x300")
        
        font_txt = ("times", 13, "normal")
        self.txt_task = tk.Text(self.win_task, bg="light yellow", font=font_txt, height=8)
        
        # !!!!!!!!!!!!!!!!!!!
        if task == "Input your note":
            self.txt_task.bind("<FocusIn>", self._clear_placeholder)    

        self.txt_task.insert("1.0", task)
        self.txt_task.pack(fill=tk.X) #side=tk.LEFT, expand=True) # #expand=True,)
        
        tk.Label(self.win_task, text="Remind me in").pack(fill=tk.X)

        func_5sec = partial(self._count_start_time, delta_str="seconds=5", text=task)
        tk.Button(self.win_task, text="5 sec", command=func_5sec).pack(side=tk.LEFT)

        func_15min = partial(self._count_start_time, delta_str="minutes=15", text=task)
        tk.Button(self.win_task, text="15 min", command=func_15min).pack(side=tk.LEFT)
        
        func_1hour = partial(self._count_start_time, delta_str="hours=1 minutes=30", text=task)
        tk.Button(self.win_task, text="1.5 hour", command=func_1hour).pack(side=tk.LEFT)        
        
        # tk.Button(self.win_task, text="choose", command=self._get_win_datetime).pack(side=tk.LEFT)        
        
    def _clear_placeholder(self, event):
        self.txt_task.delete("0.0", "end")
    
    def _count_start_time(self, delta_str):
        params = {key: int(val) for key, val in map(lambda x: x.split("="), delta_str.split(" "))}
        delta = timedelta(**params)
        now = datetime.now()
        start = (now + delta).strftime(self._pattern_time) 
        self._save_task(start)

        
if __name__ == "__main__":
    
    fname = "tasks.csv"
    if not os.path.isfile(fname):
        raise FileNotFoundError("It must be created tasks.csv file in the cwd with header 'start,delta,task'")
    root = tk.Tk()    
    # win1 = TaskWindow()
    # win1._init_window_task()
    TaskWindow()._init_window_task()
    # root.font = tk.font.nametofont("TkDefaultFont")
    # root.font.config(size=14, family="Times", weight="bold")
    # root._init_window_task()
    root.mainloop()