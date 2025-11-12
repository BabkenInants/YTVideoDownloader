import os
import yt_dlp

def download_video(url: str, output_path: str, quality: str):
    if quality == "1":
        fmt = "bestvideo[ext=mp4][vcodec*=avc1][height<=1080]+bestaudio[ext=m4a]/best[ext=mp4]"
    elif quality == "2":
        fmt = "bestvideo[ext=mp4][vcodec*=avc1][height<=720]+bestaudio[ext=m4a]/best[ext=mp4]"
    elif quality == "3":
        fmt = "bestaudio[ext=m4a]/bestaudio/best"
    else:
        fmt = "bestvideo[ext=mp4][vcodec*=avc1]+bestaudio[ext=m4a]/best[ext=mp4]"
        
    ydl_opts = {
        'outtmpl': os.path.join(output_path, '%(title)s.%(ext)s'),
        'format': fmt,
        'merge_output_format': 'mp4',
        'noplaylist': False,
        'progress_hooks': [progress_hook],
        'quiet': True,
        'no_warnings': True,
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])


def progress_hook(d):
    if d['status'] == 'downloading':
        percent = d.get('_percent_str', '').strip()
        eta = d.get('_eta_str', '').strip()
        speed = d.get('_speed_str', '').strip()
        print(f"\r📥 {percent}  ETA: {eta}  Speed: {speed}", end='', flush=True)
    elif d['status'] == 'finished':
        print("\n✅ Download Complete!, Merging Audio And Video...")

def main():
    print("=== YouTube Video Downloader ===\n")
    while True:
        url = input("🔗 Please Paste YouTube Video Link Or Type 'E' To Quit The Program: ").strip()
        if not url:
            print("❌ No Link.")
            break
        elif url.lower() == "e":
            break

        output_path = input("📂 Choose Folder To Save Files (Enter = Current Folder): ").strip() or '.'
        os.makedirs(output_path, exist_ok=True)

        print("\nChoose Quality:")
        print("1 — 1080p (Full HD)")
        print("2 — 720p (HD)")
        print("3 — Audio Only (MP3)")
        print("Enter — Auto (Best Available)")
        quality = input("👉 You Chose: ").strip()

        try:
            download_video(url, output_path, quality)
            print("\n🎉 Video Download Complete!")
        except Exception as e:
            print(f"\n❌ Error: {e}")

if __name__ == "__main__":
    main()
