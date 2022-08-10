import tkinter as tk
#%%
class Colors:
    
    bg = "navy"
    fg = "lime"
    activebackground = "#38418A",
    activeforeground="forest green"


class Button(tk.Button, Colors):
    
    relief="solid"    
    
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(bg=self.bg, fg=self.fg,
                         activebackground=self.activebackground,
                         activeforeground=self.activeforeground,
                         relief=self.relief, borderwidth=3, *args, **kwargs)


class Label(tk.Label, Colors):
    
    bg = "sky blue"
    fg = "black"
    
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(bg=self.bg, fg=self.fg, *args, **kwargs)


class LabelFrame(tk.LabelFrame):
    
    bg = "midnight blue"
    bd = 4
    
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(bg=self.bg, bd=self.bd, *args, **kwargs)    

    # def __init__(self, *args, **kwargs) -> None:
    #     super().__init__(bd = 6, bg = "black", *args, **kwargs)    


if __name__ == "__main__":
   
    root = tk.Tk()
    border = LabelFrame(root)
    border.pack()
    
    Button(border, text="Button", width=8).pack()
    Label(border, text="Label").pack(fill="x")
    root.mainloop()
