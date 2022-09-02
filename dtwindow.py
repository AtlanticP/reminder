import tkinter as tk    
from tkcalendar import Calendar   # type: ignore
from tktimepicker import AnalogPicker, AnalogThemes    # type: ignore
from datetime import datetime

from service import PATTERN_TIME
    

class DateTimeWindow(tk.Toplevel):

    def __init__(self) -> None:
        super().__init__()

        self.geometry("350x600")

        self.widget_time = AnalogPicker(self)    
        self.widget_time.pack()
        
        theme = AnalogThemes(self.widget_time)
        theme.setDracula()
        
        self.widget_cal = Calendar(self, selectmode="day")
        self.widget_cal.pack(fill="x")

        self.but_ok = tk.Button(self, bg="#3D3D3D", text="ok",
                activebackground="#2B2B2B", command=self._dt_exit)
        self.but_ok.pack(fill="both", expand=True)
        
        self.start = self._get_datetime()

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

    def _dt_exit(self):
        self.start = self._get_datetime()
        self.destroy()


if __name__ == "__main__":
    
    root = tk.Tk()
    
    dt: datetime
    dt = DateTimeWindow()._get_datetime()

    root.mainloop()

