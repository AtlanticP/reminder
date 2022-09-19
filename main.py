import os
import sys

from app import App
from configuration import get_config, Config


CURRENT_DIRECTORY: str = os.path.dirname(os.path.realpath(__file__))

FILE_TASKS: str = "tasks.csv"   # File name of task file
PATH_TASKS: str = os.path.join(CURRENT_DIRECTORY, FILE_TASKS)    # default path to file where tasks are located

FILE_CONFIG: str = "config.cfg"    # File name of config file
PATH_CONFIG: str = os.path.join(CURRENT_DIRECTORY, FILE_CONFIG) 

# If there is no config file it is created with default values
if not os.path.isfile(PATH_CONFIG):
    with open(PATH_CONFIG, "w") as file:
        text = "# path to file where tasks are located\n"
        file.write(text)
        file.write(f"path_tasks = {PATH_TASKS}\n")
        file.write("# scheme_name = deep blue\n")
        file.write("scheme_name = brown\n")

# Read config file
configs: dict[str, str] = {}

with open(PATH_CONFIG, "r") as file:

    line: str
    for line in file:
        try:
            result: Config = get_config(line)

            if result:
                param: str
                key: str
                param, key = result
                configs[param] = key

        except ValueError:
            msg = "Incorrect configuration file. Must be 'path_tasks = home/atl/Apps/reminder/tasks.csv' or 'scheme_name = deep blue"
            print(msg)
            input("press <Enter> key to exit")
            sys.exit()

if __name__ == "__main__":
    app = App(**configs)    # type: ignore
    app.mainloop()

