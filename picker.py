import tkinter as tk 
from tkcalendar import Calendar
from tktimepicker import AnalogPicker, AnalogThemes
import sys

from save_task import SaveTask
from dummy import DummyClass
#%%
class DateTimeWindow(SaveTask):
    
    def _win_task(self):

        self.win_dt = tk.Toplevel()        
        self.win_dt.geometry("350x550")
        self.win_dt.time = AnalogPicker(self.win_dt)
        self.win_dt.time.pack()
        
        theme = AnalogThemes(self.win_dt.time)
        theme.setDracula()
        
        self.win_dt.cal = Calendar(self.win_dt, selectmode="day")
        self.win_dt.cal.pack(fill="x")
        
        self.win_dt.but_ok = tk.Button(self.win_dt, text="ok", bg="#555", command=self._get_win_datetime)
        self.win_dt.but_ok.pack(expand=True, fill="both")
        
    def _get_win_datetime(self):
        date = self.win_dt.cal.selection_get().strftime("%Y-%m-%d")
        hours = self.win_dt.time.hours_picker.hours
        minutes = self.win_dt.time.minutes_picker.minutes
        start = f"{date} {hours}:{minutes}"
        self._save_task(start)        
        self.win_dt.destroy()        

class DummyDateTimeWindow(DateTimeWindow, DummyClass): pass
        

if __name__ == "__main__":
    
    root = tk.Tk()
    win_dt = DummyDateTimeWindow()
    win_dt.text = "text for dev purposes"
    win_dt._win_task()
    root.mainloop()