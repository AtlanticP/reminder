import tkinter as tk
#%%
class Colors:
    
    bg = "midnight blue"
    fg = "lime"
    activebackground = "#38418A",
    activeforeground="forest green"

class Button(Colors, tk.Button):
    
    def __init__(self, *args, **kwargs):
        super().__init__(bg=self.bg, fg=self.fg,
                         activebackground=self.activebackground,
                         activeforeground=self.activeforeground,
                         *args, **kwargs)

class Label(Colors, tk.Label):
    
    bg = "sky blue"
    fg = "black"
    
    def __init__(self, *args, **kwargs):
        super().__init__(bg=self.bg, fg=self.fg, *args, **kwargs)
        
    
    
if __name__ == "__main__":
   
    root = tk.Tk()
    Button(root, text="Button").pack()
    Label(root, text="Label").pack()
    root.mainloop()
    