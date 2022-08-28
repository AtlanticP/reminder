import tkinter as tk 
from datetime import datetime 
import random
import string
import csv
import os
from typing import Optional

from colors import COLORS
from hinting import Scheme_name, Scheme
from taskwindow import TaskWindow



class TaskList(tk.Toplevel):

    def __init__(self, tasks: list[dict], 
            scheme: Scheme_name) -> None:
        super().__init__()
        self.resizable(False, False)
        self.attributes("-topmost", 1)
        self.tasks = tasks
        self.scheme: Scheme = COLORS[scheme]
        self._set_widgets()

    def _set_widgets(self) -> None:
        self._set_tasks()
        but_ok = tk.Button(self, text="OK", command=self._exit)
        but_ok.configure(**self.scheme["button"])
        but_ok.pack(fill="x")

    def _set_tasks(self) -> None:
        pattern_time = "%H:%M"
        today = datetime.now().date()

        text: Optional[str] = None

        for task in self.tasks:

            date = task["start"].date()

            if date == today:
                time = task["start"].strftime(pattern_time)
                text = task["text"]

                if not text:
                    text = "There is no any task yet"
                    time = today.strftime(pattern_time)
                    self._set_task(text=text, time=time)

                self._set_task(text=text, time=time)


    def _set_task(self, text: str, time: str) -> None:
        frame = tk.Frame(self, **self.scheme["frame"])
        frame.pack()

        entry_task = tk.Entry(frame, width=20)
        entry_task.insert(0, text)
        entry_task.configure(**self.scheme["entry_task"])
        entry_task.pack(side="left")

        entry_task.bind("<Button-1>", self._click_task)
        
        label_time = tk.Label(frame, text=time)
        label_time.configure(**self.scheme["label_time"])
        label_time.pack(side="left")

    def _click_task(self, e: tk.Event) -> None:
        childs: list[tk.Widget] = self.winfo_children()
        TaskWindow(e.widget.get())

        for widget in childs:

            if isinstance(widget, tk.Frame):
                entry_task: tk.Entry = widget.winfo_children()[0]    # type: ignore
                text: str = entry_task.get()
                
                if e.widget.get() == text:
                    widget.destroy()

    def _exit(self):
        self.destroy()
     

def get_text()-> str:
    """get random text"""
    
    s = string.ascii_lowercase + string.digits
    n_letters = lambda: random.randint(1, 10)
    n_words = random.randint(1, 20)
    get_word = lambda : ''.join(random.sample(s, n_letters()))
    text: str = ' '.join(get_word() for _ in range(n_words))

    return text + "\n" 
                
if __name__ == "__main__":

    pattern_time = '%Y-%m-%d %H:%M:%S'
    start = datetime.now()
    
    tasks: list[dict] = []

    for _ in range(10):
        text = get_text()
        
        dct = {
            "start": start,
            "text": text
            }

        tasks.append(dct)

    root = tk.Tk()
    scheme: Scheme_name = "deep blue"
    TaskList(tasks, scheme)
    root.mainloop()

