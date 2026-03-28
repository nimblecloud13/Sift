# Sift — Free Media Sorter for Windows

Sift is a fast, no-fuss media sorting tool for Windows. Open a folder of images, videos, or audio files, set up your destinations, and move through them one by one with a single keypress. Built for the moment you realize you have gigabytes of unsorted media and just need to get through it.
<img width="2556" height="1384" alt="sift_preview_image_1" src="https://github.com/user-attachments/assets/8d2e409e-afeb-4cda-b700-39f25fdad6fa" />

---

## Features

- Supports images, video, and audio
- Up to 5 custom sort destinations with keyboard shortcuts (1–5)
- Filmstrip view with video thumbnails
- Re-sort already-sorted files into a different destination at any time
- Undo last sort with **Z**
- Filter view by media type (images, video, or audio)
- Slideshow mode with fullscreen support
- Scroll-to-zoom on images and video, with click-and-drag panning when zoomed in
- Paste any folder path directly into the path box and press Enter to load
- Runs locally — no internet connection, no account, no telemetry

---

## Requirements

- Windows 10 or 11
- Python 3.10+

---

## Quick Start

### One-click install (recommended)

1. Download **[install.bat](install.bat)** from this repo
2. Double-click it
3. A shortcut will appear on your Desktop — double-click it to launch Sift

The installer will check for Python, download Sift, install all dependencies, and create a Desktop shortcut automatically.

> **Note:** Python 3.10+ is required. If you don't have it, the installer will open the download page for you. When installing Python, make sure to tick **"Add Python to PATH"**.

### Manual install

```bash
pip install -r requirements.txt
python server.py
```

---

## Keyboard Shortcuts

| Key       | Action                   |
|-----------|--------------------------|
| `1`–`5`   | Sift file to destination |
| `←` / `→` | Navigate files           |
| `Z`       | Undo last sift           |
| `Space`   | Play / pause             |
| `F`       | Toggle fullscreen        |
| `B`       | Browse for folder        |

---

## License

Free for personal, non-commercial use. See [LICENSE](LICENSE) for full terms.

For commercial licensing enquiries: [x.com/NimbleCloud13](https://x.com/NimbleCloud13)

---

Made by [NimbleCloud13](https://x.com/NimbleCloud13) · [GitHub](https://github.com/nimblecloud13) · [Reddit](https://old.reddit.com/user/Nimblecloud13/)

If you find Sift useful: [☕ Buy me a coffee](https://buymeacoffee.com/nimblecloud13)
