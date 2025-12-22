import asyncio
from .infrastructure.start_for_test import start

if __name__ == "__main__":
    # url = 'https://music.yandex.ru/playlists/lk.1f789547-5715-4a9a-bf78-52c503d9b208'
    url = "https://music.yandex.ru/playlists/ps.6dfdcc04-515a-41dd-aefc-ab5267c4dbe0"
    # url = 'https://music.yandex.ru/users/jakovlew.c/playlists/1151?ref_id=3AE37147-6DCA-40D9-9D02-E3737916230F&utm_medium=copy_link'
    asyncio.run(start(url))
