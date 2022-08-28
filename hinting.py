from typing import Literal, Union, Any

Deep_blue = Literal["deep blue"]
Light = Literal["light"]
Brown = Literal["brown"]
Scheme_name = Union[Deep_blue, Light, Brown]

Main = Literal["main"]
Label_time = Literal["label_time"]
Button = Literal["button"]
Entry_task = Literal["entry_task"]
Frame_task = Literal["frame"]
Label_reminder = Literal["label_reminder"]
Widgets = Union[Main, Label_time, Button, Entry_task, 
        Frame_task, Label_reminder]

Bg = Literal["bg"]
Fg = Literal["fg"]
ActBg = Literal["activebackground"]
ActFg = Literal["activeforeground"]
Border = Literal["borderwidth"]
Hbg = Literal["highlightbackground"]
Relief = Literal["relief"]
Params = Union[Bg, Fg, ActBg, ActFg, Border, Hbg, Relief]

Scheme = dict[Widgets, dict[Params, str|int]]
Schemes = dict[Scheme_name, Scheme]

