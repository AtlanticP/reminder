import tkinter as tk 
from datetime import datetime, date

from colorschemes import COLORS
from hinting import  Scheme, TaskListType, TaskType
from taskwindow import TaskWindow
from service import get_text

from datetime import datetime, timedelta  # !!!!!!!!!!!!!!!!!!!!!!!!!


class TaskList(tk.Toplevel):

    PATTERN_TIME: str = "%H:%M"
    
    def __init__(self, tasks: TaskListType, 
            scheme: Scheme) -> None:

        self._pool: set[str] = set()    # Tasks that are presented int the today's list
        self._no_task_text: str = "There is no any task yet"
        self._tasks: TaskListType = tasks
        self._toggle: bool = True     # if True set self._no_task_text

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
        """If there is no task, it displays the appropriate message"""
        now: datetime = datetime.now()
        time: str = now.strftime(self.PATTERN_TIME)
        self._set_task(text=self._no_task_text, time=time)
        self._toggle = False

    def _remove_no_task_text(self):
        """If there any task in tasks, it removes self._no_task_text"""
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

    def _remove_task(self, to_remove: str) -> None:
        """Remove a task with a specifiec text"""
        childs: list[tk.Widget] = self.winfo_children()

        frames: list[tk.Frame]
        frames = list(filter(     # type: ignore
            lambda x: isinstance(x, tk.Frame), childs))

        # find frame to delete
        for frame in frames:
            entry: tk.Entry = frame.winfo_children()[0]    # type: ignore
            text: str = entry.get()

            if to_remove == text:
                frame.destroy()
                break

    def _handle_pool(self) -> None:
        """If threre are texts in the pool that are not in tasks
        they must be removed from the pool and the tasks 
        with suitable texts ust be removed from TaskList"""

        # find text of tasks that needs to be removed
        tasks_text: set[str]    # texts of all tasks
        tasks_text = set(map(lambda task: task["text"], self._tasks))
        to_remove: set[str] = self._pool - tasks_text  # text of tasks that needs to be removed

        # remove frames with texts that needs to be removed
        text: str
        for text in to_remove:
            self._remove_task(text)

        # remove tasks
        self._pool = self._pool - to_remove
        if not self._pool and self._toggle:
            self._no_tasks()
        elif self._pool:
            self._remove_no_task_text()
 
    def _set_tasks(self) -> None:
        if self._tasks:
            task: TaskType
            for task in sorted(self._tasks, key=lambda x: x["start"]):
                self._handle_task(task)

        self._handle_pool()
        self.after(1000, self._set_tasks)

    def _handle_task(self, task: TaskType) -> None:
        now: datetime = datetime.now()
        today: date = now.date()
        date_: date = task["start"].date()    # date of task

        # check the task
        if date_ == today:
            time: str = task["start"].strftime(self.PATTERN_TIME)
            text: str = task["text"]

            if text not in self._pool:
                self._set_task(text=text, time=time)
                if text != self._remove_no_task_text:
                    self._pool.add(text)

            self._toggle = True

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

        # # remove proper text from pool
        self._pool.remove(expected)

        # if no any task, an appropriate messge must be in TaskList
        if len(childs) == 2:
            self._no_tasks()

    def _exit(self):
        self.destroy()
     

if __name__ == "__main__":

    pattern_time = '%Y-%m-%d %H:%M:%S'
    start = datetime.now()
    
    tasks: TaskListType = []

    for _ in range(1):
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

