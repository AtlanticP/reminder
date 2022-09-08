"""
Here, Python processes the configuration file: config.cfg that is located
in $HOME/.config/reminder or in the current directories.
"""

from typing import Iterable, Optional


Config = Optional[Iterable[str]]

def valid_line(line: str) -> bool:
    """Validate text from config.cfg file: spaces and '#' are skipped"""

    if line.startswith("#") or line.isspace():
        return False

    return True

def get_config(line: str) -> Config:
    config: Config = None

    if valid_line(line):
        config = tuple(i.strip() for i in line.split("="))

    return config


if __name__ == "__main__":
    lines: list[str] = ["#", "   ", "scheme_name"]
    expected_valid_lines: list[bool] = [False, False, True]

    for line, exp in zip(lines, expected_valid_lines):
        msg: str
        msg = f"valid_line returns wrong value: {valid_line(line)} != {exp}"
        assert valid_line(line) == exp, msg
    
    expected_get_configs: list[Config]
    expected_get_configs = [None, None, ("scheme_name", "brown")]
    msg_valid_lines = "valid_config function returns wrong value"

    for line, exp in zip(lines, expected_get_configs):
        result: Config = get_config(line)

        if result:
            param, key = result

        msg: str
        msg = f"get_config returns wrong value: {get_config(line)} != {exp}"
        assert result == exp, msg

