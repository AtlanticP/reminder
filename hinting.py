from typing import Literal, Union, Any

Deep_blue = Literal["deep blue"]
Light = Literal["light"]
Brown = Literal["brown"]
Schemes = Union[Deep_blue, Light, Brown]

Main = Literal["main"]
Label_time = Literal["label_time"]
Button = Literal["button"]
Entry_task = Literal["entry_task"]
Frame_task = Literal["frame"]
Structure = Union[Main, Label_time, Button, Entry_task, Frame_task]

Bg = Literal["bg"]
Fg = Literal["fg"]
ActBg = Literal["activebackground"]
ActFg = Literal["activeforeground"]
Border = Literal["borderwidth"]
Relief = Literal["relief"]
Params = Union[Bg, Fg, ActBg, ActFg, Border, Relief]

Accepted_structures = dict[Structure, dict[Params, str|int]]
# Accepted_schemes = dict[Schemes, dict[Structure, dict[Params, str|int]]]
Accepted_schemes = dict[Schemes, Accepted_structures]


