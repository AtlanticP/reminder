import tkinter as tk 
import tkinter.font
from datetime import datetime, timedelta
import os
from functools import partial
from typing import Optional
import random

from picker import DateTimeWindow 
#%%

class TaskWindow(DateTimeWindow):
    
    _pattern_time = "%Y-%m-%d %H:%M:%S"
    
    def _init_win_task(self, task: Optional[str]=None) -> None:
        
        def rand_period() -> str:
            """"return random period for the reminder"""
            
            days = random.randint(0, 30)
            hours = random.randint(0, 24)
            minutes = random.randint(0, 60)
            period = f"days={days} minutes={minutes} hours={hours}"

            return period
        
        self.win_task = tk.Toplevel()
        self.win_task.title("Task")
        self.win_task.attributes("-topmost", 1)
        
        font_txt = ("times", 13, "normal")
        self.txt_task = tk.Text(self.win_task, bg="light yellow", font=font_txt, height=10, width=8)
        
        if task:
            self.txt_task.insert("1.0", task)
            
        self.txt_task.pack(fill=tk.X)
        
        tk.Label(self.win_task, text="Remind me in").pack(fill=tk.X)
        
        frame1 = tk.Frame(self.win_task)
        frame1.pack(fill="both")
        frame2 = tk.Frame(self.win_task)
        frame2.pack(fill="both")
        
        func_5sec = partial(self._count_start_time, delta_str="seconds=5")
        tk.Button(frame1, text="5 sec", command=func_5sec).pack(side="left", fill="x", expand=True)

        func_15min = partial(self._count_start_time, delta_str="minutes=15")
        tk.Button(frame1, text="15 min", command=func_15min).pack(side="left", fill="x", expand=True)
        
        func_1hour = partial(self._count_start_time, delta_str="hours=1 minutes=30")
        tk.Button(frame1, text="1.5 hour", command=func_1hour).pack(side="left", fill="x", expand=True)        
        
        func_random = partial(self._count_start_time, delta_str="days=1")
        tk.Button(frame1, text="1 day", command=func_random).pack(side="left", fill="x", expand=True)        
        
        func_random = partial(self._count_start_time, delta_str=rand_period())
        tk.Button(frame2, text="random", command=func_random).pack(side="left", fill="x", expand=True)        

        tk.Button(frame2, text="choose", command=self._pass_to_win_dt).pack(side="left", fill="x", expand=True)
        
        tk.Button(frame2, text="end task", command=self._end_task).pack(side="left", fill="x", expand=True)
    
    def _count_start_time(self, delta_str: str) -> None:
        params = {key: int(val) for key, val in map(lambda x: x.split("="), delta_str.split(" "))}
        delta = timedelta(**params)
        now = datetime.now()
        start = (now + delta).strftime(self._pattern_time) 
        task = self.txt_task.get(1.0, "end")
        self._save_task(start, task)
        self.win_task.destroy()
        
    def _pass_to_win_dt(self):
        task = self.txt_task.get(1.0, "end")
        self._init_win_dt(task)
        self.win_task.destroy()
        
    def _end_task(self) -> None:
        self.win_task.destroy()
        
if __name__ == "__main__":
    
    fname = "tasks.csv"
    if not os.path.isfile(fname):
        raise FileNotFoundError("It must be created tasks.csv file in the cwd with header 'start,delta,task'")

    root = tk.Tk()    
    root.font = tk.font.nametofont("TkDefaultFont")    # type: ignore
    root.font.config(size=14, family="Times", weight="bold")    # type: ignore
    TaskWindow()._init_win_task()
    root.mainloop()

