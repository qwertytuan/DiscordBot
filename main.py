#!/home/tuan/.local/bin/uv run
import discord
from discord.ext import commands
import logging
from dotenv import load_dotenv
import os
import requests
import json
import random as rand
import uuid
import yt_dlp
load_dotenv()

token = os.getenv('DISCORD_TOKEN')
trigger_webhook_url = os.getenv('TRIGGER_WEBHOOK')
chat_webhook_url = os.getenv('CHAT_WEBHOOK')
channel_id = int(os.getenv('CHANNEL_ID'))
def is_in_channel(ctx):
    return ctx.channel.id == channel_id

# test api
handler = logging.FileHandler(filename='discord.log', encoding='utf-8',mode='w')
intents = discord.Intents.default()
intents.message_content = True 
intents.members = True

bot = commands.Bot(command_prefix='!@',intents=intents)
roleDefault = "Admin(fake)"
roleAdmin = "Hội đồng tối cao"

@bot.event
async def on_ready():
    print(f"Bot name: {bot.user.name}")
    print(f"Bot id: {bot.user.id}")

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    if "dm" in message.content.lower():
        print("===========")
        print(f"on_message command, channel id: {message.channel.id}")
        print(f"userName: {message.author.name}")
        print("===========")
        await message.channel.send(f"HI: {message.author.mention}")
    await bot.process_commands(message)

@bot.command()
async def ping(ctx):
    latency = bot.latency * 100
    print("===========")
    print(f"ping command, channel id: {ctx.channel.id}")
    print(f"userName: {ctx.author.name}")
    print("===========")
    await ctx.reply(f"Pong: {latency:.2f}ms.")

@bot.command()
async def hello(ctx):
    print("===========")
    print(f"hello command, channel id: {ctx.channel.id}")
    print(f"userName: {ctx.author.name}")
    print("===========")
    await ctx.reply(f"Hello to you too {ctx.author.mention}")

@bot.command()
@commands.check(is_in_channel)
async def trigger(ctx):
    if ctx.author == bot.user:
        return
    try:
        print("===========")
        print(f"trigger command, channel id: {ctx.channel.id}")
        print(f"userName: {ctx.author.name}")
        print("===========")
        headers = {
            "Accept": "application/json",
            "X-HTTP-Method-Override": "PUT"
        }
        data = {"userId": str(ctx.author.id)}
        print(f"payload:{data}")
        print(f"userId: {ctx.author.id}")
        response = requests.post(trigger_webhook_url, headers=headers, data=data)
        #await ctx.reply(f"Success,sent dm to {ctx.author.mention}")
        print(f"Response status: {response.status_code}")
        print(f"Response body: {response.text}")
        await ctx.reply(f"Success,sent dm to {ctx.author.mention}")
    except Exception as e:
        print(f'Error sending webhook: {e}')
        await ctx.reply('Sorry, there was an error triggering the webhook.')

@trigger.error
async def trigger_error(ctx,error):
    if isinstance(error,commands.CheckFailure):
        channelName = bot.get_channel(channel_id)
        await ctx.send(f"Phai chay trong kenh {channelName.name}")

@bot.command()
@commands.has_role(roleAdmin)
async def assign(ctx):
    print("===========")
    print(f"assign command, channel id: {ctx.channel.id}")
    print(f"userName: {ctx.author.name}")
    print("===========")
    role = discord.utils.get(ctx.guild.roles,name=roleDefault)
    if role:
        await ctx.author.add_roles(role)
        await ctx.reply(f"{ctx.author.mention} co role {roleDefault}")
    else:
        await ctx.reply("Role ko ton tai")

@assign.error
async def assign_error(ctx,error):
    if isinstance(error,commands.MissingRole):
        await ctx.reply(f"Ko co role {roleAdmin} de chay lenh")

