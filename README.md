# 6V Series Watcher

![effect1](https://github.com/user-attachments/assets/25174a68-9d81-4a7d-9130-fd7d2cf8f7ac)

## Workflow

1. Get the series info from .toml config
2. Crawl magnet urls from 6V Movie Web once/10min
3. If magnet urls not added, deliver the magnet urls to qBittorrent Client
4. The qBittorrent Client may start downloading

**_Docker supported, and current path mappings in docker-compose are optimised for UGREEN NAS Devices_**

## Installation & Setup

### Docker Installation (Recommended)

1. Prepare the Repo **OR** Docker image:

   **Repo**

   ```bash
   git clone https://github.com/HNRobert/6V-Series-Watcher.git
   cd 6V-Series-Watcher
   ```

   **Pull Docker image**

   ```bash
   docker pull ghcr.io/hnrobert/6v-series-watcher:latest
   ```

2. Edit Environment variables and directory mappings:

   - Approach 1: Create a `.env` file in the root directory of the project:

   ```env
   # qBittorrent connection details Example
   QB_HOST=http://qbittorrent:8888
   QB_USERNAME=admin
   QB_PASSWORD=adminadmin
   ```

   - Approach 2: Edit the `docker-compose.yml` file directly:

   ```yaml
   environment:
     - QB_HOST=http://qbittorrent:8888
     - QB_USERNAME=admin
     - QB_PASSWORD=adminadmin
     - QB_VERIFY_CERT=False
     - LOG_FILE=/var/log/6v_watcher/app.log
   ```

3. Set the directory mapping for the logs and config files in the `docker-compose.yml` for easy access:

   ```yaml
   volumes:
     # Mount config directory for easy config updates
     - /volume2/docker/6v-series-watcher/config:/app/config
     - /volume2/docker/6v-series-watcher/logs:/var/log/6v_watcher
   ```

4. Configure your series in `config/auto_download.toml`:

   ```toml
   # 6V-Series-Watcher Auto Download Configuration Example

   [[auto_download_items]]
   name = "The.Last.of.Us.S02"
   url = "https://www.hao6v.me/mj/2023-01-16/41138.html"

   # Add more series like this:
   # [[auto_download_items]]
   # name = "Another.Show"
   # url = "https://example.com/show"

   # You may delete the items safely if it's already added to the qBittorrent client.
   ```

5. Start the containers:

   ```bash
   docker-compose up -d
   ```

   > Tip: The auto_download configs are mounted to the host machine, so you can edit them directly without needing to rebuild or restart the container.

## Configuration Options

### TOML Configuration File Format

```toml
[[auto_download_items]]
name = "Show.Name"       # Name of the show (used for categories in qBittorrent)
url = "https://url-to-6v-page"  # URL to the 6V page containing magnets
```

### Environment Variables

| Variable       | Description             | Example                     |
| -------------- | ----------------------- | --------------------------- |
| QB_HOST        | qBittorrent WebUI URL   | <http://localhost:8888>     |
| QB_USERNAME    | qBittorrent username    | admin                       |
| QB_PASSWORD    | qBittorrent password    | adminadmin                  |
| QB_VERIFY_CERT | Verify SSL certificates | False                       |
| LOG_FILE       | Path to log file        | /var/log/6v_watcher/app.log |

## Logging

The application logs to:

- Console (standard output)
- File (configured by LOG_FILE environment variable)

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
