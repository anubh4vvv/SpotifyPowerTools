from gui.colors import (
    BACKGROUND,
    CARD,
    CARD_LIGHT,
    TEXT,
    TEXT_SECONDARY,
    TEXT_MUTED,
    BORDER,
    HOVER,
    SUCCESS,
    WARNING,
    ERROR,
    ACCENT,
    ACCENT_HOVER,
    ACCENT_PRESSED,
    ON_ACCENT,
    SAGE,
    ROSE,
    LINE_STRONG,
)

from gui.fonts import FONT_SANS_STACK, FONT_SERIF_STACK

APP_STYLE = f"""
/* =========================================================
   Spotify Power Tools — Moodboard UI
   Cinematic, matte, film-grain-adjacent
   ========================================================= */

QMainWindow{{
    background:{BACKGROUND};
}}

QWidget#AppRoot{{
    background:qradialgradient(
        cx:0.12, cy:0.05,
        radius:1.3,
        fx:0.12, fy:0.05,
        stop:0 rgba(227,168,87,10),
        stop:0.35 {BACKGROUND},
        stop:1 {BACKGROUND}
    );
}}

QWidget{{
    background:transparent;
    color:{TEXT};
    font-family:{FONT_SANS_STACK};
    font-size:11pt;
}}

QStackedWidget{{
    background:transparent;
}}

/* ---------- Header ---------- */

QFrame#Header{{
    background:{CARD};
    border-bottom:1px solid {LINE_STRONG};
}}

QLabel#HeaderLogo{{
    background:{ACCENT};
    color:{ON_ACCENT};
    border-radius:18px;
    font-family:{FONT_SERIF_STACK};
    font-size:20pt;
    font-weight:600;
}}

QLabel#HeaderTitle{{
    font-family:{FONT_SERIF_STACK};
    font-size:22pt;
    font-weight:500;
    color:{TEXT};
}}

QLabel#HeaderSubtitle{{
    font-size:10pt;
    color:{TEXT_MUTED};
    font-weight:500;
}}

QLabel#HeaderStatus{{
    color:{SAGE};
    background:rgba(147,166,138,32);
    border:1px solid rgba(147,166,138,80);
    border-radius:15px;
    padding:7px 13px;
    font-size:10pt;
    font-weight:600;
}}

QLabel#HeaderStatusError{{
    color:{ROSE};
    background:rgba(201,138,125,32);
    border:1px solid rgba(201,138,125,80);
    border-radius:15px;
    padding:7px 13px;
    font-size:10pt;
    font-weight:600;
}}

/* ---------- Sidebar ---------- */

QFrame#Sidebar{{
    background:{BACKGROUND};
    border-right:1px solid {BORDER};
}}

QLabel#SidebarTitle{{
    font-family:{FONT_SERIF_STACK};
    font-size:19pt;
    font-weight:500;
    color:{TEXT};
}}

QLabel#SidebarSubtitle{{
    color:{TEXT_MUTED};
    font-size:9.5pt;
    font-weight:500;
    margin-bottom:10px;
}}

QLabel#SidebarVersion{{
    color:{TEXT_MUTED};
    font-size:9pt;
    font-weight:500;
}}

/* ---------- Sidebar Buttons ---------- */

QPushButton#SidebarButton{{
    background:transparent;
    border:1px solid transparent;
    border-radius:8px;
    text-align:left;
    padding:11px 14px;
    font-size:10.5pt;
    font-weight:500;
    color:{TEXT_SECONDARY};
}}

QPushButton#SidebarButton:hover{{
    background:{CARD};
    border:1px solid {BORDER};
    color:{TEXT};
}}

QPushButton#SidebarButton[active="true"]{{
    background:{CARD};
    color:{TEXT};
    border:1px solid {LINE_STRONG};
    border-radius:8px;
    font-size:10.5pt;
    font-weight:600;
}}

/* ---------- App Status Bar ---------- */

QFrame#AppStatusBar{{
    background:{CARD};
    border-top:1px solid {BORDER};
}}

QLabel#StatusDot{{
    color:{SAGE};
    font-size:12pt;
    font-weight:600;
}}

QLabel#StatusMessage{{
    color:{TEXT_SECONDARY};
    font-size:9.5pt;
    font-weight:500;
}}

/* ---------- General Cards ---------- */

QFrame#Card{{
    background:{CARD};
    border:1px solid {BORDER};
    border-radius:10px;
}}

QFrame#Card:hover{{
    border:1px solid {LINE_STRONG};
}}

QLabel#CardTitle{{
    font-family:{FONT_SERIF_STACK};
    font-size:15pt;
    font-weight:500;
    color:{TEXT};
}}

QLabel#SectionTitle{{
    font-family:{FONT_SERIF_STACK};
    font-size:21pt;
    font-weight:500;
    color:{TEXT};
}}

QLabel#SectionSubtitle{{
    color:{TEXT_MUTED};
    font-size:10.5pt;
    font-weight:500;
}}

/* ---------- Buttons ---------- */

QPushButton{{
    background:{ACCENT};
    color:{ON_ACCENT};
    border:none;
    border-radius:7px;
    padding:11px 17px;
    font-size:10.5pt;
    font-weight:600;
}}

QPushButton:hover{{
    background:{ACCENT_HOVER};
}}

QPushButton:pressed{{
    background:{ACCENT_PRESSED};
}}

QPushButton:disabled{{
    background:{CARD_LIGHT};
    color:{TEXT_MUTED};
}}

QPushButton#SecondaryButton{{
    background:transparent;
    border:1px solid {BORDER};
    color:{TEXT_SECONDARY};
    border-radius:7px;
    padding:10px 15px;
    font-size:10pt;
    font-weight:500;
}}

QPushButton#SecondaryButton:hover{{
    background:{CARD_LIGHT};
    border:1px solid {LINE_STRONG};
    color:{TEXT};
}}

QPushButton#SecondaryButton:pressed{{
    background:{HOVER};
}}

/* ---------- Inputs ---------- */

QLineEdit{{
    background:{CARD};
    color:{TEXT};
    border:1px solid {BORDER};
    border-radius:7px;
    padding:10px 14px;
    selection-background-color:{ACCENT};
    selection-color:{ON_ACCENT};
}}

QLineEdit:hover{{
    border:1px solid {LINE_STRONG};
}}

QLineEdit:focus{{
    border:1px solid {ACCENT};
}}

/* ---------- Combo Boxes ---------- */

QComboBox{{
    background:{CARD};
    color:{TEXT};
    border:1px solid {BORDER};
    border-radius:7px;
    padding:9px 12px;
    font-weight:500;
}}

QComboBox:hover{{
    border:1px solid {LINE_STRONG};
}}

QComboBox:focus{{
    border:1px solid {ACCENT};
}}

QComboBox::drop-down{{
    border:none;
    width:30px;
}}

QComboBox::down-arrow{{
    image:none;
    border-left:5px solid transparent;
    border-right:5px solid transparent;
    border-top:6px solid {TEXT_SECONDARY};
    margin-right:8px;
}}

QAbstractItemView{{
    background:{CARD};
    color:{TEXT};
    border:1px solid {LINE_STRONG};
    selection-background-color:{ACCENT};
    selection-color:{ON_ACCENT};
    outline:none;
}}

/* ---------- Sliders ---------- */

QSlider::groove:horizontal{{
    height:3px;
    background:{BORDER};
    border-radius:2px;
}}

QSlider::sub-page:horizontal{{
    background:{ACCENT};
    border-radius:2px;
}}

QSlider::add-page:horizontal{{
    background:{BORDER};
    border-radius:2px;
}}

QSlider::handle:horizontal{{
    background:{TEXT};
    border:2px solid {ACCENT};
    width:14px;
    height:14px;
    margin:-6px 0;
    border-radius:7px;
}}

QSlider::handle:horizontal:hover{{
    background:{ACCENT_HOVER};
    border:2px solid {ACCENT_HOVER};
}}

/* ---------- Progress Bar ---------- */

QProgressBar{{
    background:{BORDER};
    border:none;
    border-radius:4px;
}}

QProgressBar::chunk{{
    background:{ACCENT};
    border-radius:4px;
}}

/* ---------- Statistic Tiles ---------- */

QFrame#StatTile{{
    background:{CARD};
    border:1px solid {BORDER};
    border-radius:10px;
}}

QFrame#StatTile:hover{{
    border:1px solid {LINE_STRONG};
}}

QLabel#StatTitle{{
    color:{TEXT_MUTED};
    font-size:9.5pt;
    font-weight:600;
}}

QLabel#StatValue{{
    color:{TEXT};
    font-family:{FONT_SERIF_STACK};
    font-size:22pt;
    font-weight:500;
}}

/* ---------- Analytics Hero ---------- */

QFrame#AnalyticsHeroCard{{
    background:qlineargradient(
        x1:0, y1:0,
        x2:1, y2:1,
        stop:0 {CARD},
        stop:1 {BACKGROUND}
    );
    border:1px solid {BORDER};
    border-radius:12px;
}}

QLabel#HeroEyebrow{{
    color:{TEXT_MUTED};
    font-size:9.5pt;
    font-weight:600;
}}

QLabel#HeroEmoji{{
    font-size:36pt;
}}

QLabel#HeroPersonality{{
    color:{ACCENT};
    font-family:{FONT_SERIF_STACK};
    font-style:italic;
    font-size:30pt;
    font-weight:500;
}}

QLabel#HeroSubtitle{{
    color:{TEXT_SECONDARY};
    font-size:11pt;
    font-weight:500;
}}

QLabel#HeroRecommended{{
    color:{ON_ACCENT};
    background:{ACCENT};
    border-radius:7px;
    padding:10px 14px;
    font-size:10pt;
    font-weight:600;
}}

QLabel#AuraTitle{{
    color:{TEXT_MUTED};
    font-size:9.5pt;
    font-weight:600;
}}

QLabel#AuraNumber{{
    color:{TEXT};
    font-family:{FONT_SERIF_STACK};
    font-size:56pt;
    font-weight:500;
}}

QLabel#AuraStatus{{
    color:{TEXT_SECONDARY};
    font-size:12pt;
    font-weight:500;
}}

QProgressBar#AuraProgress{{
    background:{BORDER};
    border:none;
    border-radius:4px;
}}

QProgressBar#AuraProgress::chunk{{
    background:{ACCENT};
    border-radius:4px;
}}

QFrame#GlowMetric{{
    background:{CARD_LIGHT};
    border:1px solid {BORDER};
    border-radius:10px;
}}

QLabel#GlowMetricTitle{{
    color:{TEXT_MUTED};
    font-size:9.5pt;
    font-weight:600;
}}

QLabel#GlowMetricValue{{
    color:{TEXT};
    font-family:{FONT_SERIF_STACK};
    font-size:18pt;
    font-weight:500;
}}

QProgressBar#GlowMetricProgress{{
    background:{BORDER};
    border:none;
    border-radius:3px;
}}

QProgressBar#GlowMetricProgress::chunk{{
    background:{SAGE};
    border-radius:3px;
}}

/* ---------- Wrapped Cards ---------- */

QFrame#WrappedStatCard{{
    background:{CARD};
    border:1px solid {BORDER};
    border-radius:10px;
}}

QFrame#WrappedStatCard:hover{{
    border:1px solid {LINE_STRONG};
}}

QLabel#WrappedEmoji{{
    font-size:28pt;
}}

QLabel#WrappedTitle{{
    color:{TEXT_MUTED};
    font-size:9.5pt;
    font-weight:600;
}}

QLabel#WrappedValue{{
    color:{TEXT};
    font-family:{FONT_SERIF_STACK};
    font-size:18pt;
    font-weight:500;
}}

QLabel#WrappedSubtitle{{
    color:{TEXT_SECONDARY};
    font-size:9.5pt;
    font-weight:500;
}}

/* ---------- Badge Cloud ---------- */

QLabel#BadgePill{{
    background:rgba(227,168,87,26);
    border:1px dashed rgba(227,168,87,110);
    border-radius:5px;
    padding:8px 12px;
    color:{ACCENT};
    font-size:9.5pt;
    font-weight:600;
}}

QLabel#BadgePill:hover{{
    border:1px dashed {ACCENT};
    background:rgba(227,168,87,40);
}}

QLabel#BadgeEmpty{{
    color:{TEXT_MUTED};
    font-size:10.5pt;
    font-weight:500;
}}

/* ---------- Queue Items ---------- */

QFrame#QueueItem{{
    background:{CARD};
    border-radius:8px;
    border:1px solid {BORDER};
}}

QFrame#QueueItem:hover{{
    border:1px solid {LINE_STRONG};
    background:{CARD_LIGHT};
}}

QLabel#QueueSong{{
    color:{TEXT};
    font-size:11pt;
    font-weight:600;
}}

QLabel#QueueArtist{{
    color:{TEXT_SECONDARY};
    font-size:9.5pt;
}}

QLabel#QueueDuration{{
    color:{TEXT_MUTED};
    font-size:9.5pt;
}}

/* ---------- Search Results ---------- */

QWidget#SearchResultItem{{
    background:{CARD};
    border:1px solid {BORDER};
    border-radius:8px;
}}

QWidget#SearchResultItem:hover{{
    background:{CARD_LIGHT};
    border:1px solid {LINE_STRONG};
}}

/* ---------- Dividers ---------- */

QFrame#Divider{{
    background:{BORDER};
    max-height:1px;
    min-height:1px;
    border:none;
}}

/* ---------- Scroll Areas ---------- */

QScrollArea{{
    border:none;
    background:transparent;
}}

QScrollBar:vertical{{
    background:{BACKGROUND};
    width:10px;
    margin:4px 2px 4px 2px;
    border-radius:5px;
}}

QScrollBar::handle:vertical{{
    background:{BORDER};
    border-radius:5px;
    min-height:36px;
}}

QScrollBar::handle:vertical:hover{{
    background:{LINE_STRONG};
}}

QScrollBar::add-line:vertical,
QScrollBar::sub-line:vertical{{
    height:0px;
    background:none;
}}

QScrollBar::add-page:vertical,
QScrollBar::sub-page:vertical{{
    background:none;
}}

QScrollBar:horizontal{{
    height:0px;
    background:transparent;
}}

/* ---------- Tooltips ---------- */

QToolTip{{
    background:{CARD};
    color:{TEXT};
    border:1px solid {LINE_STRONG};
    border-radius:6px;
    padding:8px;
}}
/* ---------- Dashboard Mockup Header ---------- */

QFrame#DashboardHeader {{
    background: transparent;
}}

QWidget#DashboardContent {{
    background: transparent;
}}

QLabel#DashboardGreeting {{
    font-family: {FONT_SERIF_STACK};
    font-size: 26pt;
    font-weight: 400;
    color: #f3ecdf;
}}

QLabel#DashboardMeta {{
    color: #8f8574;
    font-size: 10.5pt;
    font-weight: 500;
}}

QLabel#ProfilePill {{
    background: #221c16;
    color: #c9bfae;
    border: 1px solid rgba(243,236,223,0.14);
    border-radius: 18px;
    padding: 9px 20px;
    font-size: 10.5pt;
    font-weight: 600;
}}

/* ---------- Playlist Identity Card ---------- */

QLabel#IdentityEyebrow {{
    color: #8f8574;
    font-size: 9.5pt;
    font-weight: 700;
    letter-spacing: 2px;
}}

QLabel#IdentityName {{
    color: #e3a857;
    font-family: {FONT_SERIF_STACK};
    font-size: 38pt;
    font-style: italic;
    font-weight: 500;
}}

QLabel#IdentitySubtitle {{
    color: #c9bfae;
    font-size: 12pt;
}}

QLabel#BadgeStickerSage {{
    background: rgba(147,166,138,28);
    color: #93a68a;
    border: 1px dashed rgba(147,166,138,120);
    border-radius: 6px;
    padding: 9px 13px;
    font-size: 10pt;
    font-weight: 600;
}}

QLabel#BadgeStickerRose {{
    background: rgba(201,138,125,28);
    color: #c98a7d;
    border: 1px dashed rgba(201,138,125,120);
    border-radius: 6px;
    padding: 9px 13px;
    font-size: 10pt;
    font-weight: 600;
}}

QLabel#BadgeStickerAmber {{
    background: rgba(227,168,87,28);
    color: #e3a857;
    border: 1px dashed rgba(227,168,87,120);
    border-radius: 6px;
    padding: 9px 13px;
    font-size: 10pt;
    font-weight: 600;
}}

QFrame#AuraRing {{
    background: rgba(227,168,87,12);
    border: 3px solid #e3a857;
    border-radius: 75px;
}}

QLabel#AuraRingNumber {{
    color: #e3a857;
    font-family: {FONT_SERIF_STACK};
    font-size: 42pt;
    font-weight: 500;
}}

QLabel#AuraRingLabel {{
    color: #8f8574;
    font-size: 8.5pt;
    font-weight: 700;
    letter-spacing: 2px;
}}
/* ---------- Dashboard Mockup Layout ---------- */

QWidget#DashboardContent {{
    background: transparent;
}}

QFrame#DashboardHeader {{
    background: transparent;
}}

QLabel#DashboardGreeting {{
    font-family: {FONT_SERIF_STACK};
    font-size: 25pt;
    font-weight: 400;
    color: #f3ecdf;
}}

QLabel#DashboardMeta {{
    color: #8f8574;
    font-size: 10.5pt;
    font-weight: 500;
}}

QLabel#ProfilePill {{
    background: #221c16;
    color: #c9bfae;
    border: 1px solid rgba(243,236,223,0.14);
    border-radius: 18px;
    padding: 8px 20px;
    font-size: 10.5pt;
    font-weight: 600;
}}

/* ---------- Smart Shuffle Mockup Card ---------- */

QLabel#SmartShuffleBadge {{
    background: rgba(147,166,138,32);
    color: #93a68a;
    border: 1px solid rgba(147,166,138,80);
    border-radius: 12px;
    padding: 5px 10px;
    font-size: 9.5pt;
    font-weight: 600;
}}

QLabel#ShuffleExplanation {{
    color: #c9bfae;
    font-size: 10.5pt;
    line-height: 145%;
}}

QLabel#ShuffleControlLabel {{
    color: #8f8574;
    font-size: 9pt;
    font-weight: 700;
    text-transform: uppercase;
}}

QComboBox#ShuffleMiniControl {{
    background: #1a1611;
    color: #f3ecdf;
    border: 1px solid rgba(243,236,223,0.08);
    border-radius: 7px;
    padding: 7px 10px;
    font-size: 10pt;
    font-weight: 500;
}}

QFrame#QueuePreviewFrame {{
    background: #1a1611;
    border: 1px solid rgba(243,236,223,0.08);
    border-radius: 9px;
}}

QWidget#QueuePreviewRow {{
    background: transparent;
    border-bottom: 1px solid rgba(243,236,223,0.06);
}}

QLabel#QueuePreviewIndex {{
    color: #8f8574;
    font-family: {FONT_SERIF_STACK};
    font-size: 11pt;
    font-weight: 500;
}}

QLabel#QueuePreviewSong {{
    color: #f3ecdf;
    font-family: {FONT_SERIF_STACK};
    font-size: 11.5pt;
    font-weight: 500;
}}

QLabel#QueuePreviewReason {{
    color: #8f8574;
    font-size: 8.5pt;
    font-weight: 500;
}}

QLabel#QueuePreviewArtist {{
    color: #c9bfae;
    font-size: 9.5pt;
    font-weight: 500;
}}

QLabel#QueueEmptyText {{
    color: #8f8574;
    font-size: 10pt;
    font-weight: 500;
}}

/* ---------- Playlist Identity Mockup Card ---------- */

QFrame#IdentityCard {{
    background: qlineargradient(
        x1:0, y1:0,
        x2:1, y2:1,
        stop:0 #221c16,
        stop:1 #1a1611
    );
    border: 1px solid rgba(243,236,223,0.08);
    border-radius: 10px;
}}

QLabel#IdentityEyebrow {{
    color: #8f8574;
    font-size: 9.5pt;
    font-weight: 700;
    letter-spacing: 2px;
}}

QLabel#IdentityName {{
    color: #e3a857;
    font-family: {FONT_SERIF_STACK};
    font-size: 36pt;
    font-style: italic;
    font-weight: 500;
}}

QLabel#IdentitySubtitle {{
    color: #c9bfae;
    font-size: 11.5pt;
}}

QLabel#BadgeStickerSage {{
    background: rgba(147,166,138,28);
    color: #93a68a;
    border: 1px dashed rgba(147,166,138,120);
    border-radius: 6px;
    padding: 8px 12px;
    font-size: 9.5pt;
    font-weight: 600;
}}

QLabel#BadgeStickerRose {{
    background: rgba(201,138,125,28);
    color: #c98a7d;
    border: 1px dashed rgba(201,138,125,120);
    border-radius: 6px;
    padding: 8px 12px;
    font-size: 9.5pt;
    font-weight: 600;
}}

QLabel#BadgeStickerAmber {{
    background: rgba(227,168,87,28);
    color: #e3a857;
    border: 1px dashed rgba(227,168,87,120);
    border-radius: 6px;
    padding: 8px 12px;
    font-size: 9.5pt;
    font-weight: 600;
}}

QFrame#AuraRing {{
    background: rgba(227,168,87,12);
    border: 3px solid #e3a857;
    border-radius: 74px;
}}

QLabel#AuraRingNumber {{
    color: #e3a857;
    font-family: {FONT_SERIF_STACK};
    font-size: 38pt;
    font-weight: 500;
}}

QLabel#AuraRingLabel {{
    color: #8f8574;
    font-size: 8.5pt;
    font-weight: 700;
    letter-spacing: 2px;
}}
"""