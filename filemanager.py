import random 
import string
from datetime import datetime
import csv
import os

from hinting import TaskListType

class FileManager:
    """Context maneger that creates temporarily file for dev purpose"""

    def __init__(self, fname: str) -> None:
        self.fname = fname

    def __enter__(self):

        with open(self.fname, "w") as csvfile:
            fieldnames = ("start", "text")
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
                
    # def _write_tasks(self, tasks: TaskListType) -> None:
    #
    #     PATTERN_TIME = '%Y-%m-%d %H:%M:%S'
    #     start_str: str = datetime.now().strftime(PATTERN_TIME)
    #     
    #     with open(self.fname, "a") as csvfile:
    #         fieldnames = ("start", "text")
    #         writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    #         writer.writeheader()
    #     
    #         for _ in range(3):
    #             text = get_text()
    #             
    #             dct = {
    #                 "start": start_str,
    #                 "text": text
    #                 }
    #             writer.writerow(dct)    # type: ignore

    def __exit__(self, type, value, traceback):
        os.remove(self.fname)
        

if __name__ == "__main__":

    fname = "tasks_temp.csv"
    header = ("start,text\n")

    with FileManager(fname):
        assert os.path.isfile(fname), f"FileManager does not create {fname}"

        with open(fname, "r") as file:
            reader: str = file.read()
            assert header == reader, f"FileManager write incorrect header"

    assert not os.path.isfile(fname), f"FileManager does not remove {fname}"
