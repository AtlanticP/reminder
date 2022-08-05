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
        self.win_task.geometry("400x400")
        
        font_txt = ("times", 13, "normal")
        self.txt_task = tk.Text(self.win_task, bg="light yellow", font=font_txt, height=8)
        
        if task:
            self.txt_task.insert("1.0", task)
            
        self.txt_task.pack(fill=tk.X) #side=tk.LEFT, expand=True) # #expand=True,)
        
        tk.Label(self.win_task, text="Remind me in").pack(fill=tk.X)
        
        frame1 = tk.Frame(self.win_task)
        frame1.pack(fill="x")
        frame2 = tk.Frame(self.win_task)
        frame2.pack(fill="x")
        
        func_5sec = partial(self._count_start_time, delta_str="seconds=5")
        tk.Button(frame1, text="5 sec", command=func_5sec).pack(fill="x")

        func_15min = partial(self._count_start_time, delta_str="minutes=15")
        tk.Button(frame1, text="15 min", command=func_15min).pack(fill="x")
        
        func_1hour = partial(self._count_start_time, delta_str="hours=1 minutes=30")
        tk.Button(frame1, text="1.5 hour", command=func_1hour).pack(fill="x")        
        
        func_random = partial(self._count_start_time, delta_str=rand_period())
        tk.Button(frame2, text="random", command=func_random).pack(fill="x")        
        # import pdb; pdb.set_trace()
        # tk.Button(self.win_task, text="choose", command=self._get_win_datetime).pack(side=tk.LEFT)        
    
    def _count_start_time(self, delta_str: str) -> None:
        params = {key: int(val) for key, val in map(lambda x: x.split("="), delta_str.split(" "))}
        delta = timedelta(**params)
        now = datetime.now()
        start = (now + delta).strftime(self._pattern_time) 
        task = self.txt_task.get(1.0, "end")
        self._save_task(start, task)
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
