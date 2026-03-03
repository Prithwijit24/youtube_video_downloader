""" import streamlit.web.cli as stcli
import sys
import os

if __name__ == "__main__":
    sys.argv = [
        "streamlit",
        "run",
        "app.py",
        "--global.developmentMode=false",
        "--server.headless=true",
        "--browser.gatherUsageStats=false"
    ]
    sys.exit(stcli.main())

 """
import sys
import os
import streamlit.web.cli as stcli

def get_app_path():
    if hasattr(sys, "_MEIPASS"):
        # Running inside PyInstaller bundle
        return os.path.join(sys._MEIPASS, "app.py")
    else:
        # Running normally
        return os.path.join(os.path.dirname(__file__), "app.py")

if __name__ == "__main__":
    app_path = get_app_path()
    # sys.argv = ["streamlit", "run", app_path]
    sys.argv = [
        "streamlit",
        "run",
        app_path,
        "--global.developmentMode=false",
        "--server.headless=true",
        "--browser.gatherUsageStats=false"
        ]
    sys.exit(stcli.main())
