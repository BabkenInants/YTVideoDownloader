import os
import threading
import tkinter as tk
from tkinter import ttk, messagebox
import subprocess
import platform
from pathlib import Path
import yt_dlp

# Default folders
BASE_DIR = Path.home() / "Downloads" / "YTDownloader"
VIDEO_DIR = BASE_DIR / "Videos"
AUDIO_DIR = BASE_DIR / "Audios"
VIDEO_DIR.mkdir(parents=True, exist_ok=True)
AUDIO_DIR.mkdir(parents=True, exist_ok=True)

class DownloadTask:
    def __init__(self, url, quality, type_, tree_item):
        self.url = url
        self.quality = quality
        self.type = type_
        self.tree_item = tree_item
        self.thread = None
        self.ydl = None
        self.stop_flag = False

class YTDownloaderGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("YT Downloader Tracker")
        self.root.geometry("1000x600")
        self.root.minsize(900, 500)

        # Top frame for buttons
        top_frame = tk.Frame(root, padx=10, pady=10)
        top_frame.pack(fill=tk.X)
        tk.Button(top_frame, text="New Download", command=self.new_download).pack(side=tk.LEFT)

        # Treeview for downloads
        tree_frame = tk.Frame(root, padx=10, pady=5)
        tree_frame.pack(fill=tk.BOTH, expand=True)

        columns = ("Name", "Type", "Progress", "Speed", "Status")
        self.tree = ttk.Treeview(tree_frame, columns=columns, show="headings", selectmode="browse")
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=180, anchor="w")
        self.tree.pack(fill=tk.BOTH, expand=True)

        # Right-click menu
        self.menu = tk.Menu(root, tearoff=0)
        self.menu.add_command(label="Pause", command=lambda: self.control_download("pause"))
        self.menu.add_command(label="Resume", command=lambda: self.control_download("resume"))
        self.menu.add_command(label="Stop", command=lambda: self.control_download("stop"))
        self.menu.add_command(label="Delete", command=lambda: self.control_download("delete"))
        self.menu.add_command(label="Open Folder", command=lambda: self.control_download("open"))
        self.tree.bind("<Button-3>", self.show_menu)

        self.downloads = []

    def new_download(self):
        dialog = tk.Toplevel(self.root)
        dialog.title("New Download")
        dialog.geometry("550x300")  # larger to fit everything
        dialog.resizable(False, False)
        dialog.grab_set()  # modal

        # URL Label & Entry with border
        tk.Label(dialog, text="YouTube URL:").pack(pady=(10, 2))
        url_entry = tk.Entry(dialog, width=65, bd=2, relief="sunken")  # added border
        url_entry.pack(pady=(0, 10))

        # Type
        tk.Label(dialog, text="Type:").pack(pady=(5, 2))
        type_var = tk.StringVar(value="video")
        type_frame = tk.Frame(dialog)
        type_frame.pack(pady=(0, 10))
        tk.Radiobutton(type_frame, text="Video", variable=type_var, value="video").pack(side=tk.LEFT, padx=10)
        tk.Radiobutton(type_frame, text="Audio (MP3)", variable=type_var, value="audio").pack(side=tk.LEFT, padx=10)

        # Quality
        tk.Label(dialog, text="Quality:").pack(pady=(5, 2))
        quality_var = tk.StringVar(value="best")
        quality_frame = tk.Frame(dialog)
        quality_frame.pack(pady=(0, 10))
        qualities = [("1080p", "1080"), ("720p", "720"), ("Audio/Auto", "best")]
        for text, val in qualities:
            tk.Radiobutton(quality_frame, text=text, variable=quality_var, value=val).pack(side=tk.LEFT, padx=10)

        # Start button (now properly visible)
        start_btn = tk.Button(dialog, text="Start Download", command=lambda: start_download())
        start_btn.pack(pady=10, ipadx=10, ipady=5)

        def start_download():
            url = url_entry.get().strip()
            if not url:
                messagebox.showerror("Error", "Please enter a URL")
                return
            type_ = type_var.get()
            quality = quality_var.get()
            tree_item = self.tree.insert("", tk.END, values=("Pending...", type_, "0%", "", "Queued"))
            task = DownloadTask(url, quality, type_, tree_item)
            self.downloads.append(task)
            task.thread = threading.Thread(target=self.download_worker, args=(task,))
            task.thread.start()
            dialog.destroy()

    def show_menu(self, event):
        selected = self.tree.selection()
        if not selected:
            return
        self.menu.post(event.x_root, event.y_root)

    def control_download(self, action):
        selected = self.tree.selection()
        if not selected:
            return
        tree_id = selected[0]
        task = next((t for t in self.downloads if t.tree_item == tree_id), None)
        if not task:
            return

        import subprocess
        if action == "pause":
            if task.ydl:
                task.stop_flag = True
                self.tree.set(task.tree_item, 4, "Paused")
        elif action == "resume":
            if task.stop_flag:
                task.stop_flag = False
                task.thread = threading.Thread(target=self.download_worker, args=(task,))
                task.thread.start()
                self.tree.set(task.tree_item, 4, "Resumed")
        elif action == "stop":
            task.stop_flag = True
            self.tree.set(task.tree_item, 4, "Stopped")
        elif action == "delete":
            task.stop_flag = True
            self.tree.delete(task.tree_item)
            self.downloads.remove(task)
        elif action == "open":
            folder = VIDEO_DIR if task.type == "video" else AUDIO_DIR
            if platform.system() == "Darwin":
                subprocess.call(["open", folder])
            elif platform.system() == "Windows":
                os.startfile(folder)

    def download_worker(self, task: DownloadTask):
        output_path = VIDEO_DIR if task.type=="video" else AUDIO_DIR
        if task.type=="video":
            format_opt = {
                "1080": "bestvideo[ext=mp4][vcodec*=avc1][height<=1080]+bestaudio[ext=m4a]/best[ext=mp4]",
                "720": "bestvideo[ext=mp4][vcodec*=avc1][height<=720]+bestaudio[ext=m4a]/best[ext=mp4]",
                "best": "bestvideo[ext=mp4]+bestaudio[ext=m4a]/bestvideo+bestaudio/best"
            }.get(task.quality, "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]")
            ydl_opts = {
                "outtmpl": os.path.join(output_path, "%(title)s.%(ext)s"),
                "format": format_opt,
                "noplaylist": False,
                "quiet": True,
                "no_warnings": True,
                "progress_hooks": [lambda d: self.progress_hook(d, task)]
            }
        else:
            ydl_opts = {
                "outtmpl": os.path.join(output_path, "%(title)s.%(ext)s"),
                "format": "bestaudio/best",
                "postprocessors": [{"key":"FFmpegExtractAudio","preferredcodec":"mp3","preferredquality":"192"}],
                "quiet": True,
                "no_warnings": True,
                "progress_hooks": [lambda d: self.progress_hook(d, task)]
            }
        try:
            task.ydl = yt_dlp.YoutubeDL(ydl_opts)
            info = task.ydl.extract_info(task.url, download=True)
            self.tree.set(task.tree_item, 0, info.get('title', 'Unknown'))
            self.tree.set(task.tree_item, 4, "Completed")
        except Exception as e:
            self.tree.set(task.tree_item, 4, f"Error: {e}")

    def progress_hook(self, d, task: DownloadTask):
        if task.stop_flag:
            raise yt_dlp.utils.DownloadError("Stopped by user")
        if d["status"]=="downloading":
            self.tree.set(task.tree_item, 2, d.get("_percent_str","0%"))
            self.tree.set(task.tree_item, 3, d.get("_speed_str",""))
            self.tree.set(task.tree_item, 4, "Downloading")
        elif d["status"]=="finished":
            self.tree.set(task.tree_item, 2, "100%")
            self.tree.set(task.tree_item, 4, "Merging/Completed")


if __name__=="__main__":
    root = tk.Tk()
    app = YTDownloaderGUI(root)
    root.mainloop()