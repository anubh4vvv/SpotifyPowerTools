import sys
from pathlib import Path

from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QFontDatabase, QIcon

from gui.main_window import MainWindow


def set_windows_app_id():
    """
    Forces Windows taskbar to treat this as its own app instead of python.exe.
    This helps the taskbar use the custom app icon.
    """

    if sys.platform != "win32":
        return

    try:
        import ctypes

        app_id = "SpotifyPowerTools.Desktop.App.1"

        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(
            app_id
        )

    except Exception:
        pass


def load_app_fonts():
    font_dir = Path(__file__).resolve().parent / "gui" / "resources" / "fonts"

    if not font_dir.exists():
        return

    for font_file in font_dir.glob("*.ttf"):
        QFontDatabase.addApplicationFont(str(font_file))

    for font_file in font_dir.glob("*.otf"):
        QFontDatabase.addApplicationFont(str(font_file))


def app_icon_path():
    base_dir = Path(__file__).resolve().parent

    candidates = [
        base_dir / "gui" / "resources" / "icons" / "app_icon.ico",
        base_dir / "gui" / "resources" / "icons" / "app_icon.png",
    ]

    for path in candidates:
        if path.exists():
            return path

    return None


def main():
    set_windows_app_id()

    app = QApplication(sys.argv)

    app.setApplicationName("Spotify Power Tools")
    app.setApplicationDisplayName("Spotify Power Tools")
    app.setOrganizationName("Spotify Power Tools")
    app.setQuitOnLastWindowClosed(False)

    load_app_fonts()

    icon_path = app_icon_path()

    if icon_path is not None:
        icon = QIcon(str(icon_path))

        app.setWindowIcon(icon)

    window = MainWindow()

    if icon_path is not None:
        window.setWindowIcon(
            QIcon(str(icon_path))
        )

    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()