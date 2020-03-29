from pytube import YouTube
import discord
from discord.ext import commands, tasks
yt = YouTube('https://www.youtube.com/watch?v=RFS5N_yAGTo')
print(yt.streams.filter(audio_codec="opus"))
#yt.streams.filter(only_audio=True).first().download()
