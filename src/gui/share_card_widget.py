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
)


def shorten(text, limit=42):

    if text is None:
        return ""

    text = str(text)

    if len(text) <= limit:
        return text

    return text[:limit - 3] + "..."


class ShareMiniCard(QFrame):

    def __init__(self, title, emoji):
        super().__init__()

        self.setObjectName("ShareMiniCard")

        layout = QVBoxLayout(self)
        layout.setContentsMargins(18, 16, 18, 16)
        layout.setSpacing(6)

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
        layout.addWidget(self.value_label)
        layout.addWidget(self.subtitle_label)
        layout.addStretch()

    def update_card(self, data):

        self.emoji_label.setText(
            data.get("emoji", "✨")
        )

        self.title_label.setText(
            data.get("title", "Highlight")
        )

        self.value_label.setText(
            shorten(
                data.get("value", "No data yet"),
                38
            )
        )

        self.subtitle_label.setText(
            shorten(
                data.get("subtitle", ""),
                58
            )
        )


class ShareMetric(QFrame):

    def __init__(self, label):
        super().__init__()

        self.setObjectName("ShareMetric")

        layout = QVBoxLayout(self)
        layout.setContentsMargins(14, 12, 14, 12)
        layout.setSpacing(3)

        self.value = QLabel("0")
        self.value.setObjectName("ShareMetricValue")
        self.value.setAlignment(Qt.AlignCenter)

        self.label = QLabel(label)
        self.label.setObjectName("ShareMetricLabel")
        self.label.setAlignment(Qt.AlignCenter)

        layout.addWidget(self.value)
        layout.addWidget(self.label)

    def set_value(self, value, suffix="%"):

        if value is None:
            value = 0

        value = round(
            float(value)
        )

        self.value.setText(
            f"{value}{suffix}"
        )


