import random

from PySide6.QtWidgets import (
    QWidget,
    QFrame,
    QLabel,
    QVBoxLayout,
    QHBoxLayout,
    QGridLayout,
)

from PySide6.QtCore import Qt, QPoint

from PySide6.QtGui import (
    QPainter,
    QPixmap,
    QColor,
    QLinearGradient,
    QRadialGradient,
)


def shorten(text, limit=42):

    if text is None:
        return ""

    text = str(text)

    if len(text) <= limit:
        return text

    return text[:limit - 3] + "..."


def safe_number(value, default=0):

    try:
        return float(value)

    except (TypeError, ValueError):
        return default


def as_int(value):

    return int(
        round(
            safe_number(value)
        )
    )


def get_card_value(card, fallback="No data yet"):

    if not isinstance(card, dict):
        return fallback

    for key in [
        "value",
        "name",
        "title",
        "song_name",
        "track_name",
        "artist",
    ]:

        value = card.get(key)

        if value not in (None, "", [], {}):
            return str(value)

    return fallback


def get_card_subtitle(card, fallback=""):

    if not isinstance(card, dict):
        return fallback

    for key in [
        "subtitle",
        "description",
        "artist",
        "meta",
        "reason",
    ]:

        value = card.get(key)

        if value not in (None, "", [], {}):
            return str(value)

    return fallback


class ShareMiniCard(QFrame):

    def __init__(self, title, emoji):
        super().__init__()

        self.setObjectName("ShareMiniCard")

        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 18, 20, 18)
        layout.setSpacing(7)

        self.emoji_label = QLabel(emoji)
        self.emoji_label.setObjectName("ShareMiniEmoji")

        self.title_label = QLabel(title)
        self.title_label.setObjectName("ShareMiniTitle")

        self.value_label = QLabel("No data yet")
        self.value_label.setObjectName("ShareMiniValue")
        self.value_label.setWordWrap(True)

        self.subtitle_label = QLabel("")
        self.subtitle_label.setObjectName("ShareMiniSubtitle")
        self.subtitle_label.setWordWrap(True)

        layout.addWidget(self.emoji_label)
        layout.addWidget(self.title_label)
        layout.addSpacing(2)
        layout.addWidget(self.value_label)
        layout.addWidget(self.subtitle_label)
        layout.addStretch()

    def update_card(self, data):

        if not isinstance(data, dict):
            data = {}

        self.emoji_label.setText(
            data.get("emoji", "✨")
        )

        self.title_label.setText(
            data.get("title", self.title_label.text())
        )

        self.value_label.setText(
            shorten(
                get_card_value(data),
                36
            )
        )

        self.subtitle_label.setText(
            shorten(
                get_card_subtitle(data),
                58
            )
        )


class ShareMetric(QFrame):

    def __init__(self, label):
        super().__init__()

        self.setObjectName("ShareMetric")

        layout = QVBoxLayout(self)
        layout.setContentsMargins(16, 14, 16, 14)
        layout.setSpacing(5)

        self.value = QLabel("0%")
        self.value.setObjectName("ShareMetricValue")
        self.value.setAlignment(Qt.AlignCenter)

        self.label = QLabel(label)
        self.label.setObjectName("ShareMetricLabel")
        self.label.setAlignment(Qt.AlignCenter)

        layout.addStretch()
        layout.addWidget(self.value)
        layout.addWidget(self.label)
        layout.addStretch()

    def set_value(self, value, suffix="%"):

        number = as_int(value)

        self.value.setText(
            f"{number}{suffix}"
        )


