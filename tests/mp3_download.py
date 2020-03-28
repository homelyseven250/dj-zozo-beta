import youtube_dl
import sys


ydl_opts = {
    'format': 'bestaudio/best',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',
    }],
}


if __name__ == "__main__":
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        filenames = ["youtube.com/watch?v=RFS5N_yAGTo"]
        ydl.download(filenames)
