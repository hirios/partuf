import requests


def downloadTorrent(MAGNETIC):
    HASH = MAGNETIC.split(':')[-1]
    url_torrent = f"https://itorrents.org/torrent/{HASH}.torrent"

    out = requests.get(url_torrent)
    with open('torrent.torrent', 'wb') as f:
        f.write(out.content)

