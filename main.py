import os
import getpass
from typing import Optional

from app import App

FILE_NAME: str = "config.cfg"    # File name of config file
user = getpass.getuser()    # name of the current user
DIRS_CONFIG: list[str] = [     # Directories where config file can be located
        f"/home/{user}/.config/reminder",
        os.getcwd()
        ]
PATH_CONFIG: Optional[str] = None

dir: str
for dir_ in DIRS_CONFIG:
    PATH_ = os.path.join(dir_, FILE_NAME)
    if PATH_:
        PATH_CONFIG = PATH_
        break

# If there is no config file it is created with default values
if not PATH_CONFIG:
    PATH_CONFIG = os.path.join(os.getcwd(), FILE_NAME)

    with open(PATH_CONFIG, "w") as file:
        writer = file.write("scheme_name = brown")

# Read config file
configs: dict[str, str] = {}

with open(PATH_CONFIG, "r") as file:
    for line in file:
        param, arg = [i.strip() for i in line.split("=")]
        configs[param] = arg

app = App(**configs)
app.mainloop()

