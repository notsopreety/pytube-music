import yt_dlp
import os
import re
import sys
from urllib.parse import urlparse, parse_qs

def print_banner():
    """Display the ASCII art banner for PyTube Music."""
    banner = """
    /$$$$$$$         /$$$$$$$$        /$$                
    | $$__  $$       |__  $$__/       | $$                
    | $$  \ $$ /$$   /$$| $$ /$$   /$$| $$$$$$$   /$$$$$$ 
    | $$$$$$$/| $$  | $$| $$| $$  | $$| $$__  $$ /$$__  $$
    | $$____/ | $$  | $$| $$| $$  | $$| $$  \ $$| $$$$$$$$
    | $$      | $$  | $$| $$| $$  | $$| $$  | $$| $$_____/
    | $$      |  $$$$$$$| $$|  $$$$$$/| $$$$$$$/|  $$$$$$$
    |__/       \____  $$|__/ \______/ |_______/  \_______/
               /$$  | $$                                  
              |  $$$$$$/                                  
               \______/                                   
    """
    print("\033[1;36m" + banner + "\033[0m")
    print("\033[1;33mWelcome to PyTube Music Downloader!\033[0m\n")

def sanitize_filename(filename):
    """Sanitize filename by removing invalid characters and trimming length."""
    filename = re.sub(r'[<>:"/\\|?*]', '', filename)
    filename = filename.replace(' ', '_')
    return filename[:200]

def get_playlist_name(url):
    """Extract playlist name from URL or metadata."""
    try:
        with yt_dlp.YoutubeDL({'quiet': True, 'no_warnings': True}) as ydl:
            info = ydl.extract_info(url, download=False)
            return sanitize_filename(info.get('title', 'Playlist'))
    except:
        return "Playlist"

def download_single_music(url, output_path, audio_format="mp3"):
    """Download a single music file."""
    try:
        ydl_opts = {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': audio_format,
                'preferredquality': 'best',
            }],
            'outtmpl': os.path.join(output_path, '%(title)s.%(ext)s'),
            'quiet': False,
            'no_warnings': True,
            'progress_hooks': [lambda d: print(f"\033[1;32mDownloading {d['filename']} ({d['_percent_str']})\033[0m")
                              if d['status'] == 'downloading' else None],
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            title = sanitize_filename(info.get('title', 'Unknown_Track'))
            filename = f"{title}.{audio_format}"
            filepath = os.path.join(output_path, filename)

            if os.path.exists(filepath):
                print(f"\033[1;33mSkipping {title}: File already exists\033[0m")
                return

            print(f"\033[1;34mStarting download: {title}\033[0m")
            ydl.download([url])
            print(f"\033[1;32mCompleted: {title}\033[0m")

    except yt_dlp.DownloadError as de:
        print(f"\033[1;31mDownload error: {str(de)}\033[0m")
    except Exception as e:
        print(f"\033[1;31mError: {str(e)}\033[0m")

def download_playlist_auto(url, output_path, audio_format="mp3"):
    """Download all songs from a playlist automatically."""
    try:
        playlist_name = get_playlist_name(url)
        playlist_path = os.path.join(output_path, playlist_name)
        os.makedirs(playlist_path, exist_ok=True)

        ydl_opts = {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': audio_format,
                'preferredquality': 'best',
            }],
            'outtmpl': os.path.join(playlist_path, '%(title)s.%(ext)s'),
            'noplaylist': False,
            'quiet': False,
            'no_warnings': True,
            'progress_hooks': [lambda d: print(f"\033[1;32mDownloading {d['filename']} ({d['_percent_str']})\033[0m")
                              if d['status'] == 'downloading' else None],
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            print(f"\033[1;34mDownloading playlist to: {playlist_path}\033[0m")
            ydl.download([url])
            print(f"\033[1;32mPlaylist download completed!\033[0m")

    except yt_dlp.DownloadError as de:
        print(f"\033[1;31mDownload error: {str(de)}\033[0m")
    except Exception as e:
        print(f"\033[1;31mError: {str(e)}\033[0m")

