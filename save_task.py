import csv 
from datetime import datetime 
from dummy import DummyClass
#%%
class SaveTask(DummyClass):
    
    def _save_task(self, start_str: str) -> None:

        text = self.txt_task.get(1.0, "end")
        
        with open("tasks.csv", "a", newline='') as csvfile:
            fieldnames = ("start", "task")

            dct = {
                "start": start_str,
                "task": text
                }
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writerow(dct)
        
        self.win_task.destroy()


class DummySaveTask(SaveTask, DummyClass): 
    pass

if __name__ == "__main__":
    
    pattern_time = '%Y-%m-%d %H:%M:%S'
    start = datetime.now().strftime(pattern_time)
    DummySaveTask()._save_task(start)
    
    import os
    
    file = "tasks.csv"
    assert os.path.isfile(file), "Save Task doesn't work"
    