class ShareCardWidget(QWidget):

    WIDTH = 900
    HEIGHT = 1200

    def __init__(self, theme_name="Aurora"):
        super().__init__()

        self.theme_name = theme_name

        self.setObjectName("ShareCardRoot")
        self.setFixedSize(
            self.WIDTH,
            self.HEIGHT
        )

        root = QVBoxLayout(self)
        root.setContentsMargins(46, 42, 46, 38)
        root.setSpacing(22)

        # ---------- Header ----------

        header = QHBoxLayout()
        header.setSpacing(14)

        self.logo = QLabel("♫")
        self.logo.setObjectName("ShareLogo")
        self.logo.setAlignment(Qt.AlignCenter)
        self.logo.setFixedSize(54, 54)

        header_text = QVBoxLayout()
        header_text.setSpacing(0)

        self.app_title = QLabel("Spotify Power Tools")
        self.app_title.setObjectName("ShareAppTitle")

        self.generated_label = QLabel("Aurora Music Intelligence")
        self.generated_label.setObjectName("ShareGenerated")

        header_text.addWidget(self.app_title)
        header_text.addWidget(self.generated_label)

        self.playlist_label = QLabel("Unknown Playlist")
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

        hero_layout = QHBoxLayout(self.hero)
        hero_layout.setContentsMargins(28, 26, 28, 26)
        hero_layout.setSpacing(24)

        left = QVBoxLayout()
        left.setSpacing(9)

        self.eyebrow = QLabel("MY PLAYLIST PERSONALITY")
        self.eyebrow.setObjectName("ShareEyebrow")

        personality_row = QHBoxLayout()
        personality_row.setSpacing(16)

        self.personality_emoji = QLabel("✨")
        self.personality_emoji.setObjectName("SharePersonalityEmoji")

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
        left.addWidget(self.personality_subtitle)
        left.addSpacing(8)
        left.addWidget(self.recommended_profile)

        right = QVBoxLayout()
        right.setSpacing(4)

        self.aura_label = QLabel("AURA")
        self.aura_label.setObjectName("ShareAuraLabel")
        self.aura_label.setAlignment(Qt.AlignCenter)

        self.aura_score = QLabel("0")
        self.aura_score.setObjectName("ShareAuraScore")
        self.aura_score.setAlignment(Qt.AlignCenter)

        self.aura_status = QLabel("Needs Vibes")
        self.aura_status.setObjectName("ShareAuraStatus")
        self.aura_status.setAlignment(Qt.AlignCenter)

        right.addWidget(self.aura_label)
        right.addWidget(self.aura_score)
        right.addWidget(self.aura_status)

        hero_layout.addLayout(left, 2)
        hero_layout.addLayout(right, 1)

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

        # ---------- Wrapped Highlights ----------

        self.highlights_title = QLabel("Wrapped Highlights")
        self.highlights_title.setObjectName("ShareSectionTitle")

        root.addWidget(self.highlights_title)

        cards_grid = QGridLayout()
        cards_grid.setSpacing(14)

        self.top_artist_card = ShareMiniCard("Top Artist", "🎤")
        self.replayed_card = ShareMiniCard("Most Replayed", "🔁")
        self.skipped_card = ShareMiniCard("Most Skipped", "⏭️")
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
        self.badges_row.setSpacing(10)

        self.badge_labels = []

        for _ in range(4):

            badge = QLabel("✨ Fresh Start")
            badge.setObjectName("ShareBadge")
            badge.setAlignment(Qt.AlignCenter)
            badge.setWordWrap(True)
            badge.setMinimumHeight(58)

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
            theme_name
        )

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

        theme_name = theme_name or "Aurora"

        if theme_name == "Midnight":

            root_gradient = """
            qradialgradient(
                cx:0.20, cy:0.10,
                radius:1.25,
                fx:0.20, fy:0.10,
                stop:0 #312E81,
                stop:0.34 #111827,
                stop:0.72 #020617,
                stop:1 #000000
            )
            """

            hero_gradient = """
            qlineargradient(
                x1:0, y1:0,
                x2:1, y2:1,
                stop:0 #312E81,
                stop:0.46 #0F172A,
                stop:1 #020617
            )
            """

            accent = "#818CF8"
            accent_two = "#22D3EE"

        elif theme_name == "Neon Pop":

            root_gradient = """
            qradialgradient(
                cx:0.18, cy:0.10,
                radius:1.15,
                fx:0.18, fy:0.10,
                stop:0 #FB7185,
                stop:0.30 #A855F7,
                stop:0.62 #0F172A,
                stop:1 #020617
            )
            """

            hero_gradient = """
            qlineargradient(
                x1:0, y1:0,
                x2:1, y2:1,
                stop:0 #FB7185,
                stop:0.48 #A855F7,
                stop:1 #22D3EE
            )
            """

            accent = "#FB7185"
            accent_two = "#FDE68A"

        else:

            root_gradient = """
            qradialgradient(
                cx:0.14, cy:0.08,
                radius:1.15,
                fx:0.14, fy:0.08,
                stop:0 #1DB954,
                stop:0.28 #0F766E,
                stop:0.58 #111827,
                stop:1 #050509
            )
            """

            hero_gradient = """
            qlineargradient(
                x1:0, y1:0,
                x2:1, y2:1,
                stop:0 #1DB954,
                stop:0.48 #22D3EE,
                stop:1 #A855F7
            )
            """

            accent = "#1DB954"
            accent_two = "#22D3EE"

        self.setStyleSheet(f"""
        QWidget#ShareCardRoot{{
            background:{root_gradient};
        }}

        QLabel#ShareLogo{{
            background:qlineargradient(
                x1:0, y1:0,
                x2:1, y2:1,
                stop:0 {accent},
                stop:1 {accent_two}
            );
            color:#020617;
            border-radius:20px;
            font-size:24pt;
            font-weight:950;
        }}

        QLabel#ShareAppTitle{{
            color:#FFFFFF;
            font-size:24pt;
            font-weight:950;
        }}

        QLabel#ShareGenerated{{
            color:#CBD5E1;
            font-size:10.5pt;
            font-weight:750;
        }}

        QLabel#SharePlaylist{{
            color:#E0F2FE;
            font-size:12pt;
            font-weight:850;
        }}

        QFrame#ShareHero{{
            background:{hero_gradient};
            border:1px solid rgba(255,255,255,130);
            border-radius:34px;
        }}

        QLabel#ShareEyebrow{{
            color:#ECFEFF;
            font-size:10.5pt;
            font-weight:950;
            letter-spacing:2px;
        }}

        QLabel#SharePersonalityEmoji{{
            font-size:54pt;
        }}

        QLabel#SharePersonalityTitle{{
            color:#FFFFFF;
            font-size:38pt;
            font-weight:950;
        }}

        QLabel#SharePersonalitySubtitle{{
            color:#F8FAFC;
            font-size:14pt;
            font-weight:750;
        }}

        QLabel#ShareRecommended{{
            color:#020617;
            background:rgba(255,255,255,210);
            border-radius:15px;
            padding:10px 14px;
            font-size:11pt;
            font-weight:950;
        }}

        QLabel#ShareAuraLabel{{
            color:#ECFEFF;
            font-size:11pt;
            font-weight:950;
            letter-spacing:2px;
        }}

        QLabel#ShareAuraScore{{
            color:#FFFFFF;
            font-size:78pt;
            font-weight:950;
        }}

        QLabel#ShareAuraStatus{{
            color:#F8FAFC;
            font-size:15pt;
            font-weight:950;
        }}

        QFrame#ShareMetric{{
            background:rgba(255,255,255,25);
            border:1px solid rgba(255,255,255,70);
            border-radius:22px;
        }}

        QLabel#ShareMetricValue{{
            color:#FFFFFF;
            font-size:27pt;
            font-weight:950;
        }}

        QLabel#ShareMetricLabel{{
            color:#CBD5E1;
            font-size:10.5pt;
            font-weight:850;
        }}

        QLabel#ShareSectionTitle{{
            color:#FFFFFF;
            font-size:18pt;
            font-weight:950;
        }}

        QFrame#ShareMiniCard{{
            background:rgba(15,23,42,210);
            border:1px solid rgba(255,255,255,60);
            border-radius:24px;
        }}

        QLabel#ShareMiniEmoji{{
            font-size:30pt;
        }}

        QLabel#ShareMiniTitle{{
            color:{accent_two};
            font-size:10.5pt;
            font-weight:950;
            letter-spacing:1px;
        }}

        QLabel#ShareMiniValue{{
            color:#FFFFFF;
            font-size:19pt;
            font-weight:950;
        }}

        QLabel#ShareMiniSubtitle{{
            color:#CBD5E1;
            font-size:10pt;
            font-weight:700;
        }}

        QLabel#ShareBadge{{
            background:rgba(255,255,255,25);
            border:1px solid rgba(255,255,255,70);
            border-radius:18px;
            color:#FFFFFF;
            font-size:10.5pt;
            font-weight:900;
            padding:10px;
        }}

        QLabel#ShareFooter{{
            color:#CBD5E1;
            font-size:10.5pt;
            font-weight:800;
        }}
        """)

    def update_data(self, playlist, analytics):

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

        aura_score = glow.get(
            "aura_score",
            0
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
            wrapped.get("top_artist", {})
        )

        self.replayed_card.update_card(
            wrapped.get("most_replayed", {})
        )

        self.skipped_card.update_card(
            wrapped.get("most_skipped", {})
        )

        self.hidden_card.update_card(
            wrapped.get("hidden_favorite", {})
        )

        badges = glow.get(
            "badges",
            []
        )[:4]

        for index, label in enumerate(self.badge_labels):

            if index < len(badges):

                badge = badges[index]

                label.setText(
                    f"{badge.get('emoji', '✨')}  {badge.get('title', 'Badge')}"
                )

                label.show()

            else:

                label.setText("✨ Fresh Start")
                label.show()

    def save_to_png(self, file_path):

        self.ensurePolished()

        if self.layout() is not None:
            self.layout().activate()

        pixmap = QPixmap(
            self.size()
        )

        pixmap.fill(
            QColor("#050509")
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