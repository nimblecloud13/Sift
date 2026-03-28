"""
Sift server — Flask backend for sift.html
Run with:  python server.py
"""
import os
import sys
import shutil
import subprocess
import threading
import webbrowser
from pathlib import Path
from flask import Flask, jsonify, request, send_from_directory, send_file

app = Flask(__name__)

src_folder: str = ""          # absolute path selected by user

IMAGE_EXTS = {
    ".jpg", ".jpeg", ".png", ".gif", ".webp", ".bmp",
    ".tiff", ".tif", ".avif", ".heic", ".heif", ".ico", ".svg",
}
VIDEO_EXTS = {
    ".mp4", ".webm", ".mov", ".avi", ".mkv", ".ogv", ".m4v",
    ".3gp", ".wmv", ".flv", ".mpeg", ".mpg",
}
AUDIO_EXTS = {
    ".mp3", ".wav", ".ogg", ".m4a", ".flac", ".aac", ".opus", ".wma", ".aif", ".aiff",
}

MEDIA_EXTS = IMAGE_EXTS | VIDEO_EXTS | AUDIO_EXTS

PORT = 7432


def _resource(rel_path: str) -> Path:
    """Resolve a bundled resource path — works both frozen (PyInstaller) and from source."""
    base = Path(sys._MEIPASS) if getattr(sys, "frozen", False) else Path(__file__).parent
    return base / rel_path


# ─── Serve the UI ────────────────────────────────────────────────────────────

@app.route("/")
def index():
    return send_file(_resource("sift.html"))

@app.route("/logo.png")
def serve_logo():
    p = _resource("logo.png")
    if not p.exists():
        return "", 404
    return send_file(p)

@app.route("/nimblecloud.png")
def serve_nimblecloud():
    p = _resource("nimblecloud.png")
    if not p.exists():
        return "", 404
    return send_file(p)


# ─── Native folder picker (spawns subprocess so tkinter runs in main thread) ─

@app.route("/api/browse", methods=["POST"])
def browse():
    script = (
        "import tkinter as tk\n"
        "from tkinter import filedialog\n"
        "root = tk.Tk()\n"
        "root.withdraw()\n"
        "root.attributes('-topmost', True)\n"
        "path = filedialog.askdirectory(title='Select media folder')\n"
        "root.destroy()\n"
        "print(path or '', end='')\n"
    )
    try:
        result = subprocess.run(
            [sys.executable, "-c", script],
            capture_output=True, text=True, timeout=120,
        )
        path = result.stdout.strip()
        return jsonify({"path": path})
    except Exception as e:
        return jsonify({"path": "", "error": str(e)})


# ─── Open / scan folder ───────────────────────────────────────────────────────

@app.route("/api/open", methods=["POST"])
def api_open():
    global src_folder
    data = request.get_json(force=True)
    path = (data or {}).get("path", "").strip()
    if not path or not os.path.isdir(path):
        return jsonify({"error": f"Folder not found: {path}"}), 400
    src_folder = os.path.abspath(path)
    return jsonify(_scan())


@app.route("/api/files")
def api_files():
    return jsonify(_scan())


def _scan() -> dict:
    if not src_folder or not os.path.isdir(src_folder):
        return {"files": [], "folder": ""}

    entries = []
    try:
        names = sorted(os.listdir(src_folder), key=lambda n: n.lower())
    except PermissionError as e:
        return {"files": [], "folder": src_folder, "error": str(e)}

    for name in names:
        full = os.path.join(src_folder, name)
        if not os.path.isfile(full):
            continue
        ext = os.path.splitext(name)[1].lower()
        if ext not in MEDIA_EXTS:
            continue
        if ext in IMAGE_EXTS:
            media_type = "image"
        elif ext in VIDEO_EXTS:
            media_type = "video"
        else:
            media_type = "audio"
        entries.append({
            "name": name,
            "type": media_type,
            "size": os.path.getsize(full),
        })
    return {"files": entries, "folder": src_folder}


# ─── Sort (move) a file ───────────────────────────────────────────────────────

