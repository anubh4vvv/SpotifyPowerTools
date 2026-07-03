from PySide6.QtWidgets import QLabel

from gui.card import Card


class ListeningAnalyticsCard(Card):

    def __init__(self):
        super().__init__("Listening Analytics")

        self.setMinimumHeight(430)

        self.summary_label = QLabel("No listening memory yet.")
        self.summary_label.setWordWrap(True)
        self.summary_label.setStyleSheet(
            "color:#FFFFFF; font-size:12pt; font-weight:800;"
        )

        self.details_label = QLabel("")
        self.details_label.setWordWrap(True)
        self.details_label.setStyleSheet(
            "color:#DADADA; font-size:10.5pt;"
        )

        self.layout.addWidget(
            self.summary_label
        )

        self.layout.addSpacing(8)

        self.layout.addWidget(
            self.details_label
        )

    def format_items(self, title, items, value_key=None, suffix=""):

        lines = [
            title
        ]

        if not items:
            lines.append(
                "  No data yet."
            )
            return lines

        for index, item in enumerate(
            items,
            start=1
        ):

            if value_key is None:

                lines.append(
                    (
                        f"  {index}. {item['song_name']} — {item['artist']}"
                    )
                )

            else:

                lines.append(
                    (
                        f"  {index}. {item['song_name']} — {item['artist']} "
                        f"({item[value_key]}{suffix})"
                    )
                )

        return lines

    def format_streaks(self, streaks):

        return [
            "Listening Streaks:",
            f"  Finished streak: {streaks.get('finished_streak', 0)} songs",
            f"  Skip streak: {streaks.get('skip_streak', 0)} songs",
            (
                f"  Artist streak: {streaks.get('artist_streak_name', 'N/A')} "
                f"x{streaks.get('artist_streak_count', 0)}"
            ),
            (
                f"  Album streak: {streaks.get('album_streak_name', 'N/A')} "
                f"x{streaks.get('album_streak_count', 0)}"
            ),
        ]

    def update_listening_analytics(self, data):

        total_known_songs = data.get(
            "total_known_songs",
            0
        )

        total_plays = data.get(
            "total_plays",
            0
        )

        total_replays = data.get(
            "total_replays",
            0
        )

        completion_rate = data.get(
            "global_completion_rate",
            0
        )

        skip_rate = data.get(
            "global_skip_rate",
            0
        )

        self.summary_label.setText(
            (
                f"{total_known_songs} remembered songs • "
                f"{total_plays} plays • "
                f"{total_replays} replays • "
                f"{completion_rate}% completion • "
                f"{skip_rate}% skip rate"
            )
        )

        lines = []

        lines.extend(
            self.format_streaks(
                data.get("streaks", {})
            )
        )

        lines.append("")

        lines.extend(
            self.format_items(
                "Recently Played:",
                data.get("recently_played", []),
                None
            )
        )

        lines.append("")

        lines.extend(
            self.format_items(
                "Recently Skipped:",
                data.get("recently_skipped", []),
                None
            )
        )

        lines.append("")

        lines.extend(
            self.format_items(
                "Recently Finished:",
                data.get("recently_finished", []),
                None
            )
        )

        lines.append("")

        lines.extend(
            self.format_items(
                "Recently Replayed:",
                data.get("recently_replayed", []),
                None
            )
        )

        lines.append("")

        lines.extend(
            self.format_items(
                "Most Replayed:",
                data.get("most_replayed", []),
                "replay_count",
                " replays"
            )
        )

        lines.append("")

        lines.extend(
            self.format_items(
                "Most Skipped:",
                data.get("most_skipped", []),
                "skip_count",
                " skips"
            )
        )

        lines.append("")

        lines.extend(
            self.format_items(
                "Best Completion Rate:",
                data.get("best_completion", []),
                "completion_rate",
                "%"
            )
        )

        lines.append("")

        lines.extend(
            self.format_items(
                "Worst Skip Rate:",
                data.get("worst_skip_rate", []),
                "skip_rate",
                "%"
            )
        )

        self.details_label.setText(
            "\n".join(lines)
        )