@bot.command()
@commands.has_role(roleAdmin)
async def remove(ctx):
    print("===========")
    print(f"remove command, channel id: {ctx.channel.id}")
    print(f"userName: {ctx.author.name}")
    print("===========")
    role = discord.utils.get(ctx.guild.roles,name=roleDefault)
    if role:
        await ctx.author.remove_roles(role)
        await ctx.reply(f"{ctx.author.mention} khong co role {roleDefault} nua")
    else:
        await ctx.reply("Role ko ton tai")

@remove.error
async def remove_error(ctx,error):
    if isinstance(error,commands.MissingRole):
        await ctx.reply(f"Ko co role {roleAdmin} de chay lenh")

@bot.command()
@commands.has_role(roleDefault)
async def secret(ctx):
    print("===========")
    print(f"secret command, channel id: {ctx.channel.id}")
    print(f"userName: {ctx.author.name}")
    print("===========")
    await ctx.reply(f"Gui cho nhung nguoi co role {roleDefault}")

@secret.error
async def secret_error(ctx,error):
    if isinstance(error,commands.MissingRole):
        await ctx.reply(f"Ko co role {roleDefault} de chay lenh")

@bot.command()
async def random(ctx,int1,int2):
    try:
        int1 = int(int1)
        int2 = int(int2)
    except Exception as e:
        await ctx.reply(f"Ca 2 bien phai deu la so!!")
        return
    if int1 >= int2:
        await ctx.reply(f"So 1 phai nho hon so 2")
    else:
        await ctx.reply(f"So ngau nhien tu {int1} den {int2} la: {rand.randint(int1,int2)}")
    print(f"===========")
    print(f"random command, channel id: {ctx.channel.id}")
    print(f"userName: {ctx.author.name}")

@bot.command()
async def play(ctx,url):
    voiceChannel = ctx.author.voice.channel
    if voiceChannel is None:
        await ctx.reply("Phai o trong kenh voice")
        return
    
    if ctx.voice_client is None:
        vc = await voiceChannel.connect()
    else:
        vc = ctx.voice_client
        if vc.channel != voiceChannel:
            await vc.move_to(voiceChannel)

    try:
        ffmpegOptions = {'before_options': '-reconnect 1 -reconnect_streamed 0 -reconnect_delay_max 5', 'options': '-vn'}
        ydl_opts = {
        'format': 'bestaudio/best',  # Download the best audio format
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',  # Convert to MP3
            'preferredquality': '192',
        }]}
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            songInfo = ydl.extract_info(url,download=False)
        
        print(songInfo["url"])
        source = discord.FFmpegPCMAudio(songInfo["url"], **ffmpegOptions)
        
        def after_play(error):
            if error:
                print(f'Player error: {error}')
            bot.loop.create_task(vc.disconnect())

        vc.play(source, after=after_play)

    except Exception as e:
        print(f"Error playing song: {e}")
        await ctx.reply("There was an error playing the song.")
        if vc.is_connected():
            await vc.disconnect()
            
@bot.command()
@commands.check(is_in_channel)
async def chat(ctx,message):
    if ctx.author == bot.user:
        return
    try:
        print("===========")
        print(f"chat command, channel id: {ctx.channel.id}")
        print(f"userName: {ctx.author.name}")
        print("===========")
        headers = {
            "Accept": "application/json",
            "X-HTTP-Method-Override": "PUT"
        }
        sessionId = uuid.uuid4()
        data = {"sessionId": str(sessionId),"userId": str(ctx.author.id),"userName": str(ctx.author.name), "message": str(message)}
        print(f"payload:{data}")
        print(f"userId: {ctx.author.id}")
        response = requests.post(chat_webhook_url, headers=headers, data=data)
        print(f"Response status: {response.status_code}")
        print(f"Response body: {response.text}")
        await ctx.reply("Success")
    except Exception as e:
        print(f'Error sending webhook: {e}')
        await ctx.reply('Sorry, there was an error triggering the webhook.')
    
bot.run(token, log_handler=handler,log_level=logging.DEBUG)
