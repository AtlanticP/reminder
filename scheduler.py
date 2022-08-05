import tkinter as tk 
import tkinter.font
import sys
from save_task import SaveTask
#%%
               
class SchedulerWindow(SaveTask, tk.Tk):
    
    def __init__(self) -> None:
        super().__init__()
        self.font = tk.font.nametofont("TkDefaultFont")
        self.font.config(size=14, family="Times", weight="bold")
        
        tk.Button(self, text="exit", command=self._app_exit).pack()
        
        self._window_scheduler()
    
    def _window_scheduler(self) -> None:
        self.win_task = tk.Toplevel(self)
        self.win_task.title("Scheduler")
        # win.attributes("-topmost", 1)
        self.win_task.geometry("300x300")
        
        tk.Label(self.win_task, text="Input your note").pack()
        
        font_txt = ("times", 13, "normal")
        self.txt_task = tk.Text(self.win_task, bg="light yellow", font=font_txt, height=8)
        # import pdb; pdb.set_trace()
        self.txt_task.pack(fill=tk.X) #side=tk.LEFT, expand=True) # #expand=True,)
        # self.sb = tk.Scrollbar(self.txt)
        # self.sb.pack(side=tk.RIGHT, fill=tk.BOTH)
        
        tk.Button(self.win_task, text="exit", command=self._app_exit).pack(side=tk.LEFT)   # !!!!!!!!!!!!!          
        tk.Button(self.win_task, text="remind in 5 sec", command=self.remind_in).pack()

    def remind_in(self) -> None:
        self._save_task()
        self.win_task.destroy()
        
    def _app_exit(self):
        self.destroy()
        sys.exit()
        
if __name__ == "__main__":
    root = SchedulerWindow()
    root.mainloop()