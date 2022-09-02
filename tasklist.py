import tkinter as tk 
from datetime import datetime, date

from colorschemes import COLORS
from hinting import  Scheme, TaskListType, TaskType
from taskwindow import TaskWindow
from service import get_text


class TaskList(tk.Toplevel):

    def __init__(self, tasks: TaskListType, 
            scheme: Scheme) -> None:

        super().__init__()
        self.resizable(False, False)
        self.attributes("-topmost", 1)
        self.tasks: TaskListType = tasks
        self.scheme: Scheme = scheme
        self._set_widgets()

    def _set_widgets(self) -> None:
        self._set_tasks()
        but_ok = tk.Button(self, text="OK", command=self._exit)
        but_ok.configure(**self.scheme["button"])
        but_ok.pack(fill="x")

    def _set_tasks(self) -> None:
        pattern_time: str = "%H:%M"

        if self.tasks:

            task: TaskType
            for task in self.tasks:
                now: datetime = datetime.now()
                today: date = now.date()
                date_: date = task["start"].date()    # date of task

                if date_ == today:
                    time: str = task["start"].strftime(pattern_time)
                    text: str = task["text"]
                    self._set_task(text=text, time=time)

        else:
            text: str = "There is no any task yet"
            now: datetime = datetime.now()
            time: str = now.strftime(pattern_time)
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
        TaskWindow(tasks=self.tasks, text=e.widget.get(),
                scheme=self.scheme)

        # find frame to delete
        for frame in childs[:-1]:

            entry: tk.Entry = frame.winfo_children()[0]    # type: ignore
            text: str = entry.get()

            got_text: str = e.widget.get()
            
            if got_text == text:
                frame.destroy()
                break

    def _exit(self):
        self.destroy()
     

if __name__ == "__main__":

    pattern_time = '%Y-%m-%d %H:%M:%S'
    start = datetime.now()
    
    tasks: TaskListType = []

    for _ in range(10):
        text = get_text()
        
        task: TaskType = {
            "start": start,
            "text": text
            }

        tasks.append(task)

    root = tk.Tk()
    scheme: Scheme = COLORS["deep blue"]
    TaskList(tasks, scheme)
    root.mainloop()

