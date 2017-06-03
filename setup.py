import sys
from cx_Freeze import setup, Executable

import os.path
PYTHON_INSTALL_DIR = os.path.dirname(os.path.dirname(os.__file__))
os.environ['TCL_LIBRARY'] = os.path.join(PYTHON_INSTALL_DIR, 'tcl', 'tcl8.6')
os.environ['TK_LIBRARY'] = os.path.join(PYTHON_INSTALL_DIR, 'tcl', 'tk8.6')

# replaces commandline arg 'build'
sys.argv.append("build")  
# change the filename to your program file --->
filename = "a3.py"
base = None
if sys.platform == "win32":
    base = "Win32GUI"
    
includes      = []
include_files = [r"C:\Users\i\AppData\Local\Programs\Python\Python35-32\DLLs\tcl86t.dll", \
                 r"C:\Users\i\AppData\Local\Programs\Python\Python35-32\DLLs\tk86t.dll"]

setup(
    name = "ye",
    version = "1.0",
    options = {"build_exe": {"includes": includes, "include_files": include_files}},
    executables = [Executable("a3.py", base=base)]
)
