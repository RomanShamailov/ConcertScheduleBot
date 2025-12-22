from typing import Any


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
    def __init__(self, concerts: list[dict[str, Any]]):
        self.concerts_ = concerts

    def schedule(self) -> str:
        schedule = ""
        for concert in self.concerts_:
            new_concert = "\n"
            try:
                new_concert += f"{concert['concert']['datetime']}: {concert['concert']['concertTitle']}\n"
                new_concert += f"price: {concert['minPrice']['value']}{concert['minPrice']['currency']}\n"
                new_concert += f"city: {concert['concert']['city']}\n"
            except KeyError:
                pass
            schedule += new_concert
        return schedule
