import tkinter as tk 
import tkinter.font
import sys
from datetime import datetime, timedelta
from collections import namedtuple
import csv
#%%

Note = namedtuple("Note", ["start", "delta", "note_txt"])

               
class TaskWindow(tk.Tk):
    
    def __init__(self):
        super().__init__()
        self.pattern_time = "%Y-%m-%d %H:%M:%S"
    
    def _window_task(self, text=None):
        self.win_task = tk.Toplevel(self)
        self.win_task.title("Task")
        self.win_task.attributes("-topmost", 1)
        self.win_task.geometry("300x300")
        
        font_txt = ("times", 13, "normal")
        self.txt_task = tk.Text(self.win_task, bg="light yellow", font=font_txt, height=8)

        if text:
            text = text
        else:
            text = "Input your note"
            self.txt_task.bind("<FocusIn>", self._clear_placeholder)    
        
        self.txt_task.insert("1.0", text)
        self.txt_task.pack(fill=tk.X) #side=tk.LEFT, expand=True) # #expand=True,)
        
        tk.Button(self.win_task, text="exit", command=self._app_exit).pack(side=tk.LEFT)   # !!!!!!!!!!!!!          
        tk.Button(self.win_task, text="remind in 5 sec", command=self._save_note).pack()
        
    def _clear_placeholder(self, event):
        self.txt_task.delete("0.0", "end")
        
    def _save_note(self):
        txt = self.txt_task.get(1.0, "end")
        start = datetime.now()
        delta = 5
        note = Note(start, delta, txt)
        
        with open("tasks.csv", "a", newline='') as csvfile:
            fieldnames = ("start", "delta", "task")
            dct = {
                "start": f"{start.strftime('%Y-%m-%d %H:%M:%S')}",
                "delta": f"seconds={delta}",
                "task": "{txt}"
                }
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writerow(dct)
        
        self.win_task.destroy()
        
    def _app_exit(self):
        self.destroy()
        sys.exit()
        
if __name__ == "__main__":
    root = TaskWindow()
    root.font = tk.font.nametofont("TkDefaultFont")
    root.font.config(size=14, family="Times", weight="bold")
    root._window_task()
    root.mainloop()