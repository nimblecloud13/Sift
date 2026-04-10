# Sift. Free Media Sorter for Windows

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
- **Strip Metadata.** Duplicate any folder with embedded metadata removed from every file (images via Pillow, video/audio via ffmpeg)
- Slideshow mode with fullscreen support
- Scroll-to-zoom on images and video, with click-and-drag panning when zoomed in
- Paste any folder path directly into the path box and press Enter to load
- Runs locally. No internet connection, no account, no telemetry

## Additional Features

- **Strip Metadata.** Duplicate any folder with GPS tags, camera info, timestamps, and other personally identifying metadata scrubbed from every file. Original folder is untouched. Images are cleaned instantly. Video/audio files require ffmpeg. Sift will offer to install it automatically if needed, or you can skip those files
- **Grid view.** See all loaded images at once in a full-window grid. Adjustable column count, click any image to jump to it, optional autoscroll with speed control
- **Slideshow mode.** Auto-advance through files at an adjustable interval. Pair with fullscreen for a gallery experience
- **Display on Launch.** Choose whether Sift reopens your last folder on startup or opens blank
- **Light and dark mode.** Toggle between themes from the controls panel. Preference is remembered across sessions
- **Copy Path.** One-click copy of the current file's full path to the clipboard

---

## Requirements

- Windows 10 or 11
- Python 3.10+

---

## Quick Start

### One-click install (recommended)

1. Download **[install.bat](install.bat)** from this repo
2. Double-click it
3. A shortcut will appear on your Desktop. Double-click it to launch Sift

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
