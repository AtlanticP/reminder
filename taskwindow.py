import tkinter as tk 
import tkinter.font
from datetime import datetime, timedelta
import os
from functools import partial
from typing import Optional
import random

from dtwindow import DateTimeWindow 

from hinting import Scheme, Scheme_name
from colors import COLORS

class TaskWindow(DateTimeWindow):

    def __init__(self, tasks: list[dict],  # order of arguments and hinting
                text: Optional[str]=None, 
                scheme_name: Scheme_name="deep blue",
                ) -> None:

        self._pattern_time: str = "%Y-%m-%d %H:%M:%S"
        self._text: Optional[str] = text
        self.scheme: Scheme = COLORS[scheme_name]

        self.tasks: list[dict] = tasks

        self._init_win_task()
        self._set_colors()

    def _init_win_task(self) -> None:
        
        def rand_period() -> str:
            """"return random period for the reminder"""
            
            days: int = random.randint(0, 30)
            hours: int = random.randint(0, 24)
            minutes: int = random.randint(0, 60)
            period: str = f"days={days} minutes={minutes} hours={hours}"

            return period
        
        self.win_task = tk.Toplevel()
        self.win_task.title("Task")
        self.win_task.attributes("-topmost", 1)
        
        font_text: tuple[str, int, str] = ("times", 13, "normal")
        self.text_task: tk.Text = tk.Text(self.win_task, bg="light yellow", 
                                font=font_text, height=10, width=8)
        
        if self._text:
            self.text_task.insert("1.0", self._text)
            
        self.text_task.pack(fill=tk.X)
        
        label_reminder = tk.Label(self.win_task, text="Remind me in",
                                height=2)
        label_reminder.pack(fill="x", anchor="center")
        
        frame1: tk.Frame = tk.Frame(self.win_task)
        frame1.pack(fill="both")
        frame2: tk.Frame = tk.Frame(self.win_task)
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
        tk.Button(frame2, text="random", command=func_random) \
                         .pack(side="left", fill="x", expand=True)        

        tk.Button(frame2, text="choose", command=self._pass_to_win_dt) \
                         .pack(side="left", fill="x", expand=True)
        
        tk.Button(frame2, text="end task", command=self._end_task) \
                         .pack(side="left", fill="x", expand=True)

    def _set_colors(self) -> None:
        self.win_task.configure(**self.scheme["main"])
        childs: list[tk.Widget] = self.win_task.winfo_children()

        textarea: tk.Text = childs[0]    # type: ignore
        textarea.configure(**self.scheme["entry_task"])

        label_reminder: tk.Label = childs[1]    # type: ignore
        label_reminder.configure(**self.scheme["label_reminder"])

        childs: list[tk.Widget] = self.win_task.winfo_children()
        frames: list[tk.Frame] = [frame for frame in childs 
                                  if isinstance(frame, tk.Frame)]

        buttons: list[tk.Button] = [but for frame in frames for but in frame.winfo_children() \
                                    if isinstance(but, tk.Button)]

        for but in buttons:
            but.configure(**self.scheme["button"])
            
    def _count_start_time(self, delta_str: str) -> None:
        """Counts delta for a start time of the task"""
        self.is_extreme = False

        params = {key: int(val) for key, val in map(lambda x: x.split("="), delta_str.split(" "))}
        delta = timedelta(**params)
        now = datetime.now()
        start = (now + delta)
        text = self.text_task.get(1.0, "end")
        self.tasks.append({"start": start, "text": text})
        # self._save_task(start, task)   # delete this functionality
        self.win_task.destroy()
        
    def _pass_to_win_dt(self):
        """???????????????"""
        text = self.text_task.get(1.0, "end")
        self._init_win_dt(text)
        self.win_task.destroy()
        
    def _end_task(self) -> None:
        self.win_task.destroy()

    # def __del__(self) -> None:
    #     """If exit from the window is not through buttons,
    #     then implement this fucntion"""
    #
    #     srart = datetime.now()
    #     self.
    #     
    #     if self._text:
    #         self.tasks.append({"start": start, "text": self._text})
        
if __name__ == "__main__":
    
    fname = "tasks.csv"
    if not os.path.isfile(fname):
        alarm = "It must be created tasks.csv file in the cwd with header 'start,text'"
        raise FileNotFoundError(alarm)

    root = tk.Tk()    
    root.font = tk.font.nametofont("TkDefaultFont")    # type: ignore
    root.font.config(size=14, family="Times", weight="bold")    # type: ignore
    tasks = []
    text = "Test task"
    TaskWindow(tasks, text)
    root.mainloop()