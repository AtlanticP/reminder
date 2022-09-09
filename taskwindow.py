import tkinter as tk 
from datetime import datetime, timedelta
import os
from functools import partial
from typing import Optional, Callable
import random
from itertools import count
import sys  

from dtwindow import DateTimeWindow 
from colorschemes import COLORS
from service import PATTERN_TIME

from hinting import Scheme, TaskListType, TaskType

class TaskWindow(tk.Toplevel):
    _ids = count(0)

    def __init__(self, text: Optional[str], tasks: TaskListType,
                scheme: Scheme) -> None:
        self._id = next(self._ids)
        self._text: Optional[str] = text
        self.scheme: Scheme = scheme
        self.tasks: TaskListType = tasks

        super().__init__()
        self._general_properties()
        self._set_widgets()
        self._set_colors()

    def _general_properties(self) -> None:
        self.title("Task")
        self.attributes("-topmost", 1)
        self._position_window()

    def _position_window(self) -> None:
        width: int = self.winfo_screenwidth()
        height: int = self.winfo_screenheight()
        x = (width - width*0.4 + self._id*40)
        y = (height - height/2 + self._id*40)

        self.geometry("+%d+%d" % (x, y))

    def _set_widgets(self) -> None:
        
        def rand_period() -> str:
            """"return random period for the reminder"""
            
            days: int = random.randint(0, 30)
            hours: int = random.randint(0, 24)
            minutes: int = random.randint(0, 60)
            period: str = f"days={days} minutes={minutes} hours={hours}"

            return period
        
        font_text: tuple[str, int, str] = ("times", 13, "normal")
        self.text_task: tk.Text = tk.Text(self, bg="light yellow", 
                                font=font_text, height=10, width=8)
        
        if self._text:
            self.text_task.insert("1.0", self._text)
            
        self.text_task.pack(fill=tk.X)
        
        label_reminder = tk.Label(self, text="Remind me in",
                                height=2)
        label_reminder.pack(fill="x", anchor="center")
        
        frame1: tk.Frame = tk.Frame(self)
        frame1.pack(fill="both")
        frame2: tk.Frame = tk.Frame(self)
        frame2.pack(fill="both")

        func_15min: Callable[...,  None]
        func_15min = partial(self._count_start_time,
                delta_str="minutes=15")
        tk.Button(frame1, text="15 min", command=func_15min)\
                .pack(side="left", fill="x", expand=True)

        func_1hour: Callable[..., None]
        func_1hour = partial(self._count_start_time,
                delta_str="hours=1 minutes=30")
        tk.Button(frame1, text="1.5 hour", command=func_1hour)\
                .pack(side="left", fill="x", expand=True)
        

        func_1day: Callable[..., None]
        func_1day = partial(self._count_start_time, delta_str="days=1")
        tk.Button(frame1, text="1 day", command=func_1day)\
                .pack(side="left", fill="x", expand=True)
        
        func_random: Callable[..., None]
        func_random = partial(self._count_start_time,
                delta_str=rand_period())
        tk.Button(frame2, text="random", command=func_random)\
                .pack(side="left", fill="x", expand=True)

        self.button_choose: tk.Button
        self.button_choose = tk.Button(frame2, command=self._pass_to_win_dt)
        self.button_choose["text"] = "choose"
        self.button_choose.pack(side="left", fill="x", expand=True)

        self.button_ok: tk.Button
        self.button_ok = tk.Button(frame2, command=self._click_ok_button)
        self.button_ok["text"] = "ok"
        self.button_ok["state"] = "disable"
        self.button_ok.pack(side="left", fill="x", expand=True)

        tk.Button(frame2, text="end", command=self._end_task)\
                .pack(side="left", fill="x", expand=True)
       
    def _set_colors(self) -> None:
        self.configure(**self.scheme["main"])
        childs: list[tk.Widget] = self.winfo_children()

        textarea: tk.Text = childs[0]    # type: ignore
        textarea.configure(**self.scheme["entry_task"])

        label_reminder: tk.Label = childs[1]    # type: ignore
        label_reminder.configure(**self.scheme["label_reminder"])

        childs: list[tk.Widget] = self.winfo_children()
        frames: list[tk.Frame] = [frame for frame in childs 
                                  if isinstance(frame, tk.Frame)]

        buttons: list[tk.Button] = [but for frame in frames for but in frame.winfo_children() \
                                    if isinstance(but, tk.Button)]

        for but in buttons:
            but.configure(**self.scheme["button"])
            
    def _count_start_time(self, delta_str: str) -> None:
        """Counts delta for a start time of the task"""

        self.is_extreme = False

        params: dict[str, int]
        params = {key: int(val) for key, val in 
                map(lambda x: x.split("="), delta_str.split(" "))}

        delta: timedelta = timedelta(**params)
        now: datetime = datetime.now()
        start: datetime = (now + delta)
        text: str = self.text_task.get(1.0, "end").rstrip("\n")    # Entry object add Return Cariage
        task: TaskType = {"start": start, "text": text}

        self.tasks.append(task)

        self.destroy()
        
    def _pass_to_win_dt(self) -> None:
        """init DateTimeWindow to choose date and timeself.
           It takes date and time after DateTimeWindow is closed"""

        self.button_choose["state"] = "disabled"
        win_dt = DateTimeWindow()
        self.wait_window(win_dt)

        self._start: datetime = win_dt.start

        try:
            self.button_ok["state"] = "active"
            self.button_choose["state"] = "active"
        except tk.TclError:
            sys.exit()
        
        self._show_choosed_time(self._start)

    def _show_choosed_time(self, start: datetime) -> None:
        """Shows the Label with selected from DateTimeWindow date and time.
        And removes the previuos one if it exists."""

        widget: tk.Widget
        for widget in self.winfo_children():
            if isinstance(widget, tk.Label):
                widget.destroy()

        dt: str = start.strftime(PATTERN_TIME)    # date and time
        
        label = tk.Label(self, text=dt)
        label.configure(**self.scheme["label_time"])
        label.pack(fill="x")

    def _click_ok_button(self) -> None:
        """Ater click on Button 'Ok' it saves task to tasks from main
        and end task"""
        text: str = self.text_task.get(1.0, "end")[:-1]    # Entry object add Return Cariage
        if text:
            self.task: TaskType = {"start": self._start, "text": text} 
            self.tasks.append(self.task)
        self._end_task()

    def _end_task(self) -> None:
        self.destroy()

        
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
    scheme: Scheme = COLORS["deep blue"]
    TaskWindow(tasks=tasks, text=text, scheme=scheme)
    root.mainloop()

