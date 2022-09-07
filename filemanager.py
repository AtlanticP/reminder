import csv
import os


class FileManager:
    """Context maneger that creates temporarily file for dev purpose"""

    def __init__(self, fname: str) -> None:
        self.fname = fname

    def __enter__(self):

        with open(self.fname, "w") as csvfile:
            fieldnames = ("start", "text")
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()

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
