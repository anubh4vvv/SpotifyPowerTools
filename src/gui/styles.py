APP_STYLE = """
/* =========================================================
   Spotify Power Tools — Aurora UI
   Neon glass music intelligence dashboard
   ========================================================= */

QMainWindow{
    background:#050509;
}

QWidget#AppRoot{
    background:qradialgradient(
        cx:0.10, cy:0.05,
        radius:1.2,
        fx:0.10, fy:0.05,
        stop:0 #153A2B,
        stop:0.24 #081B17,
        stop:0.52 #070711,
        stop:0.78 #090516,
        stop:1 #030305
    );
}

QWidget{
    background:transparent;
    color:#F8FAFC;
    font-family:'Segoe UI Variable', 'Segoe UI', Arial, sans-serif;
    font-size:11pt;
}

QStackedWidget{
    background:transparent;
}

/* ---------- Header ---------- */

QFrame#Header{
    background:qlineargradient(
        x1:0, y1:0,
        x2:1, y2:0,
        stop:0 rgba(9, 12, 18, 235),
        stop:0.45 rgba(10, 20, 22, 225),
        stop:1 rgba(17, 9, 30, 235)
    );
    border-bottom:1px solid rgba(139, 92, 246, 70);
}

QLabel#HeaderLogo{
    background:qlineargradient(
        x1:0, y1:0,
        x2:1, y2:1,
        stop:0 #1DB954,
        stop:0.52 #22D3EE,
        stop:1 #A855F7
    );
    color:#020617;
    border-radius:18px;
    font-size:20pt;
    font-weight:900;
}

QLabel#HeaderTitle{
    font-size:23pt;
    font-weight:900;
    color:#FFFFFF;
}

QLabel#HeaderSubtitle{
    font-size:10pt;
    color:#B7C3D7;
    font-weight:650;
}

QLabel#HeaderStatus{
    color:#03130A;
    background:qlineargradient(
        x1:0, y1:0,
        x2:1, y2:0,
        stop:0 #1DB954,
        stop:1 #B8FFD2
    );
    border-radius:15px;
    padding:7px 13px;
    font-size:10.5pt;
    font-weight:900;
}

QLabel#HeaderStatusError{
    color:#FFFFFF;
    background:qlineargradient(
        x1:0, y1:0,
        x2:1, y2:0,
        stop:0 #EF4444,
        stop:1 #FB7185
    );
    border-radius:15px;
    padding:7px 13px;
    font-size:10.5pt;
    font-weight:900;
}

/* ---------- Sidebar ---------- */

QFrame#Sidebar{
    background:qlineargradient(
        x1:0, y1:0,
        x2:0, y2:1,
        stop:0 rgba(8, 10, 18, 245),
        stop:0.48 rgba(7, 18, 18, 236),
        stop:1 rgba(13, 8, 25, 245)
    );
    border-right:1px solid rgba(34, 211, 238, 55);
}

QLabel#SidebarTitle{
    font-size:21pt;
    font-weight:900;
    color:#FFFFFF;
}

QLabel#SidebarSubtitle{
    color:#B8FFD2;
    font-size:10pt;
    font-weight:750;
    margin-bottom:10px;
}

QLabel#SidebarVersion{
    color:#64748B;
    font-size:9pt;
    font-weight:700;
}

/* ---------- Sidebar Buttons ---------- */

QPushButton#SidebarButton{
    background:transparent;
    border:1px solid transparent;
    border-radius:15px;
    text-align:left;
    padding:12px 14px;
    font-size:11pt;
    font-weight:750;
    color:#CBD5E1;
}

QPushButton#SidebarButton:hover{
    background:rgba(255,255,255,22);
    border:1px solid rgba(34,211,238,70);
    color:#FFFFFF;
}

QPushButton#SidebarButton[active="true"]{
    background:qlineargradient(
        x1:0, y1:0,
        x2:1, y2:0,
        stop:0 #1DB954,
        stop:0.55 #22D3EE,
        stop:1 #A855F7
    );
    color:#020617;
    border:1px solid rgba(255,255,255,100);
    border-radius:15px;
    font-size:11pt;
    font-weight:950;
}

/* ---------- App Status Bar ---------- */

QFrame#AppStatusBar{
    background:rgba(4, 6, 12, 235);
    border-top:1px solid rgba(139, 92, 246, 55);
}

QLabel#StatusDot{
    color:#22D3EE;
    font-size:13pt;
    font-weight:900;
}

QLabel#StatusMessage{
    color:#CBD5E1;
    font-size:10pt;
    font-weight:750;
}

/* ---------- General Cards ---------- */

QFrame#Card{
    background:qlineargradient(
        x1:0, y1:0,
        x2:1, y2:1,
        stop:0 rgba(255,255,255,26),
        stop:0.45 rgba(17,24,39,216),
        stop:1 rgba(3,7,18,235)
    );
    border:1px solid rgba(148, 163, 184, 48);
    border-radius:24px;
}

QFrame#Card:hover{
    border:1px solid rgba(34, 211, 238, 120);
    background:qlineargradient(
        x1:0, y1:0,
        x2:1, y2:1,
        stop:0 rgba(29,185,84,45),
        stop:0.42 rgba(17,24,39,225),
        stop:1 rgba(88,28,135,80)
    );
}

QLabel#CardTitle{
    font-size:18pt;
    font-weight:950;
    color:#FFFFFF;
}

QLabel#SectionTitle{
    font-size:25pt;
    font-weight:950;
    color:#FFFFFF;
}

QLabel#SectionSubtitle{
    color:#94A3B8;
    font-size:11pt;
    font-weight:650;
}

/* ---------- Buttons ---------- */

QPushButton{
    background:qlineargradient(
        x1:0, y1:0,
        x2:1, y2:0,
        stop:0 #1DB954,
        stop:0.55 #22D3EE,
        stop:1 #A855F7
    );
    color:#020617;
    border:none;
    border-radius:14px;
    padding:11px 17px;
    font-size:11pt;
    font-weight:950;
}

QPushButton:hover{
    background:qlineargradient(
        x1:0, y1:0,
        x2:1, y2:0,
        stop:0 #22D165,
        stop:0.55 #67E8F9,
        stop:1 #C084FC
    );
}

QPushButton:pressed{
    background:#1DB954;
}

QPushButton:disabled{
    background:#27272A;
    color:#71717A;
}

QPushButton#SecondaryButton{
    background:rgba(255,255,255,18);
    border:1px solid rgba(148,163,184,55);
    color:#F8FAFC;
    border-radius:14px;
    padding:10px 15px;
    font-size:10.5pt;
    font-weight:850;
}

QPushButton#SecondaryButton:hover{
    background:rgba(34,211,238,28);
    border:1px solid rgba(34,211,238,130);
    color:#FFFFFF;
}

QPushButton#SecondaryButton:pressed{
    background:rgba(29,185,84,60);
}

/* ---------- Inputs ---------- */

QLineEdit{
    background:rgba(15, 23, 42, 210);
    color:#FFFFFF;
    border:1px solid rgba(148,163,184,70);
    border-radius:14px;
    padding:10px 14px;
    selection-background-color:#22D3EE;
    selection-color:#020617;
}

QLineEdit:hover{
    border:1px solid rgba(34,211,238,110);
}

QLineEdit:focus{
    border:1px solid #22D3EE;
}

/* ---------- Combo Boxes ---------- */

QComboBox{
    background:rgba(15, 23, 42, 220);
    color:#FFFFFF;
    border:1px solid rgba(148,163,184,70);
    border-radius:14px;
    padding:9px 12px;
    font-weight:750;
}

QComboBox:hover{
    border:1px solid #22D3EE;
}

QComboBox:focus{
    border:1px solid #A855F7;
}

QComboBox::drop-down{
    border:none;
    width:30px;
}

QComboBox::down-arrow{
    image:none;
    border-left:5px solid transparent;
    border-right:5px solid transparent;
    border-top:6px solid #CBD5E1;
    margin-right:8px;
}

QAbstractItemView{
    background:#0F172A;
    color:#FFFFFF;
    border:1px solid rgba(34,211,238,90);
    selection-background-color:#22D3EE;
    selection-color:#020617;
    outline:none;
}

/* ---------- Sliders ---------- */

QSlider::groove:horizontal{
    height:7px;
    background:rgba(148,163,184,55);
    border-radius:3px;
}

QSlider::sub-page:horizontal{
    background:qlineargradient(
        x1:0, y1:0,
        x2:1, y2:0,
        stop:0 #1DB954,
        stop:0.6 #22D3EE,
        stop:1 #A855F7
    );
    border-radius:3px;
}

QSlider::add-page:horizontal{
    background:rgba(148,163,184,45);
    border-radius:3px;
}

QSlider::handle:horizontal{
    background:#FFFFFF;
    border:2px solid #22D3EE;
    width:17px;
    height:17px;
    margin:-6px 0;
    border-radius:8px;
}

QSlider::handle:horizontal:hover{
    background:#B8FFD2;
    border:2px solid #1DB954;
}

/* ---------- Progress Bar ---------- */

QProgressBar{
    background:rgba(148,163,184,50);
    border:none;
    border-radius:6px;
}

QProgressBar::chunk{
    background:qlineargradient(
        x1:0, y1:0,
        x2:1, y2:0,
        stop:0 #1DB954,
        stop:0.55 #22D3EE,
        stop:1 #A855F7
    );
    border-radius:6px;
}

/* ---------- Statistic Tiles ---------- */

QFrame#StatTile{
    background:qlineargradient(
        x1:0, y1:0,
        x2:1, y2:1,
        stop:0 rgba(34,211,238,28),
        stop:0.55 rgba(15,23,42,225),
        stop:1 rgba(88,28,135,55)
    );
    border:1px solid rgba(148,163,184,50);
    border-radius:21px;
}

QFrame#StatTile:hover{
    border:1px solid rgba(29,185,84,135);
    background:qlineargradient(
        x1:0, y1:0,
        x2:1, y2:1,
        stop:0 rgba(29,185,84,55),
        stop:0.55 rgba(15,23,42,225),
        stop:1 rgba(168,85,247,70)
    );
}

QLabel#StatTitle{
    color:#A7F3D0;
    font-size:10.5pt;
    font-weight:900;
}

QLabel#StatValue{
    color:#FFFFFF;
    font-size:27pt;
    font-weight:950;
}

/* ---------- Analytics Hero ---------- */

QFrame#AnalyticsHeroCard{
    background:qradialgradient(
        cx:0.15, cy:0.15,
        radius:1.1,
        fx:0.15, fy:0.15,
        stop:0 #B8FFD2,
        stop:0.18 #1DB954,
        stop:0.46 #0F766E,
        stop:0.73 #312E81,
        stop:1 #0B0618
    );
    border:1px solid rgba(255,255,255,120);
    border-radius:32px;
}

QLabel#HeroEyebrow{
    color:#E0FFF0;
    font-size:10pt;
    font-weight:950;
    letter-spacing:2px;
}

QLabel#HeroEmoji{
    font-size:52pt;
}

QLabel#HeroPersonality{
    color:#FFFFFF;
    font-size:38pt;
    font-weight:950;
}

QLabel#HeroSubtitle{
    color:#ECFEFF;
    font-size:14pt;
    font-weight:750;
}

QLabel#HeroRecommended{
    color:#020617;
    background:qlineargradient(
        x1:0, y1:0,
        x2:1, y2:0,
        stop:0 #B8FFD2,
        stop:0.5 #67E8F9,
        stop:1 #DDD6FE
    );
    border-radius:14px;
    padding:10px 14px;
    font-size:11pt;
    font-weight:950;
}

QLabel#AuraTitle{
    color:#ECFEFF;
    font-size:10pt;
    font-weight:950;
    letter-spacing:2px;
}

QLabel#AuraNumber{
    color:#FFFFFF;
    font-size:72pt;
    font-weight:950;
}

QLabel#AuraStatus{
    color:#ECFEFF;
    font-size:15pt;
    font-weight:950;
}

QProgressBar#AuraProgress{
    background:rgba(255,255,255,45);
    border:none;
    border-radius:7px;
}

QProgressBar#AuraProgress::chunk{
    background:#FFFFFF;
    border-radius:7px;
}

QFrame#GlowMetric{
    background:rgba(2,6,23,105);
    border:1px solid rgba(255,255,255,55);
    border-radius:20px;
}

QLabel#GlowMetricTitle{
    color:#D8FFE4;
    font-size:10.5pt;
    font-weight:900;
}

QLabel#GlowMetricValue{
    color:#FFFFFF;
    font-size:22pt;
    font-weight:950;
}

QProgressBar#GlowMetricProgress{
    background:rgba(255,255,255,38);
    border:none;
    border-radius:6px;
}

QProgressBar#GlowMetricProgress::chunk{
    background:qlineargradient(
        x1:0, y1:0,
        x2:1, y2:0,
        stop:0 #FFFFFF,
        stop:1 #B8FFD2
    );
    border-radius:6px;
}

/* ---------- Wrapped Cards ---------- */

QFrame#WrappedStatCard{
    background:qradialgradient(
        cx:0.12, cy:0.12,
        radius:1.0,
        fx:0.12, fy:0.12,
        stop:0 rgba(34,211,238,55),
        stop:0.42 rgba(17,24,39,235),
        stop:1 rgba(8,8,15,245)
    );
    border:1px solid rgba(148,163,184,58);
    border-radius:26px;
}

QFrame#WrappedStatCard:hover{
    border:1px solid rgba(34,211,238,150);
    background:qradialgradient(
        cx:0.12, cy:0.12,
        radius:1.0,
        fx:0.12, fy:0.12,
        stop:0 rgba(29,185,84,75),
        stop:0.44 rgba(15,23,42,235),
        stop:1 rgba(88,28,135,90)
    );
}

QLabel#WrappedEmoji{
    font-size:36pt;
}

QLabel#WrappedTitle{
    color:#A7F3D0;
    font-size:10.5pt;
    font-weight:950;
    letter-spacing:1px;
}

QLabel#WrappedValue{
    color:#FFFFFF;
    font-size:21pt;
    font-weight:950;
}

QLabel#WrappedSubtitle{
    color:#CBD5E1;
    font-size:10.5pt;
    font-weight:700;
}

/* ---------- Badge Cloud ---------- */

QLabel#BadgePill{
    background:qlineargradient(
        x1:0, y1:0,
        x2:1, y2:1,
        stop:0 rgba(29,185,84,55),
        stop:0.5 rgba(15,23,42,230),
        stop:1 rgba(168,85,247,70)
    );
    border:1px solid rgba(255,255,255,65);
    border-radius:20px;
    padding:13px;
    color:#FFFFFF;
    font-size:10.5pt;
    font-weight:900;
}

QLabel#BadgePill:hover{
    border:1px solid #67E8F9;
    background:rgba(34,211,238,45);
}

QLabel#BadgeEmpty{
    color:#94A3B8;
    font-size:11pt;
    font-weight:700;
}

/* ---------- Queue Items ---------- */

QFrame#QueueItem{
    background:rgba(15,23,42,220);
    border-radius:18px;
    border:1px solid rgba(148,163,184,55);
}

QFrame#QueueItem:hover{
    border:1px solid rgba(34,211,238,130);
    background:rgba(29,185,84,28);
}

QLabel#QueueSong{
    color:#FFFFFF;
    font-size:12pt;
    font-weight:950;
}

QLabel#QueueArtist{
    color:#CBD5E1;
    font-size:10pt;
}

QLabel#QueueDuration{
    color:#94A3B8;
    font-size:10pt;
}

/* ---------- Search Results ---------- */

QWidget#SearchResultItem{
    background:rgba(15,23,42,220);
    border:1px solid rgba(148,163,184,55);
    border-radius:18px;
}

QWidget#SearchResultItem:hover{
    background:rgba(34,211,238,30);
    border:1px solid rgba(34,211,238,130);
}

/* ---------- Dividers ---------- */

QFrame#Divider{
    background:rgba(148,163,184,60);
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
    background:rgba(2,6,23,155);
    width:12px;
    margin:4px 2px 4px 2px;
    border-radius:6px;
}

QScrollBar::handle:vertical{
    background:qlineargradient(
        x1:0, y1:0,
        x2:0, y2:1,
        stop:0 #1DB954,
        stop:0.55 #22D3EE,
        stop:1 #A855F7
    );
    border-radius:6px;
    min-height:42px;
}

QScrollBar::handle:vertical:hover{
    background:#67E8F9;
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
    background:#0F172A;
    color:#FFFFFF;
    border:1px solid #22D3EE;
    border-radius:10px;
    padding:8px;
}
"""