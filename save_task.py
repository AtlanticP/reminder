import csv 
from datetime import datetime 
#%%
class SaveTask():
    
    def _save_task(self, start_str: str, task: str) -> None:
        
        
        with open("tasks.csv", "a", newline='') as csvfile:
            fieldnames = ("start", "task")

            dct = {
                "start": start_str,
                "task": task
                }
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writerow(dct)


if __name__ == "__main__":
    
    import os
    
    pattern_time = '%Y-%m-%d %H:%M:%S'
    start_str = datetime.now().strftime(pattern_time)
    task = f"text for dev purposes: {os.path.basename(__file__)}"
    SaveTask()._save_task(start_str, task)
    
    
    file = "tasks.csv"
    assert os.path.isfile(file), "Save Task doesn't work"
    