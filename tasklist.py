import tkinter as tk 
from datetime import datetime, date

from colorschemes import COLORS
from hinting import  Scheme, TaskListType, TaskType
from taskwindow import TaskWindow
from service import get_text


class TaskList(tk.Toplevel):

    PATTERN_TIME: str = "%H:%M"
    
    def __init__(self, tasks: TaskListType, 
            scheme: Scheme) -> None:

        self._pool: list[str] = []    # Tasks that are presented int the today's list
        self._is_tasks: bool = True     # Toggle if any tasks exists 
        self._no_task_text: str = "There is no any task yet"
        self._tasks: TaskListType = tasks

        super().__init__()
        self.scheme: Scheme = scheme
        self._general_properties()
        self._set_widgets()
        self._set_tasks()

    def _general_properties(self):
        self._position_window()
        self.resizable(False, False)
        self.attributes("-topmost", 1)

    def _position_window(self) -> None:
        width: int = self.winfo_screenwidth()
        height: int = self.winfo_screenheight()
        x = (width - width*0.2)
        y = (height - height/2)

        self.geometry("+%d+%d" % (x, y))

    def _set_widgets(self) -> None:
        but_ok = tk.Button(self, text="OK", command=self._exit)
        but_ok.configure(**self.scheme["button"])
        but_ok.pack(side="bottom", fill="x")

    def _no_tasks(self) -> None:
        if self._is_tasks:
            now: datetime = datetime.now()
            time: str = now.strftime(self.PATTERN_TIME)
            self._set_task(text=self._no_task_text, time=time)
            self._is_tasks = False

    def _set_tasks(self) -> None:

        # __import__('pdb').set_trace()

        if self._tasks:
            task: TaskType
            for task in sorted(self._tasks, key=lambda x: x["start"]):
                now: datetime = datetime.now()
                today: date = now.date()
                date_: date = task["start"].date()    # date of task

                if date_ == today:
                    time: str = task["start"].strftime(self.PATTERN_TIME)
                    text: str = task["text"]

                    if text not in self._pool:
                        self._set_task(text=text, time=time)
                        self._pool.append(text)

            self._remove_no_task_text()

        if not self._pool:
            self._no_tasks()

        self.after(1500, self._set_tasks)

    def _remove_no_task_text(self):
        childs: list[tk.Widget] = self.winfo_children()

        if childs:
            frames: list[tk.Frame]
            frames = list(filter(        # type: ignore
                lambda x: isinstance(x, tk.Frame), childs))

            if len(frames) > 1:

                frame: tk.Frame
                for frame in frames:
                    frame: tk.Frame = frames[0]
                    try:
                        text: str = frame.winfo_children()[0].get()    # type: ignore

                        if text == self._no_task_text:
                            frame.destroy()

                    except tk.TclError as e:
                        pass

    def _set_task(self, text: str, time: str) -> None:
        frame = tk.Frame(self, **self.scheme["frame"])
        frame.pack()

        entry_task = tk.Entry(frame, width=20)
        entry_task.insert(0, text)
        entry_task.configure(**self.scheme["entry_task"])
        entry_task.pack(side="left")

        if text != self._no_task_text:
            entry_task.bind("<Button-1>", self._click_task)
        
        label_time = tk.Label(frame, text=time)
        label_time.configure(**self.scheme["label_time"])
        label_time.pack(side="left")

    def _click_task(self, e: tk.Event) -> None:
        """ Removes task from TaskList, from self._task and from self._pool"""

        childs: list[tk.Widget] = self.winfo_children()
        TaskWindow(tasks=self._tasks, text=e.widget.get(),
                scheme=self.scheme)

        frames: list[tk.Frame]
        frames = list(filter(     # type: ignore
            lambda x: isinstance(x, tk.Frame), childs))

        expected: str = e.widget.get()   # text that must be removed from list "tasks" and from TaskList object

        # find frame to delete
        for frame in frames:
            entry: tk.Entry = frame.winfo_children()[0]    # type: ignore
            text: str = entry.get()

            if expected == text:
                frame.destroy()
                break

        # remove from tasks
        task: TaskType
        for task in self._tasks:    # It needs to save exactly the same link to list object
            if task["text"] == expected:
                self._tasks.remove(task)

        # remove proper text from pool
        self._pool.remove(expected)

        # if no any task, a suitable message must be in TaskList
        if len(childs) == 2:
            self._is_tasks = True
            self._no_tasks()

    def _exit(self):
        self.destroy()
     

if __name__ == "__main__":

    pattern_time = '%Y-%m-%d %H:%M:%S'
    start = datetime.now()
    
    tasks: TaskListType = []

    for _ in range(2):
        text = get_text()
        
        task: TaskType = {
            "start": start,
            "text": text
            }

        tasks.append(task)

    # tasks: TaskListType = []

    root = tk.Tk()
    scheme: Scheme = COLORS["deep blue"]
    TaskList(tasks, scheme)
    root.mainloop()

