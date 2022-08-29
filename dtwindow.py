import tkinter as tk    
from tkcalendar import Calendar   # type: ignore
from tktimepicker import AnalogPicker, AnalogThemes    # type: ignore
from datetime import datetime

from hinting import TaskType
from service import PATTERN_TIME
    

class DateTimeWindow(tk.Toplevel):
    
    def __init__(self) -> None:
        """Initiate DateTimeWindow"""
        super().__init__()
        self.geometry("350x600")
        self.widget_time = AnalogPicker(self)    
        self.widget_time.pack()
        
        theme = AnalogThemes(self.widget_time)
        theme.setDracula()
        
        self.widget_cal = Calendar(self, selectmode="day")
        self.widget_cal.pack(fill="x")
        
    def _get_datetime(self) -> datetime:
        date = str(self.widget_cal.selection_get())
        hours: str = str(self.widget_time.hours_picker.hours)
        minutes: str = str(self.widget_time.minutes_picker.minutes)

        if len(hours) == 1:
            hours = '0' + hours

        if len(minutes) == 1:
            minutes = "0" + minutes

        start_str: str = f"{date} {hours}:{minutes}:00"
        start: datetime 
        start = datetime.strptime(start_str, PATTERN_TIME)

        return start
        

if __name__ == "__main__":
    
    import os 
    import csv
    
    task = f"text for dev purposes: {os.path.basename(__file__)}"
    
    root = tk.Tk()
    
    dt: datetime
    dt = DateTimeWindow()._get_datetime()

    root.mainloop()
   
    assert isinstance(dt, int)

