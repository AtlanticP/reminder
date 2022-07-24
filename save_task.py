import csv 
#%%

class SaveTask:
    
    def _save_task(self, start: type[str]):
        text = self.txt_task.get(1.0, "end")

        with open("tasks.csv", "a", newline='') as csvfile:
            fieldnames = ("start", "task")
            dct = {
                "start": start,
                "task": text
                }
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writerow(dct)
        
        self.win_task.destroy()
