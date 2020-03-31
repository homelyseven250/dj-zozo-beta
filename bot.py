from __future__ import unicode_literals
import discord
import random
import os
from discord.ext import commands, tasks
from itertools import cycle
import urllib.request
from bs4 import BeautifulSoup
from pytube import YouTube
import pickle
import glob
import pydub
import asyncio

client = commands.Bot(command_prefix = '$')
status = cycle(['Mixing Cool Tunes','Remember that', 'you can', 'request songs!'])

@client.event
async def on_ready():
    print('Bot is ready.')

@client.event
async def on_member_join(member):
    print(f'{member} has joined the server. Welcome to the party!')

@client.event
async def on_member_remove(member):
    print(f'{member} has left the server)')

@client.command
async def ping(self, ctx):
        await ctx.send(f'Pong! {round(client.latency * 1000)}ms')


@client.command(aliases=['8ball'])
async def _8ball(ctx, *, question):
    responses = ['It is certain.',
                 'It is decidedly so.',
                 'Without a doubt.',
                 'Yes - definitely.',
                 'You may rely on it.',                  
                 'As I see it, yes.',
                 'Most likely.',
                 'Outlook good.',
                 'Yes.',
                 'Signs point to yes.',
                 'Reply hazy, try again.',
                 'Ask again later.',
                 'Better not tell you now.',
                 'Cannot predict now.',
                 'Concentrate and ask again.',
                 'Don\'t count on it.',
                 'My reply is no.',
                 'My sources say no.',
                 'Outlook not so good.',
                 'Very doubtful.']
    await ctx.send(f'Question: {question}\nAnswer: {random.choice(responses)}')







@client.command()
async def clear(ctx, amount=5):
    await ctx.channel.purge(limit=amount+1)

@client.command()
async def kick(ctx, member : discord.Member, *, reason=None):
    await member.kick(reason=reason)
    await ctx.send(f'Kicked {member.mention}')

@client.command()
async def ban(ctx, member : discord.Member, *, reason=None):
    await member.ban(reason=reason)
    await ctx.send(f'Banned {member.mention}')

@client.command()
async def unban(ctx,* , member):
    banned_users = await ctx.guild.bans()
    member_name, member_discriminator = member.split('#')
    for banned_entry in banned_users:
        user = banned_entry.user
        if (user.name, user.discriminator) == (member_name, member_discriminator):
            await ctx.guild.unban(user)
            await ctx.send(f'Unbanned {user.mention}')
            return



def next_in_queue(error):
    global vc
    queue_file = open("queue", "rb")
    current_q = pickle.load(queue_file)
    queue_file.close()
    if current_q != []:
        next_song=current_q.pop(0)
        queue_file = open("queue", "wb")
        pickle.dump(current_q, queue_file)
        queue_file.close()
        song_no_async(next_song)
        



@client.command()
async def song(ctx, *, name):
    #connect to voice channel
    global vc
    voice_channel = client.get_channel(692944719965192242)
    if ctx.voice_client is None:
        vc = await voice_channel.connect()
    else:
        await ctx.voice_client.move_to(voice_channel)
        vc = ctx.voice_client 
    song_no_async(name)

def song_no_async(name):
    global vc
    #check if music is playing
    if vc.is_playing() == False:
        # generate id
        song_id_file = open("song_counter", "rb")
        song_id = pickle.load(song_id_file)
        song_id_file.close()
        song_id_file = open("song_counter", "wb")
        pickle.dump(song_id+1, song_id_file)
        song_id_file.close()
        #locate on yt
        textToSearch = f'{name} clean'
        query = urllib.parse.quote(textToSearch)
        url = "https://www.youtube.com/results?search_query=" + query
        response = urllib.request.urlopen(url)
        html = response.read()
        soup = BeautifulSoup(html, 'html.parser')
        urls = []
        for vid in soup.findAll(attrs={'class':'yt-uix-tile-link'}):
            urls.append('https://www.youtube.com' + vid['href'])
        endurl=urls[0]

        yt = YouTube(endurl)
        #download opus stream and convert to mp3
        yt.streams.filter(audio_codec="opus").first().download(filename=str(song_id))
        pydub.AudioSegment.from_file("./"+str(song_id)+".webm").export("./"+str(song_id)+".mp3", format="mp3")   

        
        audio_source = discord.FFmpegPCMAudio(str(song_id)+".mp3")
        vc.play(audio_source,after=next_in_queue)
        #await client.change_presence(activity=discord.Game(yt.title))
        print(f'Now playing: {yt.title}')
        #await asyncio.sleep(5)
    else:
        queue_file = open("queue", "rb")
        current_q = pickle.load(queue_file)
        queue_file.close()
        queue_file = open("queue", "wb")
        current_q.append(name)
        pickle.dump(current_q, queue_file)
        queue_file.close()

@client.command()
async def pause(ctx):
    global vc
    voice_channel = client.get_channel(692944719965192242)
    if ctx.voice_client is None:
        vc = await voice_channel.connect()
    else:
        await ctx.voice_client.move_to(voice_channel)
        vc = ctx.voice_client 
    
    vc.pause()
    ctx.send(f'Music paused')

@client.command()
async def resume(ctx):
    global vc
    voice_channel = client.get_channel(692944719965192242)
    if ctx.voice_client is None:
        vc = await voice_channel.connect()
    else:
        await ctx.voice_client.move_to(voice_channel)
        vc = ctx.voice_client 
    vc.resume()
    ctx.send(f'Music resumed')


client.run('NjkzMjk0MTQ1MjQ2MDY4NzY2.Xn6_lA.KvGrdRpl4h38ZMUCa1Z4nWcVnak')