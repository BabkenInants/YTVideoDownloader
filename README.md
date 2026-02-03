# YTVideoDownloader

Mostly vibe coded YouTube Video & Audio Downloader with GUI, built in Python with Tkinter and yt-dlp.
Supports parallel downloads, MP3 audio conversion, and per-download management (pause, resume, stop, delete, open folder). Works on Windows and macOS.

# Features
•	Download videos (1080p, 720p) <br>
•	Download audio only (converted to MP3) <br>
•	Parallel downloads with progress tracking <br>
•	UI with status, speed, and progress <br>
•	Right-click per-download menu: <br>
•	Pause / Resume <br>
•	Stop <br>
•	Delete <br>
•	Open folder <br>
•	Default download folders: <br>
•	Videos: ~/Downloads/YTDownloader/Videos <br>
•	Audio: ~/Downloads/YTDownloader/Audios

# Dependencies
•	Python 3.10+ (for development) <br>
•	Tkinter (built-in with Python on most systems) <br>
•	yt-dlp (pip install yt-dlp) <br>
•	ffmpeg (for audio conversion and video merging) <br>

# Installation (Development)
1.  Clone the repository:
```
git clone https://github.com/BabkenInants/YTDownloader.git
cd YTDownloader
```

2.	Create a virtual environment and activate it:
```
python3 -m venv .venv
source .venv/bin/activate  # macOS/Linux
.venv\Scripts\activate     # Windows
```

3.	Install dependencies:
```
pip install yt-dlp
```

4.	Ensure ffmpeg is installed and accessible in your PATH:
```
ffmpeg -version
```

# Running the App
```
python main.py
```
•	Click New Download to start a video or audio download. <br>
•	Paste the YouTube URL, select type (video/audio), choose quality, and click Start Download. <br>
•	Right-click on any download in the table to pause, resume, stop, delete, or open its folder. <br>

# Default Folders
•	Videos: ~/Downloads/YTDownloader/Videos <br>
•	Audio (MP3): ~/Downloads/YTDownloader/Audios <br>

These folders are created automatically if they do not exist.

# Notes
•	Pause/Resume: The “Pause” button stops the current thread; “Resume” restarts the download using yt-dlp’s resume support. <br>
•	Cross-platform: Tested only on macOS. <br>
•	ffmpeg: Required for merging video/audio and converting audio to MP3. <br>

# License

MIT License – feel free to use, modify, and distribute.
