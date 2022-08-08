import tkinter as tk    
from tkcalendar import Calendar   # type: ignore
from tktimepicker import AnalogPicker, AnalogThemes    # type: ignore
from functools import partial

from save_task import SaveTask
#%%

class CustomToplevel(tk.Toplevel):
    """ to pass type checking"""
    time: AnalogPicker
    cal: Calendar
    but_ok: tk.Button
    text = "text for dev purposes"
    
class DateTimeWindow(SaveTask):
    
    def _init_win_dt(self, task: str) -> None:
        self.win_dt = CustomToplevel()
        self.win_dt.geometry("350x550")
        self.win_dt.time = AnalogPicker(self.win_dt)    
        self.win_dt.time.pack()
        
        theme = AnalogThemes(self.win_dt.time)
        theme.setDracula()
        
        self.win_dt.cal = Calendar(self.win_dt, selectmode="day")
        self.win_dt.cal.pack(fill="x")
        
        func_get_win = partial(self._get_win_datetime, task)
        self.win_dt.but_ok = tk.Button(self.win_dt, text="ok", bg="#555", command=func_get_win)
        self.win_dt.but_ok.pack(expand=True, fill="both")
        
    def _get_win_datetime(self, task: str) -> None:
        date = self.win_dt.cal.selection_get().strftime("%Y-%m-%d")
        hours = self.win_dt.time.hours_picker.hours
        minutes = self.win_dt.time.minutes_picker.minutes
        start_str = f"{date} {hours}:{minutes}"

        if len(start_str) == 15:
            start_str += "0"
        
        start_str += ":00"    # seconds
        
        self._save_task(start_str, task)        
        self.win_dt.destroy()        
        

if __name__ == "__main__":
    
    import os 
    import csv
    
    task = f"text for dev purposes: {os.path.basename(__file__)}"
    
    root = tk.Tk()
    win_dt = DateTimeWindow()
    win_dt._init_win_dt(task)
    root.mainloop()

    file_name = "tasks.csv"
    with open(file_name, "r") as file:
        reader = csv.DictReader(file, fieldnames=["time", "task"])
        first = last = next(iter(reader))
        
        for last in reader: pass
    
    assert last['task'] == task, "Smth. wrong with _get_win_datetime"
