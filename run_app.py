import streamlit.web.cli as stcli
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