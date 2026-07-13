'''
This python script will be the ebtry point for .exe file. It will launch the streamlit application.

'''

import streamlit
import streamlit.web.cli as stcli
import pandas          # Force cx_Freeze to include
import os, sys

def resolve_path(path):
    if getattr(sys, 'frozen', False):
        # cx_Freeze puts everything in same dir as .exe
        base_path = os.path.dirname(sys.executable)
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