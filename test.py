import yt_dlp
import random
id = random.randint(1,10)
name = f'{id}.%(ext)s'
ydl_opts = {
        'format': 'bestaudio/best',  # Download the best audio format
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',  # Convert to MP3
            'preferredquality': '192',
        }],
        'outtmpl': name,  # Output file name template
    }

    # Example usage to download a video and convert to MP3
with yt_dlp.YoutubeDL(ydl_opts) as ydl:
    ydl.download(['https://www.youtube.com/watch?v=dQw4w9WgXcQ'])
    print(name)
