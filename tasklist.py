import tkinter as tk 
from datetime import datetime 
import random
import string
import csv
import os

from colors import COLORS
from hinting import Scheme_name, Scheme
from taskwindow import TaskWindow

class TaskList(tk.Toplevel):

    def __init__(self, fname: str, scheme: Scheme_name="deep blue",
                *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.resizable(False, False)
        self.attributes("-topmost", 1)
        self.fname = fname      # File name
        self.tasks = []
        self.scheme: Scheme = COLORS[scheme]
        self._set_widgets()

    def _set_widgets(self) -> None:
        self._set_tasks()
        but_ok = tk.Button(self, text="OK", command=self._exit)
        but_ok.configure(**self.scheme["button"])
        but_ok.pack(fill="x")

    def _set_tasks(self) -> None:
        today = datetime.now().date()

        with open(self.fname) as csvfile:
            reader = csv.DictReader(csvfile)
            text = None

            while True:

                try:
                    line = next(reader)
                    pattern_time = '%Y-%m-%d %H:%M:%S'
                    date = datetime.strptime(line["start"],
                            pattern_time).date()

                    if date == today:
                        time = line["start"][11:-3]
                        text = line["text"]

                        self._set_task(text=text, time=time)

                except StopIteration:

                    if not text:
                        pattern_time = "%H:%M"
                        time = datetime.now().strftime(pattern_time)
                        text = "There is no any task yet"
                        self._set_task(text=text, time=time)

                    break

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

class FileManager:
    """Context maneger that creates temporarily file for dev purpose"""

    def __init__(self, fname: str) -> None:
        self.fname = fname

    def __enter__(self):
        pattern_time = '%Y-%m-%d %H:%M:%S'
        start_str = datetime.now().strftime(pattern_time)
        
        with open(self.fname, "w") as csvfile:
            fieldnames = ("start", "text")
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
        
            for _ in range(10):
                text = get_text()
                
                dct = {
                    "start": start_str,
                    "text": text
                    }
                writer.writerow(dct)    # type: ignore
                
    def __exit__(self, type, value, traceback):
        os.remove(self.fname)
        

if __name__ == "__main__":

    fname = "tasks_temp.csv"

    with FileManager(fname):

        root = tk.Tk()
        TaskList(fname, "deep blue")
        root.mainloop()


