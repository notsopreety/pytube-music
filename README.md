# PyTube Music Downloader

A powerful and user-friendly command-line interface (CLI) tool for downloading music from YouTube videos and playlists. Built with `yt-dlp`, PyTube Music offers a robust set of features for downloading high-quality audio with a sleek ASCII interface and flexible options.

## Features

- **Download Single Tracks**: Download audio from a single YouTube video URL.
- **Playlist Download (Auto)**: Automatically download all tracks in a playlist, saving them in a dedicated folder named after the playlist.
- **Playlist Download (Manual)**: Manually approve or skip each track in a playlist, with song titles and URLs displayed for review.
- **Search and Download**: Search YouTube for music and select from the top results to download.
- **High-Quality Audio**: Downloads the best available audio quality, with support for MP3 format.
- **Filename Sanitization**: Ensures safe, clean filenames by removing invalid characters and replacing spaces with underscores.
- **Progress Feedback**: Real-time download progress with percentage updates and colored CLI output.
- **Error Handling**: Robust error handling for invalid URLs, network issues, and file conflicts.
- **Cross-Platform**: Works on Windows, macOS, and Linux.

## Installation

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/notsopreety/pytube-music.git
   cd pytube-music
   ```

2. **Install Python**:
   Ensure Python 3.6 or higher is installed. You can download it from [python.org](https://www.python.org/downloads/).

3. **Install Dependencies**:
   Install the required Python packages using pip:
   ```bash
   pip install yt-dlp
   ```

4. **Install FFmpeg**:
   FFmpeg is required for audio extraction. Install it based on your operating system:
   - **Windows**: Download from [FFmpeg website](https://ffmpeg.org/download.html) or install via a package manager like Chocolatey (`choco install ffmpeg`).
   - **macOS**: Install via Homebrew (`brew install ffmpeg`).
   - **Linux**: Install via your package manager (e.g., `sudo apt install ffmpeg` for Ubuntu).

## Usage

Run the script using Python:
```bash
python run.py
```

The CLI displays an ASCII banner and a menu with the following options:
1. Download music by music URL
2. Download playlist (auto full)
3. Download playlist (manually choose)
4. Search and download
5. Exit

### Examples

- **Download a Single Track**:
  Select option 1, enter a YouTube video URL (e.g., `https://www.youtube.com/watch?v=example`), and specify a save directory (or press Enter for the current directory).

- **Download a Playlist Automatically**:
  Select option 2, enter a playlist URL (e.g., `https://www.youtube.com/playlist?list=example`), and the tool will create a folder named after the playlist and download all tracks.

- **Download a Playlist with Manual Approval**:
  Select option 3, enter a playlist URL, and approve or skip each track after reviewing its title and URL.

- **Search and Download**:
  Select option 4, enter a search query (e.g., `lofi hip hop`), choose a result from the top 5, and download the selected track.

### Notes
- Files are saved with the track title as the filename (e.g., `Song_Title.mp3`).
- The tool skips existing files to prevent overwrites.
- Press `Ctrl+C` to cancel operations or exit the program gracefully.

## Requirements

- Python 3.6+
- yt-dlp (`pip install yt-dlp`)
- FFmpeg (installed and accessible in your system PATH)

## Contributing

Contributions are welcome! To contribute:
1. Fork the repository.
2. Create a new branch (`git checkout -b feature/your-feature`).
3. Make your changes and commit (`git commit -m "Add your feature"`).
4. Push to your branch (`git push origin feature/your-feature`).
5. Open a pull request.

Please ensure your code follows PEP 8 style guidelines and includes appropriate tests.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Disclaimer

This tool is for personal use only. Ensure you have the right to download and use the content as per YouTube's terms of service and applicable copyright laws.

## Acknowledgments

- Built with [yt-dlp](https://github.com/yt-dlp/yt-dlp), a powerful YouTube downloader.
- Inspired by the need for a simple, feature-rich CLI music downloader.

Happy downloading with PyTube Music! 🎵