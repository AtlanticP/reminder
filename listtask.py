import tkinter as tk 
from datetime import datetime 
import random
import string
import csv
import os

from colors import COLORS
from hinting import Schemes, Accepted_structures

class ListTask(tk.Toplevel):

    def __init__(self, fname: str, scheme: Schemes, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.geometry="400x400"
        self.resizable(False, False)
        self.attributes("-topmost", 1)
        self.fname = fname      # File name
        self.tasks = []
        # import pdb; pdb.set_trace()
        self.scheme = COLORS[scheme]    # type: Accepted_structures
        # self.label_tasks = {}
        # self.label_time = {}
        # self.buttons = []
        self._set_widgets()
        # self._set_colorscheme(scheme)

    def _set_widgets(self) -> None:
        self._set_tasks()
        but_ok = tk.Button(self, text="OK", command=self._exit)
        but_ok.configure(**self.scheme["button"])
        but_ok.pack(fill="x")

    def _set_tasks(self) -> None:

        with open(self.fname) as csvfile:
            reader = csv.DictReader(csvfile)

            for i, line in enumerate(reader):

                self.tasks.append(line)    # why? 
                time = line["start"][11:-3]

                # The code below returns text of lentgh equals to 23.
                s = line["task"]    
                task = (s[:20] + "...") if len(s) > 23 else s + " "*(23 - len(s))

                self._set_task(i=i, task=task, time=time)

    def _set_task(self, i, task: str, time: str) -> None:
        frame = tk.Frame(self, **self.scheme["frame"])
        frame.pack()

        entry_task = tk.Entry(frame, width=20)
        entry_task.insert(0, task)
        entry_task.configure(**self.scheme["entry_task"])
        entry_task.pack(side="left")
        
        label_time = tk.Label(frame, text=time)
        label_time.configure(**self.scheme["label_time"])
        label_time.pack(side="left")

    def _exit(self):
        self.destroy()
     

def get_task()-> str:
    '''get random task: random text'''
    
    s = string.ascii_lowercase + string.digits
    n_letters = lambda: random.randint(1, 10)
    n_words = random.randint(1, 20)
    get_word = lambda : ''.join(random.sample(s, n_letters()))
    task: str = ' '.join(get_word() for _ in range(n_words))

    return task + "\n" 

class FileManager:
    """Context maneger that creates temporarily file for dev purpose"""

    def __init__(self, fname: str) -> None:
        self.fname = fname

    def __enter__(self):
        pattern_time = '%Y-%m-%d %H:%M:%S'
        start_str = datetime.now().strftime(pattern_time)
        tasks: list[str] = []
        
        with open(self.fname, "w") as csvfile:
            fieldnames = ("start", "task")
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
        
            for _ in range(10):
                task = get_task()
                
                dct = {
                    "start": start_str,
                    "task": task
                    }
                writer.writerow(dct)    # type: ignore
                
    def __exit__(self, type, value, traceback):
        os.remove(self.fname)
        

if __name__ == "__main__":

    fname = "tasks_temp.csv"

    with FileManager(fname):

        root = tk.Tk()
        ListTask(fname, "deep blue")
        root.mainloop()


