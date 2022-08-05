import tkinter as tk    
from tkcalendar import Calendar   # type: ignore
from tktimepicker import AnalogPicker, AnalogThemes    # type: ignore

from save_task import SaveTask
#%%

class CustomToplevel(tk.Toplevel):
    """ to pass type checking"""
    time: AnalogPicker
    cal: Calendar
    but_ok: tk.Button
    text = "text for dev purposes"
    
class DateTimeWindow(SaveTask):
    
    def _init_win_dt(self) -> None:

        self.win_dt = CustomToplevel()
        self.win_dt.geometry("350x550")
        self.win_dt.time = AnalogPicker(self.win_dt)    
        self.win_dt.time.pack()
        
        theme = AnalogThemes(self.win_dt.time)
        theme.setDracula()
        
        self.win_dt.cal = Calendar(self.win_dt, selectmode="day")
        self.win_dt.cal.pack(fill="x")
        
        self.win_dt.but_ok = tk.Button(self.win_dt, text="ok", bg="#555", command=self._get_win_datetime)
        self.win_dt.but_ok.pack(expand=True, fill="both")
        
    def _get_win_datetime(self) -> None:
        date = self.win_dt.cal.selection_get().strftime("%Y-%m-%d")
        hours = self.win_dt.time.hours_picker.hours
        minutes = self.win_dt.time.minutes_picker.minutes
        start = f"{date} {hours}:{minutes}"
        self._save_task(start, task)        
        self.win_dt.destroy()        
        

if __name__ == "__main__":
    
    import os 
    
    task = f"text for dev purposes: {os.path.basename(__file__)}"
    
    root = tk.Tk()
    win_dt = DateTimeWindow()
    win_dt._init_win_dt()
    root.mainloop()