@app.route("/api/sort", methods=["POST"])
def api_sort():
    global src_folder
    if not src_folder:
        return jsonify({"error": "No folder open"}), 400

    data = request.get_json(force=True) or {}
    filename      = data.get("filename",      "").strip()
    dest_name     = data.get("folder",        "").strip()
    src_subfolder = data.get("src_subfolder", "").strip()

    if not filename or not dest_name:
        return jsonify({"error": "Missing filename or folder"}), 400

    # Prevent path traversal
    if ".." in filename or ".." in dest_name or ".." in src_subfolder:
        return jsonify({"error": "Invalid path"}), 400

    src_path = os.path.join(src_folder, src_subfolder, filename) if src_subfolder else os.path.join(src_folder, filename)
    if not os.path.isfile(src_path):
        return jsonify({"error": f"File not found: {filename}"}), 404

    dest_dir = os.path.join(src_folder, dest_name)
    os.makedirs(dest_dir, exist_ok=True)

    dest_path = os.path.join(dest_dir, filename)

    # Resolve name collision
    if os.path.exists(dest_path):
        base, ext = os.path.splitext(filename)
        n = 1
        while os.path.exists(dest_path):
            dest_path = os.path.join(dest_dir, f"{base}_{n}{ext}")
            n += 1

    shutil.move(src_path, dest_path)
    return jsonify({"ok": True, "dest_name": os.path.basename(dest_path)})


# ─── Undo: move a file from a subfolder back to source ───────────────────────

@app.route("/api/undo", methods=["POST"])
def api_undo():
    global src_folder
    if not src_folder:
        return jsonify({"error": "No folder open"}), 400

    data = request.get_json(force=True) or {}
    folder_name  = data.get("folder",    "").strip()   # subfolder it lives in
    dest_name    = data.get("dest_name", "").strip()   # actual filename in subfolder
    orig_name    = data.get("orig_name", "").strip()   # original name to restore as

    if not folder_name or not dest_name or not orig_name:
        return jsonify({"error": "Missing parameters"}), 400

    for part in (folder_name, dest_name, orig_name):
        if ".." in part:
            return jsonify({"error": "Invalid path"}), 400

    src_path = os.path.join(src_folder, folder_name, dest_name)
    if not os.path.isfile(src_path):
        return jsonify({"error": f"File not found in {folder_name}/"}), 404

    restore_path = os.path.join(src_folder, orig_name)
    if os.path.exists(restore_path):
        base, ext = os.path.splitext(orig_name)
        n = 1
        while os.path.exists(restore_path):
            restore_path = os.path.join(src_folder, f"{base}_{n}{ext}")
            n += 1

    shutil.move(src_path, restore_path)
    return jsonify({"ok": True, "restored_name": os.path.basename(restore_path)})


# ─── Serve media files (supports HTTP Range for video seeking) ───────────────

@app.route("/media/<path:filename>")
def serve_media(filename):
    if not src_folder:
        return "No folder open", 404
    # Security: resolve and confirm the file is inside src_folder
    try:
        target = Path(src_folder) / filename
        target.resolve().relative_to(Path(src_folder).resolve())
    except ValueError:
        return "Forbidden", 403
    return send_from_directory(src_folder, filename, conditional=True)


# ─── Entry point ─────────────────────────────────────────────────────────────

