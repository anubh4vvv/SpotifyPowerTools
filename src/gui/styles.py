APP_STYLE = """
/* =========================================================
   Spotify Power Tools - Global Theme
   ========================================================= */

QMainWindow{
    background:#000000;
}

QWidget{
    background:transparent;
    color:#F5F5F5;
   font-family:'Segoe UI Variable', 'Segoe UI', Arial, sans-serif;
    font-size:11pt;
}

/* ---------- Analytics Glow-Up ---------- */

QFrame#AnalyticsHeroCard{
    background:qlineargradient(
        x1:0, y1:0,
        x2:1, y2:1,
        stop:0 #1DB954,
        stop:0.35 #143B2A,
        stop:0.7 #17171A,
        stop:1 #101014
    );
    border:1px solid #38F28B;
    border-radius:28px;
}

QLabel#HeroEyebrow{
    color:#B8FFD2;
    font-size:10pt;
    font-weight:900;
    letter-spacing:2px;
}

QLabel#HeroEmoji{
    font-size:46pt;
}

QLabel#HeroPersonality{
    color:#FFFFFF;
    font-size:34pt;
    font-weight:950;
}

QLabel#HeroSubtitle{
    color:#E8FFEf;
    font-size:13.5pt;
    font-weight:650;
}

QLabel#HeroRecommended{
    color:#000000;
    background:#B8FFD2;
    border-radius:12px;
    padding:9px 13px;
    font-size:11pt;
    font-weight:900;
}

QLabel#AuraTitle{
    color:#B8FFD2;
    font-size:10pt;
    font-weight:900;
    letter-spacing:2px;
}

QLabel#AuraNumber{
    color:#FFFFFF;
    font-size:66pt;
    font-weight:950;
}

QLabel#AuraStatus{
    color:#E8FFEf;
    font-size:14pt;
    font-weight:900;
}

QProgressBar#AuraProgress{
    background:rgba(255,255,255,0.20);
    border:none;
    border-radius:6px;
}

QProgressBar#AuraProgress::chunk{
    background:#FFFFFF;
    border-radius:6px;
}

QFrame#GlowMetric{
    background:rgba(0,0,0,0.28);
    border:1px solid rgba(255,255,255,0.18);
    border-radius:18px;
}

QLabel#GlowMetricTitle{
    color:#D8FFE4;
    font-size:10.5pt;
    font-weight:800;
}

QLabel#GlowMetricValue{
    color:#FFFFFF;
    font-size:20pt;
    font-weight:950;
}

QProgressBar#GlowMetricProgress{
    background:rgba(255,255,255,0.18);
    border:none;
    border-radius:5px;
}

QProgressBar#GlowMetricProgress::chunk{
    background:#B8FFD2;
    border-radius:5px;
}

/* ---------- Wrapped Cards ---------- */

QFrame#WrappedStatCard{
    background:qlineargradient(
        x1:0, y1:0,
        x2:1, y2:1,
        stop:0 #19191D,
        stop:0.55 #111114,
        stop:1 #0C0C0F
    );
    border:1px solid #2F2F35;
    border-radius:22px;
}

QFrame#WrappedStatCard:hover{
    border:1px solid #1DB954;
    background:qlineargradient(
        x1:0, y1:0,
        x2:1, y2:1,
        stop:0 #203B2B,
        stop:0.55 #151518,
        stop:1 #0C0C0F
    );
}

QLabel#WrappedEmoji{
    font-size:32pt;
}

QLabel#WrappedTitle{
    color:#9CA3AF;
    font-size:10.5pt;
    font-weight:900;
    letter-spacing:1px;
}

QLabel#WrappedValue{
    color:#FFFFFF;
    font-size:19pt;
    font-weight:950;
}

QLabel#WrappedSubtitle{
    color:#B8B8C0;
    font-size:10.5pt;
    font-weight:600;
}

/* ---------- Badge Cloud ---------- */

QLabel#BadgePill{
    background:qlineargradient(
        x1:0, y1:0,
        x2:1, y2:1,
        stop:0 #1E1E24,
        stop:1 #101014
    );
    border:1px solid #34343A;
    border-radius:18px;
    padding:12px;
    color:#FFFFFF;
    font-size:10.5pt;
    font-weight:850;
}

QLabel#BadgePill:hover{
    border:1px solid #1DB954;
    background:#17251C;
}

QLabel#BadgeEmpty{
    color:#A0A0A0;
    font-size:11pt;
}

/* ---------- Header ---------- */

QFrame#Header{
    background:#08080A;
    border-bottom:1px solid #242428;
}

QLabel#HeaderTitle{
    font-size:22pt;
    font-weight:900;
    color:#FFFFFF;
}

QLabel#HeaderSubtitle{
    font-size:10pt;
    color:#9CA3AF;
}

QLabel#HeaderStatus{
    color:#1DB954;
    font-size:11pt;
    font-weight:800;
}

QLabel#HeaderStatusError{
    color:#FF5C5C;
    font-size:11pt;
    font-weight:800;
}

/* ---------- Sidebar ---------- */

QFrame#Sidebar{
    background:#08080A;
    border-right:1px solid #242428;
}

QLabel#SidebarTitle{
    font-size:20pt;
    font-weight:900;
    color:#FFFFFF;
}

QLabel#SidebarSubtitle{
    color:#9CA3AF;
    font-size:10pt;
    margin-bottom:10px;
}

QLabel#SidebarVersion{
    color:#666666;
    font-size:9pt;
}

/* ---------- Sidebar Buttons ---------- */

QPushButton#SidebarButton{
    background:transparent;
    border:none;
    border-radius:12px;
    text-align:left;
    padding:12px 14px;
    font-size:11pt;
    font-weight:650;
    color:#DADADA;
}

QPushButton#SidebarButton:hover{
    background:#17171A;
    color:#FFFFFF;
}

QPushButton#SidebarButton:pressed{
    background:#1DB954;
    color:#000000;
}

/* ---------- Cards ---------- */

QFrame#Card{
    background:#111114;
    border:1px solid #27272A;
    border-radius:18px;
}

QFrame#Card:hover{
    border:1px solid #36363A;
}

/* ---------- Card Titles ---------- */

QLabel#CardTitle{
    font-size:18pt;
    font-weight:900;
    color:#FFFFFF;
}

/* ---------- Section Titles ---------- */

QLabel#SectionTitle{
    font-size:22pt;
    font-weight:900;
    color:#FFFFFF;
}

/* ---------- General Buttons ---------- */

QPushButton{
    background:#1DB954;
    color:#000000;
    border:none;
    border-radius:12px;
    padding:11px 16px;
    font-size:11pt;
    font-weight:800;
}

QPushButton:hover{
    background:#22D165;
}

QPushButton:pressed{
    background:#159447;
}

QPushButton:disabled{
    background:#2A2A2E;
    color:#777777;
}

/* ---------- Secondary Buttons ---------- */

QPushButton#SecondaryButton{
    background:#19191D;
    border:1px solid #333338;
    color:#F5F5F5;
    border-radius:12px;
    padding:10px 14px;
    font-size:10.5pt;
    font-weight:700;
}

QPushButton#SecondaryButton:hover{
    background:#222228;
    border:1px solid #1DB954;
}

QPushButton#SecondaryButton:pressed{
    background:#111114;
    border:1px solid #1DB954;
}

/* ---------- Inputs ---------- */

QLineEdit{
    background:#151518;
    color:#FFFFFF;
    border:1px solid #333338;
    border-radius:12px;
    padding:10px 14px;
    selection-background-color:#1DB954;
    selection-color:#000000;
}

QLineEdit:hover{
    border:1px solid #44444A;
}

QLineEdit:focus{
    border:1px solid #1DB954;
}

/* ---------- Combo Boxes ---------- */

QComboBox{
    background:#151518;
    color:#FFFFFF;
    border:1px solid #333338;
    border-radius:12px;
    padding:9px 12px;
    font-weight:600;
}

QComboBox:hover{
    border:1px solid #1DB954;
}

QComboBox:focus{
    border:1px solid #1DB954;
}

QComboBox::drop-down{
    border:none;
    width:28px;
}

QComboBox::down-arrow{
    image:none;
    border-left:5px solid transparent;
    border-right:5px solid transparent;
    border-top:6px solid #A0A0A0;
    margin-right:8px;
}

QAbstractItemView{
    background:#151518;
    color:#FFFFFF;
    border:1px solid #333338;
    selection-background-color:#1DB954;
    selection-color:#000000;
    outline:none;
}

/* ---------- Sliders ---------- */

QSlider::groove:horizontal{
    height:6px;
    background:#34343A;
    border-radius:3px;
}

QSlider::sub-page:horizontal{
    background:#1DB954;
    border-radius:3px;
}

QSlider::add-page:horizontal{
    background:#34343A;
    border-radius:3px;
}

QSlider::handle:horizontal{
    background:#FFFFFF;
    border:2px solid #1DB954;
    width:16px;
    height:16px;
    margin:-6px 0;
    border-radius:8px;
}

QSlider::handle:horizontal:hover{
    background:#1DB954;
}

/* ---------- Progress Bar ---------- */

QProgressBar{
    background:#34343A;
    border:none;
    border-radius:5px;
}

QProgressBar::chunk{
    background:#1DB954;
    border-radius:5px;
}

/* ---------- Statistic Tiles ---------- */

QFrame#StatTile{
    background:#151518;
    border:1px solid #2D2D32;
    border-radius:16px;
}

QFrame#StatTile:hover{
    background:#19191D;
    border:1px solid #1DB954;
}

QLabel#StatTitle{
    color:#9CA3AF;
    font-size:10.5pt;
    font-weight:700;
}

QLabel#StatValue{
    color:#FFFFFF;
    font-size:28pt;
    font-weight:900;
}

/* ---------- Queue Items ---------- */

QFrame#QueueItem{
    background:#151518;
    border-radius:14px;
    border:1px solid #2D2D32;
}

QFrame#QueueItem:hover{
    border:1px solid #1DB954;
    background:#1B1B20;
}

QLabel#QueueSong{
    color:#FFFFFF;
    font-size:12pt;
    font-weight:900;
}

QLabel#QueueArtist{
    color:#9CA3AF;
    font-size:10pt;
}

QLabel#QueueDuration{
    color:#888888;
    font-size:10pt;
}

/* ---------- Search Results ---------- */

QWidget#SearchResultItem{
    background:#151518;
    border:1px solid #2D2D32;
    border-radius:14px;
}

QWidget#SearchResultItem:hover{
    background:#1B1B20;
    border:1px solid #1DB954;
}

/* ---------- Dividers ---------- */

QFrame#Divider{
    background:#2F2F35;
    max-height:1px;
    min-height:1px;
    border:none;
}

/* ---------- Scroll Areas ---------- */

QScrollArea{
    border:none;
    background:transparent;
}

QScrollBar:vertical{
    background:#0D0D10;
    width:11px;
    margin:4px 2px 4px 2px;
    border-radius:5px;
}

QScrollBar::handle:vertical{
    background:#333338;
    border-radius:5px;
    min-height:40px;
}

QScrollBar::handle:vertical:hover{
    background:#1DB954;
}

QScrollBar::add-line:vertical,
QScrollBar::sub-line:vertical{
    height:0px;
    background:none;
}

QScrollBar::add-page:vertical,
QScrollBar::sub-page:vertical{
    background:none;
}

QScrollBar:horizontal{
    height:0px;
    background:transparent;
}

/* ---------- Tooltips ---------- */

QToolTip{
    background:#151518;
    color:#FFFFFF;
    border:1px solid #333338;
    border-radius:8px;
    padding:8px;
}

/* ---------- App Status Bar ---------- */

QFrame#AppStatusBar{
    background:#08080A;
    border-top:1px solid #242428;
}

QLabel#StatusMessage{
    color:#9CA3AF;
    font-size:10pt;
    font-weight:600;
}
"""