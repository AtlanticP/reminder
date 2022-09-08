import os
import getpass
from typing import Optional
import sys

from app import App
from configuration import get_config, Config


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
        try:
            result: Config = get_config(line)

            if result:
                param: str
                key: str
                param, key = result
                configs[param] = key

        except ValueError:
            msg = "Incorrect configuration file. Must be 'scheme_name = brown' or  'scheme_name = deep blue"
            print(msg)
            input("press <Enter> key to exit")
            sys.exit()

app = App(**configs)    # type: ignore
app.mainloop()