class ShareCardWidget(QWidget):

    WIDTH = 900
    HEIGHT = 1200

    THEME_ALIASES = {
        "Aurora": "Golden Hour",
        "Midnight": "Late Night",
        "Neon Pop": "Rosewood",
    }

    THEMES = {
        "Golden Hour": {
            "background": "#0f0d09",
            "panel": "#1d1812",
            "panel_alt": "#221c16",
            "line": "#3a3226",
            "text": "#f3ecdf",
            "muted": "#c9bfae",
            "low": "#8f8574",
            "accent": "#e3a857",
            "accent_soft": "#efb667",
            "sage": "#a8b487",
            "rose": "#c98a7d",
            "glow": "#7a4a18",
        },
        "Late Night": {
            "background": "#0d1117",
            "panel": "#151922",
            "panel_alt": "#1b2230",
            "line": "#2b3444",
            "text": "#eef2ff",
            "muted": "#bbc4d6",
            "low": "#7c8798",
            "accent": "#a8b487",
            "accent_soft": "#c0cca0",
            "sage": "#8fb6a1",
            "rose": "#c98a7d",
            "glow": "#283a31",
        },
        "Rosewood": {
            "background": "#120d0d",
            "panel": "#211616",
            "panel_alt": "#2b1b19",
            "line": "#44302b",
            "text": "#f7ebe2",
            "muted": "#d3bdb1",
            "low": "#947f76",
            "accent": "#c98a7d",
            "accent_soft": "#e1a99e",
            "sage": "#a8b487",
            "rose": "#e3a857",
            "glow": "#6a2924",
        },
    }

    def __init__(self, theme_name="Golden Hour"):
        super().__init__()

        theme_name = self.THEME_ALIASES.get(
            theme_name,
            theme_name
        )

        self.theme_name = theme_name or "Golden Hour"
        self.theme = self.THEMES.get(
            self.theme_name,
            self.THEMES["Golden Hour"]
        )

        self.grain = self.create_grain_tile()

        self.setObjectName("ShareCardRoot")
        self.setFixedSize(
            self.WIDTH,
            self.HEIGHT
        )

        self.setAttribute(
            Qt.WA_StyledBackground,
            False
        )

        root = QVBoxLayout(self)
        root.setContentsMargins(52, 46, 52, 38)
        root.setSpacing(22)

        # ---------- Header ----------

        header = QHBoxLayout()
        header.setSpacing(16)

        self.logo = QLabel("♫")
        self.logo.setObjectName("ShareLogo")
        self.logo.setAlignment(Qt.AlignCenter)
        self.logo.setFixedSize(56, 56)

        header_text = QVBoxLayout()
        header_text.setSpacing(1)

        self.app_title = QLabel(
            'Power<span style="color:#e3a857;">Tools</span>'
        )
        self.app_title.setTextFormat(Qt.RichText)
        self.app_title.setObjectName("ShareAppTitle")

        self.generated_label = QLabel("FOR SPOTIFY")
        self.generated_label.setObjectName("ShareGenerated")

        header_text.addWidget(self.app_title)
        header_text.addWidget(self.generated_label)

        self.playlist_label = QLabel("<3")
        self.playlist_label.setObjectName("SharePlaylist")
        self.playlist_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.playlist_label.setWordWrap(True)

        header.addWidget(self.logo)
        header.addLayout(header_text)
        header.addStretch()
        header.addWidget(self.playlist_label, 1)

        root.addLayout(header)

        # ---------- Hero ----------

        self.hero = QFrame()
        self.hero.setObjectName("ShareHero")
        self.hero.setMinimumHeight(260)

        hero_layout = QHBoxLayout(self.hero)
        hero_layout.setContentsMargins(30, 28, 30, 28)
        hero_layout.setSpacing(26)

        left = QVBoxLayout()
        left.setSpacing(9)

        self.eyebrow = QLabel("MY PLAYLIST PERSONALITY")
        self.eyebrow.setObjectName("ShareEyebrow")

        personality_row = QHBoxLayout()
        personality_row.setSpacing(18)

        self.personality_emoji = QLabel("✨")
        self.personality_emoji.setObjectName("SharePersonalityEmoji")
        self.personality_emoji.setFixedSize(74, 74)
        self.personality_emoji.setAlignment(Qt.AlignCenter)

        self.personality_title = QLabel("Main Character Mix")
        self.personality_title.setObjectName("SharePersonalityTitle")
        self.personality_title.setWordWrap(True)

        personality_row.addWidget(self.personality_emoji)
        personality_row.addWidget(self.personality_title, 1)

        self.personality_subtitle = QLabel(
            "Balanced vibes with enough personality to keep it moving."
        )
        self.personality_subtitle.setObjectName("SharePersonalitySubtitle")
        self.personality_subtitle.setWordWrap(True)

        self.recommended_profile = QLabel("Recommended: Balanced")
        self.recommended_profile.setObjectName("ShareRecommended")

        left.addWidget(self.eyebrow)
        left.addLayout(personality_row)
        left.addSpacing(2)
        left.addWidget(self.personality_subtitle)
        left.addSpacing(8)
        left.addWidget(self.recommended_profile)
        left.addStretch()

        self.aura_box = QFrame()
        self.aura_box.setObjectName("ShareAuraBox")
        self.aura_box.setFixedSize(176, 176)

        aura_layout = QVBoxLayout(self.aura_box)
        aura_layout.setContentsMargins(0, 0, 0, 0)
        aura_layout.setSpacing(0)
        aura_layout.setAlignment(Qt.AlignCenter)

        self.aura_score = QLabel("0")
        self.aura_score.setObjectName("ShareAuraScore")
        self.aura_score.setAlignment(Qt.AlignCenter)

        self.aura_label = QLabel("AURA SCORE")
        self.aura_label.setObjectName("ShareAuraLabel")
        self.aura_label.setAlignment(Qt.AlignCenter)

        self.aura_status = QLabel("Needs Vibes")
        self.aura_status.setObjectName("ShareAuraStatus")
        self.aura_status.setAlignment(Qt.AlignCenter)

        aura_layout.addStretch()
        aura_layout.addWidget(self.aura_score)
        aura_layout.addWidget(self.aura_label)
        aura_layout.addSpacing(6)
        aura_layout.addWidget(self.aura_status)
        aura_layout.addStretch()

        hero_layout.addLayout(left, 1)
        hero_layout.addWidget(
            self.aura_box,
            alignment=Qt.AlignCenter
        )

        root.addWidget(self.hero)

        # ---------- Metrics ----------

        metrics = QGridLayout()
        metrics.setSpacing(14)

        self.taste_metric = ShareMetric("Taste Match")
        self.variety_metric = ShareMetric("Variety")
        self.replay_metric = ShareMetric("Replay Energy")

        metrics.addWidget(self.taste_metric, 0, 0)
        metrics.addWidget(self.variety_metric, 0, 1)
        metrics.addWidget(self.replay_metric, 0, 2)

        root.addLayout(metrics)

        # ---------- Highlights ----------

        self.highlights_title = QLabel("Wrapped Highlights")
        self.highlights_title.setObjectName("ShareSectionTitle")

        root.addWidget(self.highlights_title)

        cards_grid = QGridLayout()
        cards_grid.setSpacing(14)

        self.top_artist_card = ShareMiniCard("Top Artist", "🎤")
        self.replayed_card = ShareMiniCard("Most Replayed", "🔁")
        self.skipped_card = ShareMiniCard("Most Skipped", "⏭")
        self.hidden_card = ShareMiniCard("Hidden Favorite", "💎")

        cards_grid.addWidget(self.top_artist_card, 0, 0)
        cards_grid.addWidget(self.replayed_card, 0, 1)
        cards_grid.addWidget(self.skipped_card, 1, 0)
        cards_grid.addWidget(self.hidden_card, 1, 1)

        root.addLayout(cards_grid)

        # ---------- Badges ----------

        self.badges_title = QLabel("Badges")
        self.badges_title.setObjectName("ShareSectionTitle")

        root.addWidget(self.badges_title)

        self.badges_row = QHBoxLayout()
        self.badges_row.setSpacing(12)

        self.badge_labels = []

        for index in range(4):

            badge = QLabel("✨ Fresh Start")
            badge.setObjectName(f"ShareBadge{index}")
            badge.setProperty("badge", "true")
            badge.setAlignment(Qt.AlignCenter)
            badge.setWordWrap(True)
            badge.setMinimumHeight(62)

            self.badge_labels.append(badge)
            self.badges_row.addWidget(badge)

        root.addLayout(self.badges_row)

        root.addStretch()

        # ---------- Footer ----------

        self.footer = QLabel("Generated with Spotify Power Tools")
        self.footer.setObjectName("ShareFooter")
        self.footer.setAlignment(Qt.AlignCenter)

        root.addWidget(self.footer)

        self.apply_theme(
            self.theme_name
        )

    def create_grain_tile(self):

        size = 180
        pixmap = QPixmap(size, size)
        pixmap.fill(Qt.transparent)

        painter = QPainter(pixmap)
        random.seed(42)

        for _ in range(2600):

            x = random.randint(0, size - 1)
            y = random.randint(0, size - 1)

            if random.random() < 0.58:
                color = QColor(255, 241, 218, random.randint(5, 18))
            else:
                color = QColor(0, 0, 0, random.randint(7, 22))

            painter.setPen(color)
            painter.drawPoint(x, y)

        painter.end()

        return pixmap

    def paintEvent(self, event):

        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        bg = QColor(
            self.theme["background"]
        )

        painter.fillRect(
            self.rect(),
            bg
        )

        glow = QRadialGradient(
            130,
            120,
            760
        )
        glow.setColorAt(
            0.0,
            QColor(self.theme["glow"])
        )
        glow.setColorAt(
            0.38,
            QColor(self.theme["background"])
        )
        glow.setColorAt(
            1.0,
            QColor("#050403")
        )

        painter.fillRect(
            self.rect(),
            glow
        )

        wash = QLinearGradient(
            0,
            0,
            self.WIDTH,
            self.HEIGHT
        )
        wash.setColorAt(
            0.0,
            QColor(255, 255, 255, 11)
        )
        wash.setColorAt(
            0.45,
            QColor(255, 255, 255, 0)
        )
        wash.setColorAt(
            1.0,
            QColor(0, 0, 0, 85)
        )

        painter.fillRect(
            self.rect(),
            wash
        )

        painter.setOpacity(0.20)
        painter.drawTiledPixmap(
            self.rect(),
            self.grain
        )
        painter.setOpacity(1.0)

        vignette = QRadialGradient(
            self.WIDTH / 2,
            self.HEIGHT / 2,
            self.WIDTH * 0.72
        )
        vignette.setColorAt(
            0.0,
            QColor(0, 0, 0, 0)
        )
        vignette.setColorAt(
            1.0,
            QColor(0, 0, 0, 92)
        )

        painter.fillRect(
            self.rect(),
            vignette
        )

        painter.end()

        super().paintEvent(event)

    def get_aura_status(self, score):

        if score >= 90:
            return "Legendary"

        if score >= 80:
            return "Excellent"

        if score >= 65:
            return "Strong"

        if score >= 45:
            return "Developing"

        return "Needs Vibes"

    def apply_theme(self, theme_name):

        theme_name = self.THEME_ALIASES.get(
            theme_name,
            theme_name
        )

        self.theme_name = theme_name or "Golden Hour"

        self.theme = self.THEMES.get(
            self.theme_name,
            self.THEMES["Golden Hour"]
        )

        t = self.theme

        self.setStyleSheet(f"""
        QWidget#ShareCardRoot {{
            background: transparent;
        }}

        QLabel#ShareLogo {{
            background: {t["accent"]};
            color: #14110e;
            border-radius: 18px;
            font-size: 24pt;
            font-weight: 950;
        }}

        QLabel#ShareAppTitle {{
            color: {t["text"]};
            font-family: "Fraunces 72pt", "Fraunces", Georgia;
            font-size: 29pt;
            font-weight: 500;
        }}

        QLabel#ShareGenerated {{
            color: {t["low"]};
            font-family: "JetBrains Mono", Consolas;
            font-size: 9pt;
            font-weight: 900;
            letter-spacing: 4px;
        }}

        QLabel#SharePlaylist {{
            color: {t["muted"]};
            font-size: 12pt;
            font-weight: 800;
        }}

        QFrame#ShareHero {{
            background:
                qlineargradient(
                    x1:0, y1:0,
                    x2:1, y2:1,
                    stop:0 {t["panel_alt"]},
                    stop:1 {t["panel"]}
                );
            border: 1px solid {t["line"]};
            border-radius: 16px;
        }}

        QLabel#ShareEyebrow {{
            color: {t["low"]};
            font-family: "JetBrains Mono", Consolas;
            font-size: 9.5pt;
            font-weight: 950;
            letter-spacing: 2px;
        }}

        QLabel#SharePersonalityEmoji {{
            background: rgba(227, 168, 87, 32);
            border: 1px solid {t["line"]};
            border-radius: 18px;
            font-size: 31pt;
        }}

        QLabel#SharePersonalityTitle {{
            color: {t["accent"]};
            font-family: "Fraunces 72pt", "Fraunces", Georgia;
            font-size: 38pt;
            font-style: italic;
            font-weight: 500;
        }}

        QLabel#SharePersonalitySubtitle {{
            color: {t["text"]};
            font-size: 14pt;
            font-weight: 650;
        }}

        QLabel#ShareRecommended {{
            color: {t["background"]};
            background: {t["accent"]};
            border-radius: 13px;
            padding: 10px 14px;
            font-size: 11pt;
            font-weight: 950;
        }}

        QFrame#ShareAuraBox {{
            border: 3px solid {t["accent"]};
            border-radius: 88px;
            background: rgba(20, 17, 14, 150);
        }}

        QLabel#ShareAuraScore {{
            color: {t["accent"]};
            font-family: "Fraunces 72pt", "Fraunces", Georgia;
            font-size: 56pt;
            font-weight: 500;
        }}

        QLabel#ShareAuraLabel {{
            color: {t["low"]};
            font-family: "JetBrains Mono", Consolas;
            font-size: 8.5pt;
            font-weight: 950;
            letter-spacing: 2px;
        }}

        QLabel#ShareAuraStatus {{
            color: {t["sage"]};
            font-size: 10.5pt;
            font-weight: 850;
        }}

        QFrame#ShareMetric {{
            background: rgba(34, 28, 22, 190);
            border: 1px solid {t["line"]};
            border-radius: 12px;
        }}

        QLabel#ShareMetricValue {{
            color: {t["text"]};
            font-family: "Fraunces 72pt", "Fraunces", Georgia;
            font-size: 30pt;
            font-weight: 500;
        }}

        QLabel#ShareMetricLabel {{
            color: {t["low"]};
            font-family: "JetBrains Mono", Consolas;
            font-size: 9pt;
            font-weight: 900;
            letter-spacing: 2px;
        }}

        QLabel#ShareSectionTitle {{
            color: {t["text"]};
            font-family: "Fraunces 72pt", "Fraunces", Georgia;
            font-size: 21pt;
            font-weight: 500;
        }}

        QFrame#ShareMiniCard {{
            background: rgba(29, 24, 18, 212);
            border: 1px solid {t["line"]};
            border-radius: 14px;
        }}

        QLabel#ShareMiniEmoji {{
            font-size: 24pt;
        }}

        QLabel#ShareMiniTitle {{
            color: {t["accent"]};
            font-family: "JetBrains Mono", Consolas;
            font-size: 9.5pt;
            font-weight: 950;
            letter-spacing: 1px;
        }}

        QLabel#ShareMiniValue {{
            color: {t["text"]};
            font-family: "Fraunces 72pt", "Fraunces", Georgia;
            font-size: 19pt;
            font-weight: 500;
        }}

        QLabel#ShareMiniSubtitle {{
            color: {t["muted"]};
            font-size: 9.5pt;
            font-weight: 650;
        }}

        QLabel[badge="true"] {{
            background: rgba(34, 28, 22, 190);
            border: 1px solid {t["line"]};
            border-radius: 13px;
            color: {t["text"]};
            font-size: 10pt;
            font-weight: 850;
            padding: 10px;
        }}

        QLabel#ShareFooter {{
            color: {t["muted"]};
            font-family: "JetBrains Mono", Consolas;
            font-size: 9pt;
            font-weight: 800;
        }}
        """)

        self.update()

    def update_data(self, playlist, analytics):

        analytics = analytics or {}

        glow = analytics.get(
            "analytics_glow",
            {}
        )

        intelligence = analytics.get(
            "playlist_intelligence",
            {}
        )

        personality = glow.get(
            "personality",
            {}
        )

        playlist_name = "Unknown Playlist"

        if playlist is not None:
            playlist_name = playlist.get(
                "name",
                "Unknown Playlist"
            )

        self.playlist_label.setText(
            shorten(
                playlist_name,
                34
            )
        )

        self.personality_emoji.setText(
            personality.get("emoji", "✨")
        )

        self.personality_title.setText(
            personality.get("title", "Main Character Mix")
        )

        self.personality_subtitle.setText(
            personality.get(
                "subtitle",
                "Balanced vibes with enough personality to keep it moving."
            )
        )

        recommended = intelligence.get(
            "recommended_profile",
            "Balanced"
        )

        confidence = intelligence.get(
            "recommendation_confidence",
            "Low"
        )

        self.recommended_profile.setText(
            f"Recommended: {recommended} • {confidence} Confidence"
        )

        aura_score = safe_number(
            glow.get("aura_score", 0)
        )

        self.aura_score.setText(
            str(round(aura_score))
        )

        self.aura_status.setText(
            self.get_aura_status(
                aura_score
            )
        )

        self.taste_metric.set_value(
            glow.get("taste_match", 0)
        )

        self.variety_metric.set_value(
            glow.get("variety_score", 0)
        )

        self.replay_metric.set_value(
            glow.get("replay_energy", 0)
        )

        wrapped = glow.get(
            "wrapped_cards",
            {}
        )

        self.top_artist_card.update_card(
            wrapped.get("top_artist", {
                "emoji": "🎤",
                "title": "Top Artist",
            })
        )

        self.replayed_card.update_card(
            wrapped.get("most_replayed", {
                "emoji": "🔁",
                "title": "Most Replayed",
            })
        )

        self.skipped_card.update_card(
            wrapped.get("most_skipped", {
                "emoji": "⏭",
                "title": "Most Skipped",
            })
        )

        self.hidden_card.update_card(
            wrapped.get("hidden_favorite", {
                "emoji": "💎",
                "title": "Hidden Favorite",
            })
        )

        badges = glow.get(
            "badges",
            []
        )

        for index, label in enumerate(self.badge_labels):

            if index < len(badges):

                badge = badges[index]

                if isinstance(badge, dict):

                    label.setText(
                        f"{badge.get('emoji', '✨')}  {badge.get('title', 'Badge')}"
                    )

                else:

                    label.setText(
                        f"✨  {badge}"
                    )

                label.show()

            else:

                label.setText("✨  Fresh Start")
                label.show()

    def save_to_png(self, file_path):

        self.ensurePolished()

        if self.layout() is not None:
            self.layout().activate()

        pixmap = QPixmap(
            self.size()
        )

        pixmap.fill(
            QColor(self.theme["background"])
        )

        painter = QPainter(
            pixmap
        )

        painter.setRenderHint(
            QPainter.Antialiasing
        )

        self.render(
            painter,
            QPoint(0, 0)
        )

        painter.end()

        return pixmap.save(
            file_path,
            "PNG"
        )