from __future__ import unicode_literals
import discord
import random
import os
from discord.ext import commands, tasks
from itertools import cycle
import urllib.request
from bs4 import BeautifulSoup
import youtube_dl

client = commands.Bot(command_prefix = '.')
status = cycle(['Mixing Cool Tunes','Remember that', 'you can', 'request songs!'])

@client.event
async def on_ready():
    change_status.start()
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
async def song(ctx, *, name):
    song_channel = client.get_channel(692569906935365672)
    radio_channel = client.get_channel(692944719965192242)
    await discord.VoiceChannel.connect(radio_channel, timeout=60.0, reconnect=True)
    textToSearch = f'{name} clean'
    query = urllib.parse.quote(textToSearch)
    url = "https://www.youtube.com/results?search_query=" + query
    response = urllib.request.urlopen(url)
    html = response.read()
    soup = BeautifulSoup(html, 'html.parser')
    urls = []
    for vid in soup.findAll(attrs={'class':'yt-uix-tile-link'}):
        urls.append('https://www.youtube.com' + vid['href'])
   




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


@tasks.loop(seconds=10)
async def change_status():
    await client.change_presence(activity=discord.Game(next(status)))


client.run('NjkzMjk0MTQ1MjQ2MDY4NzY2.Xn6_lA.KvGrdRpl4h38ZMUCa1Z4nWcVnak')