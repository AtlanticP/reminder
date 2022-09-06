import tkinter as tk
import tkinter.font    # type: ingore
import time
import os
import csv
from datetime import datetime 
from typing import Union

from movewin import MoveWin
from taskwindow import TaskWindow
from colorschemes import COLORS
from tasklist import TaskList
from savetask import SaveTask
from service import PATTERN_TIME, FIELDNAMES

from hinting import Scheme_name, Scheme, TaskType, TaskListType 


class App(MoveWin, SaveTask):
    
    def __init__(self, scheme_name) -> None:
        super().__init__()

        self.tasks: TaskListType = []

        self.fname: str = "tasks.csv" # file where tasks are stored
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
        
        but_list = tk.Button(self, text="today", 
                            command=self._get_list)
        but_list.pack(**params_but)
        self.buttons.append(but_list)


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
        TaskWindow(text=None, tasks=self.tasks,
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
                self.tasks.append(task)

        self._check_tasks()
                
    def _check_tasks(self) -> None:
        """Pop task window if there is a time for a task."""

        for i, el in enumerate(self.tasks):

            now: datetime = datetime.now()

            if now > el["start"]:

                TaskWindow(el["text"], self.tasks, scheme=self.scheme)
                self.tasks.pop(i)
        
        self.after(1000, self._check_tasks)

    def _get_list(self) -> None:
        TaskList(self.tasks, self.scheme)

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
                self.tasks.append(task)
        
        self._save_tasks(self.tasks, self.fname)
        self.destroy()


if __name__ == "__main__":        
    root = App("deep blue")
    PATH_ICON = "media/reminder.png"
    # PATH_ICON = "icon.ico"
    photo = tk.PhotoImage(file=PATH_ICON)
    root.iconphoto(False, photo)
    root.mainloop()
    
