import tkinter as tk
import tkinter.font    # type: ingore
import time
import os
import csv
from datetime import datetime

from movewin import MoveWin
from taskwindow import TaskWindow
from colors import COLORS
from hinting import Scheme_name, Scheme
from tasklist import TaskList

class App(MoveWin):
    
    def __init__(self) -> None:
        super().__init__()

        self._pattern_time = "%Y-%m-%d %H:%M:%S"
        self.tasks = []

        self.fname: str = "tasks.csv" # file where tasks are stored
        if not os.path.isfile(self.fname):
            with open(self.fname, "w") as file:
                fieldnames = ("start", "text")
                writer = csv.DictWriter(file, fieldnames=fieldnames)
                writer.writeheader()
                
        self.buttons = []
        self.scheme: Scheme_name = "deep blue"
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
        my_font = ("times", 24)
        self.label_time = tk.Label(self, font=my_font, height=3)
        self.label_time.pack(side=tk.LEFT)

        params_but = {"side":"top", "fill":"both", "expand":True}
        
        but_task = tk.Button(self, text="task", 
                            command=self._window_task)
        but_task.pack(**params_but)
        self.buttons.append(but_task)
        
        but_list = tk.Button(self, text="list", 
                            command=self._get_list)
        but_list.pack(**params_but)
        self.buttons.append(but_list)


        but_exit = tk.Button(self, text="exit", 
                            command=self._app_exit)
        but_exit.pack(**params_but)
        self.buttons.append(but_exit)
        
    def _set_colorscheme(self):
        scheme: Scheme  = COLORS[self.scheme]
        self.configure(**scheme["main"]) 
        self.label_time.configure(**scheme["label_time"])
        
        for button in self.buttons:
            button.configure(**scheme["button"])
        
    def _current_time(self) -> None:
        time_string = time.strftime("%H:%M:%S %p")
        self.label_time.config(text=time_string)
        self.after(1000, self._current_time)

    def _window_task(self) -> None:
        TaskWindow(text=None, tasks=self.tasks,
                    scheme_name=self.scheme)
            
    def _load_tasks(self) -> None:
        """ Read csv file where tasks are stored, append tasks 
            and call function that check tasks to appears.
        """

        with open(self.fname, "r") as csvfile:
            fieldnames = ("start", "text")
            reader = csv.DictReader(csvfile, fieldnames=fieldnames)
            next(reader)    # header
            
            for row in reader:
                start = datetime.strptime(row["start"], self._pattern_time)
                self.tasks.append({"start": start, "text": row["text"]})

        self._check_tasks()
                
    def _check_tasks(self) -> None:
        """Pop task window if there is a time for a task."""
    
        for i, el in enumerate(self.tasks):

            now = datetime.now()

            if now > el["start"]:

                TaskWindow(self.tasks, text=el["text"])
                self.tasks.pop(i)
        
        self.after(1000, self._check_tasks)

    def _get_list(self) -> None:
        TaskList(self.tasks, self.scheme)
    
    def _app_exit(self) -> None:
        """Get taskss from open TaskWinow, write down 
        all task and exit"""

        start: str = datetime.now().strftime(self._pattern_time)
    
        for el in self.winfo_children():

            if isinstance(el, tk.Toplevel):
                textarea: tk.Text = el.winfo_children()[0]     # type: ignore
                text = textarea.get(1.0, "end")

                if text:
                    self.tasks.append({"start": start, "text": text})

        
        with open(self.fname, "w") as csvfile:
            fieldnames: tuple["str", "str"] = ("start", "text")
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()

            for task in self.tasks:
                writer.writerow({"start": start, "text": task["text"]})

        self.destroy()


if __name__ == "__main__":        
    root = App()
    root.mainloop()
    
