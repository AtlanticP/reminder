import tkinter as tk
import tkinter.font
import time
import os
import csv
from datetime import datetime 
from typing import Union
import sys

from movewin import MoveWin
from taskwindow import TaskWindow
from colorschemes import COLORS
from tasklist import TaskList
from savetask import SaveTask
from service import PATTERN_TIME, FIELDNAMES
from filemanager import FileManager

from hinting import Scheme_name, Scheme, TaskType, TaskListType 


class App(MoveWin, SaveTask):
    
    def __init__(self, scheme_name: Scheme_name,
            path_tasks: str) -> None:
        super().__init__()

        self._tasks: TaskListType = []

        self.fname: str = path_tasks    # file where tasks are located
        if not os.path.isfile(self.fname):
            with open(self.fname, "w") as file:
                writer = csv.DictWriter(file, fieldnames=FIELDNAMES)
                writer.writeheader()
                
        self.buttons: list[tk.Button] = []
        self.scheme: Scheme = COLORS[scheme_name]

        self._general_properties()
        self._set_widgets()
        self._set_colorscheme()
        self._current_time()
        self._load_tasks()

    def _general_properties(self) -> None:
        self.font = tkinter.font.nametofont("TkDefaultFont")
        self.font.config(size=12, family="Times", weight="bold")
        self.title("My Notes") 
        self.resizable(False, False)
        
    def _set_widgets(self) -> None:
        my_font: tuple[str, int] = ("times", 24)
        self.label_time = tk.Label(self, font=my_font, height=3)
        self.label_time.pack(side=tk.LEFT)

        params_but: dict[str, Union[str, bool]] 
        params_but= {"side":"top", "fill":"both", "expand":True}
        
        but_task = tk.Button(self, text="task", 
                            command=self._window_task)
        but_task.pack(**params_but)
        self.buttons.append(but_task)
        
        self.but_list = tk.Button(self, text="today", 
                            command=self._get_list)
        self.but_list.pack(**params_but)
        self.buttons.append(self.but_list)

        but_exit = tk.Button(self, text="exit", 
                            command=self._app_exit)
        but_exit.pack(**params_but)
        self.buttons.append(but_exit)
        
    def _set_colorscheme(self):
        self.configure(**self.scheme["main"]) 
        self.label_time.configure(**self.scheme["label_time"])
        
        button: tk.Button
        for button in self.buttons:
            button.configure(**self.scheme["button"])
        
    def _current_time(self) -> None:
        """get current time for Label (a clock)"""
        time_string: str = time.strftime("%H:%M:%S %p")
        self.label_time.config(text=time_string)
        self.after(1000, self._current_time)

    def _window_task(self) -> None:
        TaskWindow(text=None, tasks=self._tasks,
                    scheme=self.scheme)
            
    def _load_tasks(self) -> None:
        """ Read csv file where tasks are stored, append tasks 
            and call function that check tasks to appears.
        """

        with open(self.fname, "r") as csvfile:
            reader = csv.DictReader(csvfile, fieldnames=FIELDNAMES)
            next(reader)    # header
            
            for row in reader:
                start: datetime 
                start = datetime.strptime(row["start"], PATTERN_TIME)

                task: TaskType  = {"start": start, "text": row["text"]}
                self._tasks.append(task)

        self._check_tasks()
                
    def _check_tasks(self) -> None:
        """Pop task window if there is a time for a task."""

        for el in self._tasks:

            now: datetime = datetime.now()

            if now > el["start"]:

                text: str = el["text"]
                self._tasks.remove(el)

                TaskWindow(text, self._tasks, scheme=self.scheme)

        self.after(1000, self._check_tasks)

    def _get_list(self) -> None:
        self.but_list["state"] = "disable"
        self.wait_window(TaskList(self._tasks, self.scheme))
        try:
            self.but_list["state"] = "active"
        except tk.TclError:
            sys.exit

    def _app_exit(self) -> None:
        """Get taskss from open TaskWinow, write down 
        all task and exit"""

        start: datetime = datetime.now() 
    
        el: tk.Widget
        for el in self.winfo_children():

            if isinstance(el, TaskWindow):
                textarea: tk.Text = el.winfo_children()[0]     # type: ignore
                text: str = textarea.get(1.0, "end")

                task: TaskType = {"start": start, "text": text}
                self._tasks.append(task)
        
        self._save_tasks(self._tasks, self.fname)
        self.destroy()


if __name__ == "__main__":        
    fname = "taskstemp.csv"
    with FileManager(fname):
        root = App("deep blue", fname)
        root.mainloop()
    
