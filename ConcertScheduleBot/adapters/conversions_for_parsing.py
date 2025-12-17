class UrlTemplates:
    TEMPLATES: list[str] = [
        ('https://music.yandex.ru/playlists/', 'https://api.music.yandex.ru/playlist/'),
        ('https://music.yandex.ru/users/', 'https://api.music.yandex.ru/users/'),
    ]


class PlaylistUrlToApiConvertor:

    def __init__(self, url: str) -> None:
        self.url_: str = url

    def api_url(self) -> str | None:
        for url_template, api_template in UrlTemplates.TEMPLATES:
            if self.url_.startswith(url_template):
                return api_template + self.url_[len(url_template):]
        return None
