APP_STYLE = """
QMainWindow{
    background:#000000;
}

QWidget{
    background:transparent;
    color:white;
    font-family:'Segoe UI';
    font-size:11pt;
}

/* ---------- Header ---------- */

QFrame#Header{
    background:#0B0B0D;
    border-bottom:1px solid #242424;
}

QLabel#HeaderTitle{
    font-size:22pt;
    font-weight:800;
    color:white;
}

QLabel#HeaderSubtitle{
    font-size:10pt;
    color:#A0A0A0;
}

QLabel#HeaderStatus{
    color:#1DB954;
    font-size:11pt;
    font-weight:700;
}

QLabel#HeaderStatusError{
    color:#E74C3C;
    font-size:11pt;
    font-weight:700;
}

/* ---------- Sidebar ---------- */

QFrame#Sidebar{
    background:#0B0B0D;
    border-right:1px solid #242424;
}

QLabel#SidebarTitle{
    font-size:20pt;
    font-weight:800;
    color:white;
}

QLabel#SidebarSubtitle{
    color:#A0A0A0;
    font-size:10pt;
    margin-bottom:10px;
}

QLabel#SidebarVersion{
    color:#777777;
    font-size:9pt;
}

/* ---------- Sidebar Buttons ---------- */

QPushButton#SidebarButton{
    background:transparent;
    border:none;
    border-radius:10px;
    text-align:left;
    padding:12px 14px;
    font-size:11pt;
    color:#EAEAEA;
}

QPushButton#SidebarButton:hover{
    background:#1A1A1D;
}

QPushButton#SidebarButton:pressed{
    background:#1DB954;
}

/* ---------- Cards ---------- */

QFrame#Card{
    background:#111113;
    border:1px solid #292929;
    border-radius:16px;
}

QFrame#Card:hover{
    border:1px solid #3A3A3A;
}

/* ---------- Card Titles ---------- */

QLabel#CardTitle{
    font-size:18pt;
    font-weight:800;
    color:white;
}

/* ---------- Buttons ---------- */

QPushButton{
    background:#1DB954;
    color:white;
    border:none;
    border-radius:10px;
    padding:12px;
    font-size:11pt;
    font-weight:600;
}

QPushButton:hover{
    background:#21C95D;
}

QPushButton:pressed{
    background:#169C46;
}

QPushButton:disabled{
    background:#333333;
    color:#888888;
}

/* ---------- Secondary Button ---------- */

QPushButton#SecondaryButton{
    background:#181818;
    border:1px solid #333333;
    color:white;
    border-radius:10px;
    padding:10px;
}

QPushButton#SecondaryButton:hover{
    background:#222222;
}

/* ---------- Statistic Tiles ---------- */

QFrame#StatTile{
    background:#18181B;
    border:1px solid #303030;
    border-radius:14px;
}

QFrame#StatTile:hover{
    border:1px solid #1DB954;
}

QLabel#StatTitle{
    color:#A0A0A0;
    font-size:11pt;
    font-weight:600;
}

QLabel#StatValue{
    color:white;
    font-size:28pt;
    font-weight:800;
}

/* ---------- Queue ---------- */

QFrame#QueueItem{
    background:#18181B;
    border-radius:12px;
    border:1px solid #2C2C2C;
}

QFrame#QueueItem:hover{
    border:1px solid #1DB954;
    background:#1F1F22;
}

QLabel#QueueSong{
    color:white;
    font-size:12pt;
    font-weight:800;
}

QLabel#QueueArtist{
    color:#A0A0A0;
    font-size:10pt;
}

QLabel#QueueDuration{
    color:#9A9A9A;
    font-size:10pt;
}

/* ---------- Section Titles ---------- */

QLabel#SectionTitle{
    font-size:20pt;
    font-weight:800;
    color:white;
}

/* ---------- Divider ---------- */

QFrame#Divider{
    background:#2F2F2F;
    max-height:1px;
    min-height:1px;
    border:none;
}

/* ---------- Progress Bar ---------- */

QProgressBar{
    background:#333333;
    border:none;
    border-radius:4px;
}

QProgressBar::chunk{
    background:#1DB954;
    border-radius:4px;
}

/* ---------- Combo Box ---------- */

QComboBox{
    background:#18181B;
    color:white;
    border:1px solid #333333;
    border-radius:8px;
    padding:8px;
}

QComboBox:hover{
    border:1px solid #1DB954;
}

/* ---------- Sliders ---------- */

QSlider::groove:horizontal{
    height:5px;
    background:#444444;
    border-radius:2px;
}

QSlider::handle:horizontal{
    background:#1DB954;
    width:14px;
    height:14px;
    margin:-5px 0;
    border-radius:7px;
}

/* ---------- Scroll Area ---------- */

QScrollArea{
    border:none;
}

QScrollBar:vertical{
    background:#111113;
    width:10px;
    margin:0;
}

QScrollBar::handle:vertical{
    background:#333333;
    border-radius:5px;
}

QScrollBar::handle:vertical:hover{
    background:#1DB954;
}

QScrollBar::add-line:vertical,
QScrollBar::sub-line:vertical{
    height:0;
}

/* ---------- App Status Bar ---------- */

QFrame#AppStatusBar{
    background:#0B0B0D;
    border-top:1px solid #242424;
}

QLabel#StatusMessage{
    color:#A0A0A0;
    font-size:10pt;
}
"""