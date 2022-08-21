from typing import Literal, Union

Deep_blue = Literal["deep blue"]
Light = Literal["light"]
Brown = Literal["brown"]
Schemes = Union[Deep_blue, Light, Brown]

Main = Literal["main"]
Label_time = Literal["label_time"]
Button = Literal["button"]
Label = Literal["label"]
Structure = Union[Main, Label_time, Button, Label]

Bg = Literal["bg"]
Fg = Literal["fg"]
ActBg = Literal["activebackground"]
ActFg = Literal["activeforeground"]
Params = Union[Bg, Fg, ActBg, ActFg]

Accepted_schemes = dict[Schemes, dict[Structure, dict[Params, str]]]

