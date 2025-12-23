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
    def __init__(self, concerts):
        self.concerts_ = concerts

    def schedule(self) -> str:
        lines = ["Список концертов"]

        for concert in self.concerts_:
            try:
                dt = datetime.fromisoformat(concert["concert"]["datetime"])
                title = concert["concert"]["concertTitle"]
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
                            f"🎤 {title}",
                            f"🌍 {city}",
                            f"💵 {price_block}",
                        ]
                    )
                )
            except KeyError:
                continue

        return "\n\n".join(lines) if lines else "Концерты не найдены"
