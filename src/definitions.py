import sys
from pathlib import Path

SRC_DIR = Path(__file__).parent

DEBUG_MODE = sys.gettrace() is not None
is_PyCharm = False