def download_playlist_manual(url, output_path, audio_format="mp3"):
    """Download playlist with manual song approval."""
    try:
        playlist_name = get_playlist_name(url)
        playlist_path = os.path.join(output_path, playlist_name)
        os.makedirs(playlist_path, exist_ok=True)

        ydl_opts = {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': audio_format,
                'preferredquality': 'best',
            }],
            'outtmpl': os.path.join(playlist_path, '%(title)s.%(ext)s'),
            'noplaylist': False,
            'quiet': False,
            'no_warnings': True,
            'extract_flat': 'in_playlist',
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            print(f"\033[1;34mFetching playlist info: {url}\033[0m")
            playlist_info = ydl.extract_info(url, download=False)
            
            if 'entries' not in playlist_info:
                print("\033[1;31mNo videos found in the playlist.\033[0m")
                return

            for index, entry in enumerate(playlist_info['entries'], 1):
                title = sanitize_filename(entry.get('title', f'Unknown_Track_{index}'))
                song_url = entry.get('url', '')
                print(f"\n\033[1;36mSong {index}: {title}\033[0m")
                print(f"\033[1;35mURL: {song_url}\033[0m")
                while True:
                    choice = input("\033[1;33mDownload this song? (y/n): \033[0m").strip().lower()
                    if choice in ['y', 'n']:
                        break
                    print("\033[1;31mPlease enter 'y' or 'n'.\033[0m")

                if choice == 'y':
                    single_video_opts = ydl_opts.copy()
                    single_video_opts['outtmpl'] = os.path.join(playlist_path, f"{title}.%(ext)s")
                    single_video_opts['noplaylist'] = True
                    single_video_opts.pop('extract_flat', None)

                    with yt_dlp.YoutubeDL(single_video_opts) as ydl_single:
                        print(f"\033[1;34mDownloading: {title}\033[0m")
                        ydl_single.download([song_url])
                        print(f"\033[1;32mCompleted: {title}\033[0m")
                else:
                    print(f"\033[1;33mSkipped: {title}\033[0m")

            print(f"\033[1;32mPlaylist processing completed!\033[0m")

    except yt_dlp.DownloadError as de:
        print(f"\033[1;31mDownload error: {str(de)}\033[0m")
    except Exception as e:
        print(f"\033[1;31mError: {str(e)}\033[0m")

def search_and_download(query, output_path, audio_format="mp3"):
    """Search YouTube and download selected video."""
    try:
        ydl_opts = {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': audio_format,
                'preferredquality': 'best',
            }],
            'outtmpl': os.path.join(output_path, '%(title)s.%(ext)s'),
            'quiet': False,
            'no_warnings': True,
            'default_search': 'ytsearch5',
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            print(f"\033[1;34mSearching for: {query}\033[0m")
            results = ydl.extract_info(query, download=False)
            
            if 'entries' not in results:
                print("\033[1;31mNo results found.\033[0m")
                return

            for index, entry in enumerate(results['entries'], 1):
                print(f"\033[1;36m{index}. {entry.get('title', 'Unknown Title')}\033[0m")
                print(f"\033[1;35mURL: {entry.get('webpage_url', 'Unknown URL')}\033[0m")

            while True:
                try:
                    choice = input("\033[1;33mEnter number to download (0 to skip): \033[0m").strip()
                    if choice == '0':
                        print("\033[1;33mSearch download skipped.\033[0m")
                        return
                    choice = int(choice)
                    if 1 <= choice <= len(results['entries']):
                        break
                    print("\033[1;31mInvalid selection. Enter a number between 1 and {len(results['entries'])}.\033[0m")
                except ValueError:
                    print("\033[1;31mPlease enter a valid number.\033[0m")

            selected_entry = results['entries'][choice - 1]
            title = sanitize_filename(selected_entry.get('title', 'Unknown_Track'))
            url = selected_entry.get('webpage_url', '')

            print(f"\033[1;34mDownloading: {title}\033[0m")
            download_single_music(url, output_path, audio_format)

    except yt_dlp.DownloadError as de:
        print(f"\033[1;31mDownload error: {str(de)}\033[0m")
    except Exception as e:
        print(f"\033[1;31mError: {str(e)}\033[0m")

def main():
    """Main CLI loop."""
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        print_banner()
        print("\033[1;36mOptions:\033[0m")
        print("1. Download music by music URL")
        print("2. Download playlist (auto full)")
        print("3. Download playlist (manually choose)")
        print("4. Search and download")
        print("5. Exit")

        choice = input("\033[1;33mSelect an option (1-5): \033[0m").strip()

        if choice == '5':
            print("\033[1;32mThank you for using PyTube Music! Exiting...\033[0m")
            break

        if choice not in ['1', '2', '3', '4']:
            print("\033[1;31mInvalid option. Please select 1-5.\033[0m")
            input("\033[1;33mPress Enter to continue...\033[0m")
            continue

        save_path = input("\033[1;33mEnter save directory (press Enter for current directory): \033[0m").strip() or "."
        os.makedirs(save_path, exist_ok=True)

        try:
            if choice == '1':
                url = input("\033[1;33mEnter music URL: \033[0m").strip()
                if url:
                    download_single_music(url, save_path)
            elif choice == '2':
                url = input("\033[1;33mEnter playlist URL: \033[0m").strip()
                if url:
                    download_playlist_auto(url, save_path)
            elif choice == '3':
                url = input("\033[1;33mEnter playlist URL: \033[0m").strip()
                if url:
                    download_playlist_manual(url, save_path)
            elif choice == '4':
                query = input("\033[1;33mEnter search query: \033[0m").strip()
                if query:
                    search_and_download(query, save_path)

        except KeyboardInterrupt:
            print("\n\033[1;31mOperation cancelled by user.\033[0m")
        except Exception as e:
            print(f"\033[1;31mError: {str(e)}\033[0m")

        input("\033[1;33mPress Enter to continue...\033[0m")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\033[1;32mExiting PyTube Music.\033[0m")
        sys.exit(0)