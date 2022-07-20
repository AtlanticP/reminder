import tkinter as tk 
import tkinter.font
import sys
from datetime import datetime, timedelta
from collections import namedtuple
#%%
Note = namedtuple("Note", ["start", "delta", "note_txt"])
                
class TaskWindow(tk.Tk):
    
    def __init__(self):
        super().__init__()
        self.font = tk.font.nametofont("TkDefaultFont")
        self.font.config(size=14, family="Times", weight="bold")
        
        self.but = tk.Button(self, text="exit", command=self._app_exit) #, width=50, height=50)
        self.but.pack()
        
        self.notes = []   # list of notes
        
        self._window_task()
        self._check_tasks()
        # self.update()
    
    def _window_task(self):
        win = tk.Toplevel(self)
        win.title("Task")
        win.attributes("-topmost", 1)
        win.geometry("300x300")
        
        tk.Label(win, text="Input your note").pack()
        
        font_txt = ("times", 13, "normal")
        self.txt = tk.Text(win, bg="light yellow", font=font_txt, height=8)
        self.txt.insert("1.0", "Input your note and choose time to remind")
        self.txt.bind("<FocusIn>", self._clear_placeholder)
        # import pdb; pdb.set_trace()
        self.txt.pack(fill=tk.X) #side=tk.LEFT, expand=True) # #expand=True,)
        # self.sb = tk.Scrollbar(self.txt)
        # self.sb.pack(side=tk.RIGHT, fill=tk.BOTH)
        
        
        tk.Button(win, text="exit", command=self._app_exit).pack(side=tk.LEFT)   # !!!!!!!!!!!!!          
        tk.Button(win, text="remind in 5 sec", command=self._save_note).pack()
        
        # import pdb; pdb.set_trace()
        self.update_idletasks()

    def _clear_placeholder(self, event):
        self.txt.delete("0.0", "end")
        
    def _save_note(self):
        txt = self.txt.get(1.0, "end")
        start = datetime.now()
        delta = timedelta(seconds=5)
        note = Note(start, delta, txt)
        self.notes.append(note)


    def _check_tasks(self):
        for i, (start, delta, txt) in enumerate(self.notes):
            now = datetime.now()

            if now - start > delta:
                note = self.notes.pop(i)
                print(note)
                
        self.after(1000, self._check_tasks)        
        
    def _app_exit(self):
        self.destroy()
        sys.exit()
        
if __name__ == "__main__":
    root = TaskWindow()
    root.mainloop()