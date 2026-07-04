from PySide6.QtWidgets import (
    QLabel,
    QFrame,
    QVBoxLayout,
    QHBoxLayout,
    QGridLayout,
    QProgressBar,
)

from PySide6.QtCore import Qt, QPropertyAnimation, QEasingCurve


class GlowMetric(QFrame):

    def __init__(self, title):
        super().__init__()

        self.setObjectName("GlowMetric")

        layout = QVBoxLayout(self)
        layout.setContentsMargins(14, 12, 14, 12)
        layout.setSpacing(7)

        self.title_label = QLabel(title)
        self.title_label.setObjectName("GlowMetricTitle")

        self.value_label = QLabel("0%")
        self.value_label.setObjectName("GlowMetricValue")

        self.progress = QProgressBar()
        self.progress.setObjectName("GlowMetricProgress")
        self.progress.setRange(0, 100)
        self.progress.setValue(0)
        self.progress.setTextVisible(False)
        self.progress.setFixedHeight(9)
        self.animation = None

        layout.addWidget(
            self.title_label
        )

        layout.addWidget(
            self.value_label
        )

        layout.addWidget(
            self.progress
        )

    def animate_to(self, target_value):

        if self.animation is not None:
            self.animation.stop()

        self.animation = QPropertyAnimation(
            self.progress,
            b"value",
            self
        )

        self.animation.setDuration(
            450
        )

        self.animation.setStartValue(
            self.progress.value()
        )

        self.animation.setEndValue(
            target_value
        )

        self.animation.setEasingCurve(
            QEasingCurve.OutCubic
        )

        self.animation.start()

    def update_value(self, value):

        if value is None:
            value = 0

        value = round(
            float(value),
            1
        )

        self.value_label.setText(
            f"{value}%"
        )

        self.animate_to(
            int(max(0, min(100, round(value))))
        )

class AnalyticsHeroCard(QFrame):

    def __init__(self):
        super().__init__()

        self.setObjectName("AnalyticsHeroCard")
        self.setMinimumHeight(360)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(28, 26, 28, 26)
        layout.setSpacing(18)

        top_row = QHBoxLayout()
        top_row.setSpacing(24)

        left = QVBoxLayout()
        left.setSpacing(8)

        self.eyebrow = QLabel("YOUR PLAYLIST PERSONALITY")
        self.eyebrow.setObjectName("HeroEyebrow")

        title_row = QHBoxLayout()
        title_row.setSpacing(14)

        self.emoji_label = QLabel("✨")
        self.emoji_label.setObjectName("HeroEmoji")

        self.personality_label = QLabel("Main Character Mix")
        self.personality_label.setObjectName("HeroPersonality")
        self.personality_label.setWordWrap(True)

        title_row.addWidget(
            self.emoji_label
        )

        title_row.addWidget(
            self.personality_label,
            1
        )

        self.subtitle_label = QLabel(
            "Balanced vibes with enough personality to keep it moving."
        )
        self.subtitle_label.setObjectName("HeroSubtitle")
        self.subtitle_label.setWordWrap(True)

        self.recommended_label = QLabel("Recommended Profile: Balanced")
        self.recommended_label.setObjectName("HeroRecommended")

        left.addWidget(
            self.eyebrow
        )

        left.addLayout(
            title_row
        )

        left.addWidget(
            self.subtitle_label
        )

        left.addSpacing(8)

        left.addWidget(
            self.recommended_label
        )

        right = QVBoxLayout()
        right.setSpacing(4)

        self.aura_title = QLabel("AURA SCORE")
        self.aura_title.setObjectName("AuraTitle")
        self.aura_title.setAlignment(Qt.AlignCenter)

        self.aura_number = QLabel("0")
        self.aura_number.setObjectName("AuraNumber")
        self.aura_number.setAlignment(Qt.AlignCenter)

        self.aura_status = QLabel("No Data Yet")
        self.aura_status.setObjectName("AuraStatus")
        self.aura_status.setAlignment(Qt.AlignCenter)

        self.aura_progress = QProgressBar()
        self.aura_progress.setObjectName("AuraProgress")
        self.aura_progress.setRange(0, 100)
        self.aura_progress.setValue(0)
        self.aura_progress.setTextVisible(False)
        self.aura_progress.setFixedHeight(12)
        self.aura_animation = None

        right.addWidget(
            self.aura_title
        )

        right.addWidget(
            self.aura_number
        )

        right.addWidget(
            self.aura_status
        )

        right.addSpacing(10)

        right.addWidget(
            self.aura_progress
        )

        top_row.addLayout(
            left,
            2
        )

        top_row.addLayout(
            right,
            1
        )

        metric_grid = QGridLayout()
        metric_grid.setSpacing(14)

        self.taste_metric = GlowMetric("Taste Match")
        self.variety_metric = GlowMetric("Variety")
        self.replay_metric = GlowMetric("Replay Energy")

        metric_grid.addWidget(
            self.taste_metric,
            0,
            0
        )

        metric_grid.addWidget(
            self.variety_metric,
            0,
            1
        )

        metric_grid.addWidget(
            self.replay_metric,
            0,
            2
        )

        layout.addLayout(
            top_row
        )

        layout.addLayout(
            metric_grid
        )

    def animate_aura_to(self, target_value):

        if self.aura_animation is not None:
            self.aura_animation.stop()

        self.aura_animation = QPropertyAnimation(
            self.aura_progress,
            b"value",
            self
        )

        self.aura_animation.setDuration(
            650
        )

        self.aura_animation.setStartValue(
            self.aura_progress.value()
        )

        self.aura_animation.setEndValue(
            target_value
        )

        self.aura_animation.setEasingCurve(
            QEasingCurve.OutCubic
        )

        self.aura_animation.start()

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

    def update_glow(self, glow, intelligence):

        personality = glow.get(
            "personality",
            {}
        )

        aura_score = glow.get(
            "aura_score",
            0
        )

        self.emoji_label.setText(
            personality.get("emoji", "✨")
        )

        self.personality_label.setText(
            personality.get("title", "Main Character Mix")
        )

        self.subtitle_label.setText(
            personality.get(
                "subtitle",
                "Balanced vibes with enough personality to keep it moving."
            )
        )

        recommended_profile = intelligence.get(
            "recommended_profile",
            "Balanced"
        )

        confidence = intelligence.get(
            "recommendation_confidence",
            "Low"
        )

        self.recommended_label.setText(
            f"Recommended Profile: {recommended_profile} • {confidence} Confidence"
        )

        self.aura_number.setText(
            str(round(aura_score))
        )

        self.aura_status.setText(
            self.get_aura_status(
                aura_score
            )
        )

        self.animate_aura_to(
            int(max(0, min(100, round(aura_score))))
        )

        self.taste_metric.update_value(
            glow.get("taste_match", 0)
        )

        self.variety_metric.update_value(
            glow.get("variety_score", 0)
        )

        self.replay_metric.update_value(
            glow.get("replay_energy", 0)
        )