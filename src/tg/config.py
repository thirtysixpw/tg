"""
Every parameter (except for CONFIG_FILE) can be
overwritten by external config file
"""

import os
import platform
import runpy
from pathlib import Path
from typing import Dict, Optional

_os_name = platform.system()
_darwin = "Darwin"
_linux = "Linux"


CONFIG_DIR = Path("~/.config/tg/").expanduser()
CONFIG_FILE = CONFIG_DIR / "conf.py"
FILES_DIR = Path("~/.cache/tg/").expanduser()
MAILCAP_FILE: Optional[str] = None

LOG_LEVEL = "INFO"
LOG_PATH = Path("~/.local/share/tg/").expanduser()

API_ID = "559815"
API_HASH = "fd121358f59d764c57c55871aa0807ca"

PHONE = None
ENC_KEY = ""

TDLIB_PATH = None
TDLIB_VERBOSITY = 0

MAX_DOWNLOAD_SIZE = "10MB"

# TODO: check platform
NOTIFY_CMD = "/usr/local/bin/terminal-notifier -title {title} -subtitle {subtitle} -message {msg} -appIcon {icon_path}"

VIEW_TEXT_CMD = "less"
FZF = "fzf"

if _os_name == _linux:
    # for more info see https://trac.ffmpeg.org/wiki/Capture/ALSA
    VOICE_RECORD_CMD = "ffmpeg -y -f alsa -i hw:0 -c:a libopus -b:a 32k {file_path}"
else:
    VOICE_RECORD_CMD = "ffmpeg -y -f avfoundation -i ':0' -c:a libopus -b:a 32k {file_path}"

# TODO: use mailcap instead of editor
LONG_MSG_CMD = "vim + -c 'startinsert' {file_path}"
EDITOR = os.environ.get("EDITOR", "vi")

DEFAULT_OPEN = "xdg-open {file_path}" if _os_name == _linux else "open {file_path}"

if _os_name == _linux:
    COPY_CMD = "wl-copy" if os.environ.get("WAYLAND_DISPLAY") else "xclip -selection c"
else:
    COPY_CMD = "pbcopy"

CHAT_FLAGS: Dict[str, str] = {}

MSG_FLAGS: Dict[str, str] = {}

ICON_PATH = Path(__file__).parent / "resources" / "tg.png"

URL_VIEW = "urlview"

USERS_COLORS = tuple(range(2, 16))

KEEP_MEDIA = 7

FILE_PICKER_CMD = "ranger --choosefile={file_path}"

DOWNLOAD_DIR = Path("~/Downloads/").expanduser()

if CONFIG_FILE.is_file():
    config_params = runpy.run_path(CONFIG_FILE)  # type: ignore
    for param, value in config_params.items():
        if param.isupper():
            globals()[param] = value
else:
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)

    if not PHONE:
        print("Enter your phone number in international format (including country code)")
        PHONE = input("phone> ")
        if not PHONE.startswith("+"):
            PHONE = "+" + PHONE

    with open(CONFIG_FILE, "w") as f:
        f.write(f"PHONE = '{PHONE}'\n")
