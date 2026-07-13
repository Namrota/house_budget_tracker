from cx_Freeze import setup, Executable
import sys
import os

# Get venv paths only to avoid Anaconda/OpenSSL conflicts
venv_dir = os.path.dirname(sys.executable)
venv_site_packages = os.path.join(venv_dir, "Lib", "site-packages")

build_exe_options = {
    "packages": [
        "streamlit",
        "streamlit.web.cli",    # Critical: the CLI module
        "pandas",
        "numpy",
        "validators",
        "toml",
        "uvicorn"
    ],
    "excludes": ["tkinter", "matplotlib", "pytest", "unittest"],
    "includes": [
        # Uvicorn hidden imports
        "uvicorn.protocols.http.auto",
        "uvicorn.protocols.websockets.auto",
        # PyArrow hidden imports
        "pyarrow.vendored.version",
        "pyarrow._hdfs",
        "pyarrow._s3fs",
        # Pandas/Arrow integration
        "pandas.core.arrays.string_arrow",
    ],
    "include_files": [
        "main.py",              # Main Streamlit app
        "data_handling.py",
        "widgets.py",
        "expenses.csv",
    ],
    "include_msvcr": True,
    "bin_includes": [],
    "bin_path_includes": [venv_dir, venv_site_packages],
    "bin_path_excludes": [
        os.path.expanduser(r"~\anaconda3"),
        os.path.expanduser(r"~\anaconda3\Library\bin"),
        os.path.expanduser(r"~\anaconda3\DLLs"),
        os.path.expanduser(r"~\anaconda3\Scripts"),
    ],
}

executables = [
    Executable(
        "launcher.py",          # Entry point
        base="Console",
        target_name="BudgetTracker.exe",
    )
]

setup(
    name="House Budget Tracker",
    version="1.0",
    options={"build_exe": build_exe_options},
    executables=executables,
)
