import tkinter as tk
class Button(tk.Button):
    
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(bg="navy", fg="lime",
                         activebackground="#38418A",
                         activeforeground="forest green",
                         borderwidth=3, *args, **kwargs)


class Label(tk.Label):
    
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(bg="sky blue", fg="black", *args, **kwargs)


class LabelFrame(tk.LabelFrame):
    
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(bg="midnight blue", bd=4, *args, **kwargs)    


class Frame(tk.Frame):
    
    def __init__(self, *args, **kwargs):
        super().__init__(bg="#0E142F", *args, **kwargs)


if __name__ == "__main__":
   
    root = tk.Tk()
    border = LabelFrame(root)
    border.pack()
    
    Button(border, text="Button", width=8).pack()
    Label(border, text="Label").pack(fill="x")
    root.mainloop()
