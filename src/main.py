import flet as ft
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent))
from ui.app_ui import main


if __name__ == "__main__":
    ft.run(main)
