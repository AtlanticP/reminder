import tkinter as tk 
import tkinter.font
import sys
from datetime import datetime, timedelta
#%%

class TaskWindow(tk.Tk):
    
    def __init__(self):
        super().__init__()
        self.font = tk.font.nametofont("TkDefaultFont")
        self.font.config(size=14, family="Times", weight="bold")
        
        tk.Button(self, text="exit", command=self._app_exit).pack()
        
        self._win_task()
    
    def _win_task(self):
        win_task = tk.Toplevel()
        win_task.title("Scheduler")
        win_task.attributes("-topmost", 1)
        win_task.geometry("300x300")
        
        font_txt = ("times", 13, "normal")
        self.txt = tk.Text(win_task, bg="light yellow", font=font_txt, height=8)
        self.txt.insert("1.0", "Input your note and choose time to remind")
        self.txt.pack(fill=tk.X) #side=tk.LEFT, expand=True) # #expand=True,)
        
        
        tk.Button(win_task, text="exit", command=self._app_exit).pack(side=tk.LEFT)   # !!!!!!!!!!!!!          
        tk.Button(win_task, text="remind in 5 sec", command=self._save_note).pack()
        
    def _save_note(self):
        txt = self.txt.get(1.0, "end")
        start = datetime.now()
        delta = timedelta(seconds=5)
        note = Note(start, delta, txt)
        self.notes.append(note)
            
        # import pdb; pdb.set_trace()
        self.update_idletasks()
        
    def _app_exit(self):
        self.destroy()
        sys.exit()
        
if __name__ == "__main__":

    root = TaskWindow()
    root.mainloop()        