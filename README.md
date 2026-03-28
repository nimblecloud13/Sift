# Sift — Free Media Sorter for Windows

Sift is a fast, no-fuss media sorting tool for Windows. Open a folder of images, videos, or audio files, set up your destinations, and move through them one by one with a single keypress. Built for the moment you realize you have gigabytes of unsorted media and just need to get through it.

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

1. Clone or download this repository
2. Double-click **run.bat**

`run.bat` will install dependencies automatically on first run, then launch Sift. Your browser will open to `http://localhost:7432`.

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
