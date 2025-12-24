from typing import Any
from datetime import datetime


class UrlTemplates:
    TEMPLATES: list[str] = [
        ("https://music.yandex.ru/playlists/", "https://api.music.yandex.ru/playlist/"),
        ("https://music.yandex.ru/users/", "https://api.music.yandex.ru/users/"),
    ]


class PlaylistUrlToApiConvertor:
    def __init__(self, url: str) -> None:
        self.url_: str = url

    def api_url(self) -> str | None:
        for url_template, api_template in UrlTemplates.TEMPLATES:
            if self.url_.startswith(url_template):
                return api_template + self.url_[len(url_template) :]
        return None


class TracksToArtistsIdsConvertor:
    def __init__(self, tracks: list[dict[str, Any]]):
        self.tracks_: list[dict[str, Any]] = tracks

    def artists_ids(self) -> set[int]:
        artists_ids: set[int] = set()
        for track in self.tracks_:
            for artist in track["artists"]:
                artists_ids.add(artist["id"])
        return artists_ids


class ConcertsToScheduleConvertor:
    def __init__(
        self,
        concerts: list[dict[str, Any]],
        similar_concerts: list[dict[str, Any]] | None = None,
    ):
        self.concerts_ = concerts
        self.similar_concerts_ = similar_concerts

    def _format_section(
        self, concerts: list[dict[str, Any]], title: str
    ) -> list[str]:
        lines: list[str] = []

        for concert in concerts:
            try:
                dt = datetime.fromisoformat(concert["concert"]["datetime"])
                concert_title = concert["concert"]["concertTitle"]
                city = concert["concert"]["city"]

                price_block = "Цена: неизвестна"
                if "minPrice" in concert:
                    price_block = (
                        f"Цена: {concert['minPrice']['value']} "
                        f"{concert['minPrice']['currency']}"
                    )

                lines.append(
                    "\n".join(
                        [
                            f"🕒 {dt:%d.%m.%Y %H:%M}",
                            f"🎤 {concert_title}",
                            f"🌍 {city}",
                            f"💵 {price_block}",
                        ]
                    )
                )
            except KeyError:
                continue

        if lines:
            return [title] + lines
        return []

    def schedule(self) -> str:
        sections: list[str] = []

        main_section = self._format_section(
            self.concerts_, "🎵 Концерты артистов из плейлиста"
        )
        if main_section:
            sections.append("\n\n".join(main_section))

        if self.similar_concerts_:
            similar_section = self._format_section(
                self.similar_concerts_, "✨ Вам может понравиться"
            )
            if similar_section:
                sections.append("\n\n".join(similar_section))

        if sections:
            separator = "\n\n" + "═" * 35 + "\n\n"
            return separator.join(sections)
        return "Концерты не найдены"
