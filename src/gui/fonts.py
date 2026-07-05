from pathlib import Path

from PySide6.QtGui import QFontDatabase

TITLE = 30
HEADER = 22
SUBHEADER = 18
BODY = 13
SMALL = 11

# Display/personality font — used for hero titles, aura score, playlist
# identity name, stat numbers. Sans is used for everything else (nav,
# buttons, body copy, labels).
FONT_SERIF = "Fraunces"
FONT_SANS = "Inter"

# Fallback chain used everywhere in styles.py so the app still looks
# reasonable if the bundled fonts fail to load for any reason.
FONT_SERIF_STACK = f"'{FONT_SERIF}', Georgia, serif"
FONT_SANS_STACK = f"'{FONT_SANS}', 'Segoe UI Variable', 'Segoe UI', Arial, sans-serif"

FONTS_DIR = Path(__file__).resolve().parent.parent / "assets" / "fonts"

# Add/remove filenames here to match whatever weights you actually download
# from Google Fonts (fonts.google.com/specimen/Fraunces and /specimen/Inter).
# Static .ttf files, not the variable-font versions, are the safe choice —
# QFontDatabase.addApplicationFont is more reliable with statics.
FONT_FILES = [
    "Fraunces-Regular.ttf",
    "Fraunces-Medium.ttf",
    "Fraunces-Italic.ttf",
    "Inter-Regular.ttf",
    "Inter-Medium.ttf",
    "Inter-SemiBold.ttf",
]


def load_app_fonts():
    """
    Registers the bundled font files with Qt's font database so family
    names like 'Fraunces' and 'Inter' resolve correctly in styles.py QSS.

    Call this once, after the QApplication instance is created and before
    MainWindow is constructed — e.g. in your entry point:

        app = QApplication(sys.argv)
        load_app_fonts()
        window = MainWindow()
        window.show()

    Calling it before QApplication exists will silently fail to register
    anything, since QFontDatabase needs an active application instance.
    """
    if not FONTS_DIR.exists():
        print(f"[fonts] fonts folder not found at {FONTS_DIR} — "
              f"create it and add the .ttf files listed in FONT_FILES")
        return

    missing = []

    for filename in FONT_FILES:
        path = FONTS_DIR / filename

        if not path.exists():
            missing.append(filename)
            continue

        font_id = QFontDatabase.addApplicationFont(str(path))

        if font_id == -1:
            print(f"[fonts] failed to load font file: {filename}")

    if missing:
        print(f"[fonts] missing font files (place in {FONTS_DIR}): {missing}")