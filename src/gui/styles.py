from gui.colors import (
    BACKGROUND,
    CARD,
    CARD_LIGHT,
    TEXT,
    TEXT_SECONDARY,
    TEXT_MUTED,
    BORDER,
    HOVER,
    ACCENT,
    ACCENT_HOVER,
    ACCENT_PRESSED,
    ON_ACCENT,
    SAGE,
    ROSE,
    LINE_STRONG,
)

from gui.fonts import (
    FONT_SANS_STACK,
    FONT_SERIF_STACK,
    FONT_MONO_STACK,
)


APP_STYLE = f"""
/* =========================================================
   Spotify Power Tools — Cinematic Moodboard UI
   Single source of truth stylesheet
   ========================================================= */

/* ---------- Root ---------- */

QMainWindow {{
    background: {BACKGROUND};
}}

QWidget#AppRoot {{
    background: qradialgradient(
        cx:0.16, cy:0.04,
        radius:1.25,
        fx:0.16, fy:0.04,
        stop:0 rgba(227,168,87,16),
        stop:0.30 {BACKGROUND},
        stop:1 {BACKGROUND}
    );
}}

QWidget {{
    background: transparent;
    color: {TEXT};
    font-family: {FONT_SANS_STACK};
    font-size: 11pt;
}}

QStackedWidget {{
    background: transparent;
}}

/* ---------- Sidebar ---------- */

QFrame#Sidebar {{
    background: #100d0a;
    border-right: 1px solid rgba(243,236,223,0.10);
}}

QLabel#SidebarTitle {{
    font-family: {FONT_SERIF_STACK};
    font-size: 22pt;
    font-weight: 500;
    color: {TEXT};
}}

QLabel#SidebarSubtitle {{
    color: {TEXT_MUTED};
    font-size: 9.5pt;
    font-weight: 600;
    letter-spacing: 3px;
}}

QLabel#SidebarVersion {{
    color: {TEXT_SECONDARY};
    font-size: 9.5pt;
    font-weight: 500;
}}

QPushButton#SidebarButton {{
    background: transparent;
    border: 1px solid transparent;
    border-radius: 9px;
    text-align: left;
    padding: 12px 14px;
    color: {TEXT_SECONDARY};
    font-size: 11pt;
    font-weight: 500;
}}

QPushButton#SidebarButton:hover {{
    background: rgba(243,236,223,0.04);
    border: 1px solid rgba(243,236,223,0.08);
    color: {TEXT};
}}

QPushButton#SidebarButton[active="true"] {{
    background: {CARD};
    color: {TEXT};
    border: 1px solid rgba(243,236,223,0.12);
    font-weight: 700;
}}

/* ---------- Generic Cards ---------- */

QFrame#Card {{
    background: {CARD};
    border: 1px solid rgba(243,236,223,0.08);
    border-radius: 10px;
}}

QFrame#Card:hover {{
    border: 1px solid rgba(243,236,223,0.14);
}}

QLabel#CardTitle {{
    font-family: {FONT_SERIF_STACK};
    color: {TEXT};
    font-size: 15pt;
    font-weight: 500;
}}

/* ---------- Dashboard ---------- */

QWidget#DashboardContent {{
    background: transparent;
}}

QFrame#DashboardHeader {{
    background: transparent;
}}

QLabel#DashboardGreeting {{
    font-family: {FONT_SERIF_STACK};
    font-size: 29pt;
    font-weight: 400;
    color: {TEXT};
}}

QLabel#DashboardMeta {{
    color: {TEXT_MUTED};
    font-size: 10.5pt;
    font-weight: 500;
}}

QLabel#ProfilePill {{
    background: {CARD};
    color: {TEXT_SECONDARY};
    border: 1px solid rgba(243,236,223,0.14);
    border-radius: 20px;
    padding: 8px 22px;
    font-size: 10.5pt;
    font-weight: 700;
}}

/* ---------- Dashboard Cards ---------- */

QFrame#NowPlayingCard,
QFrame#SmartShuffleCard,
QFrame#IdentityCard,
QFrame#StatsStrip {{
    background: {CARD};
    border: 1px solid rgba(243,236,223,0.09);
    border-radius: 10px;
}}

QFrame#NowPlayingCard QLabel#CardTitle,
QFrame#SmartShuffleCard QLabel#CardTitle {{
    color: {TEXT_MUTED};
    font-size: 10pt;
    font-weight: 800;
    letter-spacing: 4px;
}}

/* ---------- Now Playing ---------- */

QFrame#PolaroidFrame {{
    background: #f0e8da;
    border: none;
    border-radius: 3px;
}}

QLabel#AlbumCover {{
    background: #0e0c09;
    border: none;
}}

QLabel#PolaroidCaption {{
    color: #4b4034;
    font-family: {FONT_MONO_STACK};
    font-size: 9pt;
    font-weight: 500;
}}

QLabel#NowPlayingTitle {{
    color: {TEXT};
    font-family: {FONT_SERIF_STACK};
    font-size: 28pt;
    font-weight: 500;
}}

QLabel#NowPlayingArtist {{
    color: {TEXT};
    font-size: 14pt;
    font-weight: 500;
}}

QLabel#NowPlayingAlbum {{
    color: {TEXT_SECONDARY};
    font-size: 11.5pt;
    font-style: italic;
}}

QLabel#NowPlayingTime,
QLabel#NowPlayingMeta {{
    color: {TEXT_MUTED};
    font-size: 10pt;
}}

QLabel#RatingTitle {{
    color: {TEXT_SECONDARY};
    font-size: 10pt;
    font-weight: 700;
}}

QSlider#NowPlayingProgress::groove:horizontal {{
    height: 3px;
    background: rgba(243,236,223,0.10);
    border-radius: 2px;
}}

QSlider#NowPlayingProgress::sub-page:horizontal {{
    background: {ACCENT};
    border-radius: 2px;
}}

QSlider#NowPlayingProgress::add-page:horizontal {{
    background: rgba(243,236,223,0.08);
    border-radius: 2px;
}}

QSlider#NowPlayingProgress::handle:horizontal {{
    background: {TEXT};
    border: 2px solid {ACCENT};
    width: 13px;
    height: 13px;
    margin: -6px 0;
    border-radius: 7px;
}}

QPushButton#TransportSecondary {{
    background: transparent;
    color: {TEXT_SECONDARY};
    border: 1px solid rgba(243,236,223,0.16);
    border-radius: 18px;
    padding: 8px;
    font-size: 16pt;
    font-weight: 700;
}}

QPushButton#TransportSecondary:hover {{
    border: 1px solid {ACCENT};
    color: {TEXT};
}}

QPushButton#TransportPlay {{
    background: {ACCENT};
    color: {ON_ACCENT};
    border: none;
    border-radius: 20px;
    padding: 8px;
    font-size: 12pt;
    font-weight: 900;
}}

QPushButton#RatingButton {{
    background: #1a1611;
    color: {TEXT_SECONDARY};
    border: 1px solid rgba(243,236,223,0.12);
    border-radius: 10px;
    font-weight: 800;
}}

QPushButton#RatingButton:hover {{
    border: 1px solid {ACCENT};
    color: {TEXT};
}}

QPushButton#RatingClearButton {{
    background: transparent;
    color: {TEXT_SECONDARY};
    border: 1px solid rgba(243,236,223,0.10);
    border-radius: 9px;
    padding: 8px;
    font-size: 9.5pt;
}}

QPushButton#RatingClearButton:hover {{
    border: 1px solid {ACCENT};
    color: {TEXT};
}}

/* ---------- Smart Shuffle ---------- */

QLabel#SmartShuffleBadge {{
    background: rgba(147,166,138,32);
    color: {SAGE};
    border: 1px solid rgba(147,166,138,80);
    border-radius: 12px;
    padding: 5px 11px;
    font-size: 9.5pt;
    font-weight: 700;
}}

QLabel#ShuffleExplanation {{
    color: {TEXT_SECONDARY};
    font-size: 10.5pt;
}}

QFrame#QueuePreviewFrame {{
    background: #1a1611;
    border: 1px solid rgba(243,236,223,0.08);
    border-radius: 9px;
}}

QScrollArea#QueuePreviewScroll {{
    background: transparent;
    border: none;
}}

QWidget#QueuePreviewScrollContent {{
    background: transparent;
}}

QWidget#QueuePreviewRow {{
    background: transparent;
    border-bottom: 1px solid rgba(243,236,223,0.06);
}}

QLabel#QueuePreviewIndex {{
    color: {TEXT_MUTED};
    font-family: {FONT_SERIF_STACK};
    font-size: 11pt;
    font-weight: 500;
}}

QLabel#QueuePreviewSong {{
    color: {TEXT};
    font-family: {FONT_SERIF_STACK};
    font-size: 12pt;
    font-weight: 500;
}}

QLabel#QueuePreviewReason {{
    color: {TEXT_MUTED};
    font-size: 8.5pt;
    font-weight: 500;
}}

QLabel#QueuePreviewArtist {{
    color: {TEXT_SECONDARY};
    font-size: 9.5pt;
    font-weight: 500;
}}

QLabel#QueueEmptyText {{
    color: {TEXT_MUTED};
    font-size: 10pt;
    font-weight: 500;
}}

QPushButton#GhostButton {{
    background: transparent;
    color: {TEXT_SECONDARY};
    border: 1px solid rgba(243,236,223,0.10);
    border-radius: 7px;
    padding: 10px 14px;
    font-size: 10pt;
    font-weight: 500;
}}

QPushButton#GhostButton:hover {{
    border: 1px solid {ACCENT};
    color: {TEXT};
}}

QPushButton#AmberButton {{
    background: {ACCENT};
    color: {ON_ACCENT};
    border: none;
    border-radius: 7px;
    padding: 10px 14px;
    font-size: 10pt;
    font-weight: 800;
}}

QPushButton#AmberButton:hover {{
    background: {ACCENT_HOVER};
}}

QPushButton#AmberButton:pressed {{
    background: {ACCENT_PRESSED};
}}

QPushButton#AmberButton:disabled {{
    background: rgba(227,168,87,90);
    color: rgba(26,22,17,150);
}}

/* ---------- Stats Strip ---------- */

QFrame#StatsStrip {{
    background: {CARD};
    border: 1px solid rgba(243,236,223,0.09);
    border-radius: 10px;
}}

QFrame#StatStripItem {{
    background: transparent;
    border: none;
}}

QFrame#StatDivider {{
    background: rgba(243,236,223,0.10);
    border: none;
}}

QLabel#StatStripValue {{
    color: {TEXT};
    font-family: {FONT_SERIF_STACK};
    font-size: 31pt;
    font-weight: 500;
}}

QLabel#StatStripLabel {{
    color: {TEXT_MUTED};
    font-size: 9pt;
    font-weight: 800;
    letter-spacing: 3px;
}}

/* ---------- Identity ---------- */

QFrame#IdentityCard {{
    background: qlineargradient(
        x1:0, y1:0,
        x2:1, y2:1,
        stop:0 {CARD},
        stop:1 #1a1611
    );
    border: 1px solid rgba(243,236,223,0.09);
    border-radius: 10px;
}}

QLabel#IdentityEyebrow {{
    color: {TEXT_MUTED};
    font-size: 9.5pt;
    font-weight: 800;
    letter-spacing: 4px;
}}

QLabel#IdentityName {{
    color: {ACCENT};
    font-family: {FONT_SERIF_STACK};
    font-size: 39pt;
    font-style: italic;
    font-weight: 500;
}}

QLabel#IdentitySubtitle {{
    color: {TEXT_SECONDARY};
    font-size: 11.5pt;
}}

QLabel#BadgeStickerSage {{
    background: rgba(147,166,138,32);
    color: {SAGE};
    border: 1px dashed rgba(147,166,138,120);
    border-radius: 6px;
    padding: 8px 13px;
    font-size: 9.5pt;
    font-weight: 700;
}}

QLabel#BadgeStickerRose {{
    background: rgba(201,138,125,32);
    color: {ROSE};
    border: 1px dashed rgba(201,138,125,120);
    border-radius: 6px;
    padding: 8px 13px;
    font-size: 9.5pt;
    font-weight: 700;
}}

QLabel#BadgeStickerAmber {{
    background: rgba(227,168,87,32);
    color: {ACCENT};
    border: 1px dashed rgba(227,168,87,120);
    border-radius: 6px;
    padding: 8px 13px;
    font-size: 9.5pt;
    font-weight: 700;
}}

QFrame#AuraRing {{
    background: rgba(227,168,87,12);
    border: 3px solid {ACCENT};
    border-radius: 74px;
}}

QLabel#AuraRingNumber {{
    color: {ACCENT};
    font-family: {FONT_SERIF_STACK};
    font-size: 40pt;
    font-weight: 500;
}}

QLabel#AuraRingLabel {{
    color: {TEXT_MUTED};
    font-size: 8.5pt;
    font-weight: 800;
    letter-spacing: 2px;
}}

/* ---------- Scrollbars ---------- */

QScrollBar:vertical {{
    background: rgba(243,236,223,0.04);
    width: 8px;
    margin: 8px 0px 8px 2px;
    border-radius: 4px;
}}

QScrollBar::handle:vertical {{
    background: rgba(227,168,87,0.35);
    border-radius: 4px;
    min-height: 30px;
}}

QScrollBar::handle:vertical:hover {{
    background: rgba(227,168,87,0.65);
}}

QScrollBar::add-line:vertical,
QScrollBar::sub-line:vertical {{
    height: 0px;
    background: none;
}}

QScrollBar::add-page:vertical,
QScrollBar::sub-page:vertical {{
    background: none;
}}

QScrollBar:horizontal {{
    background: rgba(243,236,223,0.04);
    height: 8px;
    margin: 2px 8px 0px 8px;
    border-radius: 4px;
}}

QScrollBar::handle:horizontal {{
    background: rgba(227,168,87,0.45);
    border-radius: 4px;
    min-width: 42px;
}}

QScrollBar::handle:horizontal:hover {{
    background: rgba(227,168,87,0.70);
}}

QScrollBar::add-line:horizontal,
QScrollBar::sub-line:horizontal {{
    width: 0px;
    background: none;
}}

QScrollBar::add-page:horizontal,
QScrollBar::sub-page:horizontal {{
    background: none;
}}

/* ---------- Other Pages Fallback ---------- */

QLineEdit,
QComboBox {{
    background: {CARD};
    color: {TEXT};
    border: 1px solid {BORDER};
    border-radius: 7px;
    padding: 9px 12px;
}}

QLineEdit:focus,
QComboBox:focus {{
    border: 1px solid {ACCENT};
}}

QToolTip {{
    background: {CARD};
    color: {TEXT};
    border: 1px solid {LINE_STRONG};
    border-radius: 6px;
    padding: 8px;
}}
"""