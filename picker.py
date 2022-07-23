import tkinter as tk 
from tkcalendar import Calendar
from tktimepicker import AnalogPicker, AnalogThemes
import sys
#%%
class DateTimeWindow(tk.Tk):
    
    def __init__(self):
        super().__init__()
        
        self.geometry("350x550")
        self.time = AnalogPicker(self)
        self.time.pack()
        
        theme = AnalogThemes(self.time)
        theme.setDracula()
        
        self.cal = Calendar(self, selectmode="day")
        self.cal.pack(fill="x") #side=tk.LEFT, expand=True)

        
        self.but_ok = tk.Button(self, text="ok", bg="#555", command=self._get_datetime)
        self.but_ok.pack(expand=True, fill="both")
        
    def _get_datetime(self):
        date = self.cal.selection_get().strftime("%Y-%m-%d")
        hours = self.time.hours_picker.hours
        minutes = self.time.minutes_picker.minutes
        datetime_str = f"{date} {hours}:{minutes}"
        # self.
        
        # self.destroy()
        
    

if __name__ == "__main__":
    
    root = DateTimeWindow()
    root.mainloop()