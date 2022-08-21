import tkinter as tk 
from datetime import datetime 
import random
import string
import csv
import os

# from colors import COLORS

class ListTask(tk.Toplevel):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


def get_task()-> str:
    '''get random task: random text'''
    
    s = string.ascii_lowercase + string.digits
    n_letters = lambda: random.randint(1, 10)
    n_words = random.randint(1, 20)
    get_word = lambda : ''.join(random.sample(s, n_letters()))
    task: str = ' '.join(get_word() for _ in range(n_words))

    return task + "\n" 

class FileManager:
    """Context maneger that creates temporily file for testing purposes"""

    def __init__(self) -> None:
        self.fname = "tasks_temp.csv"

    def __enter__(self):
        pattern_time = '%Y-%m-%d %H:%M:%S'
        start_str = datetime.now().strftime(pattern_time)
        tasks: list[str] = []
        
        with open(self.fname, "w") as csvfile:
            fieldnames = ("start", "task")
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            for _ in range(5):
                task = get_task()
                tasks.append(task)
                
                dct = {
                    "start": start_str,
                    "task": task
                    }
                writer.writerow(dct)    # type: ignore
                
    def __exit__(self, *args, **kwargs):
        os.remove(self.fname)
        

if __name__ == "__main__":

    with FileManager():
        print(os.listdir())
        root = tk.Tk()
        ListTask(root)
        root.mainloop()
    os.listdir()