if __name__ == "__main__":
    url = f"http://localhost:{PORT}"

    import logging
    logging.getLogger("werkzeug").setLevel(logging.ERROR)

    # Flask in a background daemon thread
    flask_thread = threading.Thread(
        target=lambda: app.run(
            host="127.0.0.1", port=PORT,
            debug=False, threaded=True, use_reloader=False,
        ),
        daemon=True,
    )
    flask_thread.start()

    # Open browser after a short delay
    threading.Timer(0.8, lambda: webbrowser.open(url)).start()

    try:
        import pystray
        import tkinter as tk
        from PIL import Image as PILImage, ImageTk

        icon_path = _resource("logo.png")
        pil_img = (
            PILImage.open(icon_path)
            if icon_path.exists()
            else PILImage.new("RGB", (64, 64), (255, 153, 0))
        )

        # ── Shared quit ───────────────────────────────────────────
        def quit_all():
            try: tray.stop()
            except: pass
            os._exit(0)

        def open_browser(icon=None, item=None):
            webbrowser.open(url)

        # ── System tray icon (runs in its own thread) ─────────────
        tray = pystray.Icon(
            "Sift", pil_img.resize((64, 64)), "Sift",
            menu=pystray.Menu(
                pystray.MenuItem("Open Sift", open_browser, default=True),
                pystray.MenuItem("Quit",      lambda i, m: quit_all()),
            ),
        )
        tray.run_detached()

        # ── Tkinter window (taskbar presence) ─────────────────────
        # Tell Windows this is its own app (not pythonw) so taskbar icon is ours
        try:
            import ctypes
            ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID("sift.mediasort.app")
        except Exception:
            pass

        root = tk.Tk()
        root.title("Sift")
        root.geometry("300x90")
        root.resizable(False, False)
        root.configure(bg="#1a1a1a")

        # iconbitmap() is what Windows actually uses for the taskbar icon
        import tempfile
        _ico = Path(tempfile.gettempdir()) / "sift_icon.ico"
        pil_img.resize((32, 32)).save(str(_ico), format="ICO")
        root.iconbitmap(str(_ico))

        photo = ImageTk.PhotoImage(pil_img.resize((32, 32)))
        root.iconphoto(True, photo)

        ABOUT_TEXT = (
            "Sift  —  Free Media Sorter for Windows\n"
            "─────────────────────────────────────────\n\n"
            "A free media sorter for Windows, for the moment when you realize you have "
            "gigabytes of images, audio, or videos that you created sitting unsorted on "
            "your hard drive, and you just need to go through it fast and move the keepers "
            "somewhere.\n\n"
            "It happened to me, so I built Sift.\n\n"
            "I'm sharing it freely because I wouldn't have gotten this far without so much "
            "free support and assistance from others. No bloat, no subscription, no learning "
            "curve.\n\n"
            "If you like my work, and only if you can afford to, my family and I would truly "
            "appreciate your support!\nhttps://buymeacoffee.com/nimblecloud13\n\n"
            "Keep creating, and have a great day!\n\n"
            "- Nimble\n\n"
            "─────────────────────────────────────────\n"
            "Copyright © 2026 NimbleCloud13. All rights reserved.\n"
            "Free for personal, non-commercial use only.\n"
            "See LICENSE file for full terms."
        )

        def show_about():
            win = tk.Toplevel(root)
            win.title("About Sift")
            win.geometry("480x380")
            win.resizable(False, False)
            win.configure(bg="#1a1a1a")
            win.grab_set()
            try: win.iconbitmap(str(_ico))
            except: pass

            txt = tk.Text(win, bg="#1a1a1a", fg="#d4d4d4", font=("Segoe UI", 9),
                          wrap="word", relief="flat", padx=18, pady=14,
                          bd=0, highlightthickness=0, cursor="arrow")
            txt.insert("1.0", ABOUT_TEXT)
            txt.config(state="disabled")
            txt.pack(fill="both", expand=True)

            tk.Button(win, text="Close", command=win.destroy,
                      bg="#2c2c2c", fg="#d4d4d4", font=("Segoe UI", 10),
                      relief="flat", padx=16, pady=4, cursor="hand2").pack(pady=(0, 12))

        tk.Label(root, text="Sift is running",
                 bg="#1a1a1a", fg="#d4d4d4",
                 font=("Segoe UI", 11)).pack(pady=(14, 8))

        btn_frame = tk.Frame(root, bg="#1a1a1a")
        btn_frame.pack()
        tk.Button(btn_frame, text="Open", command=open_browser,
                  bg="#ff9900", fg="#000", font=("Segoe UI", 10, "bold"),
                  relief="flat", padx=16, pady=4, cursor="hand2").pack(side="left", padx=5)
        tk.Button(btn_frame, text="About", command=show_about,
                  bg="#2c2c2c", fg="#d4d4d4", font=("Segoe UI", 10),
                  relief="flat", padx=12, pady=4, cursor="hand2").pack(side="left", padx=5)
        tk.Button(btn_frame, text="Quit", command=quit_all,
                  bg="#2c2c2c", fg="#d4d4d4", font=("Segoe UI", 10),
                  relief="flat", padx=16, pady=4, cursor="hand2").pack(side="left", padx=5)

        root.protocol("WM_DELETE_WINDOW", quit_all)
        root.iconify()   # start minimized — shows as taskbar button
        root.mainloop()

    except ImportError:
        # Fallback: plain terminal mode (pystray/pillow not installed)
        print(f"\n  Sift running → {url}\n  Press Ctrl+C to stop.\n")
        try:
            flask_thread.join()
        except KeyboardInterrupt:
            pass
