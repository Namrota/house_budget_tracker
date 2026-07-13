'''
This python script will be the entry point for .exe file. It will launch the streamlit application.

'''

import streamlit
import streamlit.web.cli as stcli
import pandas          # Force cx_Freeze to include
import os, sys
from datetime import datetime
from data_handling import load_data
from widgets import render_sidebar

def resolve_path(path):
    if getattr(sys, 'frozen', False):
        # PyInstaller extracts to sys._MEIPASS when running onefile
        base_path = sys._MEIPASS
    else:
        base_path = os.getcwd()
    return os.path.abspath(os.path.join(base_path, path))

if __name__ == "__main__":
    sys.argv = [
        "streamlit",
        "run",
        resolve_path("main.py"),          # Main app file
        "--global.developmentMode=false",  # Critical for .exe
    ]
    sys.exit(stcli.main())