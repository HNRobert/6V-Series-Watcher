# 6V Series Watcher

![effect1](https://github.com/user-attachments/assets/25174a68-9d81-4a7d-9130-fd7d2cf8f7ac)

## Workflow:

1. Get the series info from .toml config
2. Crawl magnet urls from 6V Movie Web once/10min
3. If magnet urls not added, deliver the magnet urls to qBittorrent Client
4. The qBittorrent Client may start downloading

> Docker supported, current paths are optimised for Ugreen NAS Device

> Issues are welcomed
