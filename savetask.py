import csv

from utils import PATTERN_TIME, FIELDNAMES
from hinting import TaskListType, TaskType


class SaveTask:

    @staticmethod
    def _validate(text: str) -> bool:
        """Validate the task is not empty."""
        if text == "\n":
            return False
        return True

    @staticmethod
    def _save_tasks(tasks: TaskListType, fname: str) -> None:

        with open(fname, "w") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=FIELDNAMES)
            writer.writeheader()
        
            task: TaskType
            for task in tasks:
                  
                start: str
                start = task["start"].replace(microsecond=0) \
                        .strftime(PATTERN_TIME)

                if SaveTask._validate(task["text"]):
                    task_to_write: dict[str, str]
                    task_to_write = {"start": start, "text": task["text"]}

                    writer.writerow(task_to_write)    # type: ignore


if __name__ == "__main__":
    
    from datetime import datetime, timedelta

    from service import get_text 
    from filemanager import FileManager

    from hinting import TaskListType

    tasks: TaskListType = []

    for _, delta in zip(range(3), [0, 0, 1]):
        text: str = get_text()
        start: datetime = datetime.now() + timedelta(days=delta)
        start = start.replace(microsecond=0)

        task: TaskType = {"start": start, "text": text}

        tasks.append(task)

    fname: str = "tasks_temp.csv"     # filename

    with FileManager(fname):
        """Manager that creates temporarily file and then remove it"""

        SaveTask._save_tasks(tasks, fname)

        with open(fname, "r") as csvfile:
            reader = csv.DictReader(csvfile, fieldnames=FIELDNAMES)
            next(reader)      # header

            row: dict[str, str]
            for i, row in enumerate(reader):
                
                msg_text: str = f"Wrong text of task {i}"
                assert tasks[i]["text"] == row["text"], msg_text

                start: datetime = datetime.strptime(row["start"], 
                                PATTERN_TIME)
                expect: datetime = tasks[i]["start"]
            
                msg_start: str = f"Wrong time of task {i}"
                assert expect == start, msg_start

