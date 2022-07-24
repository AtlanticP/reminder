import csv 
from datetime import datetime 
#%%

class SaveTask:
    
    def _save_task(self, start_str: type[str]) -> None:

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


#%% These three classes were made only for test purposes

class DummyGetTask:
    
    def get(self, *args, **kwargs) -> str:
        return "text for dev purposes"
    
    def destroy(self, *args, **kwargs) -> None:
        pass

class DummyClass: 
    
    txt_task = DummyGetTask()
    win_task = DummyGetTask()
    
class DummySaveTask(SaveTask, DummyGetTask, DummyClass): 
    pass
        
if __name__ == "__main__":
    
    pattern_time = '%Y-%m-%d %H:%M:%S'
    start = datetime.now().strftime(pattern_time)
    DummySaveTask()._save_task(start)
    

        