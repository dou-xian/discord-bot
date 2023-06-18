import discord
from discord.ext import commands
import os
import youtube_dl
from core import Cog_Extension

class Music(Cog_Extension):
    def __init__(self, bot):
        self.bot = bot
        self.song_queue = []

    @commands.command()
    async def play(self, ctx, *, song_name):
        song_exist = os.path.isfile("song.mp3")
        try:
            if song_exist:
                os.remove("song.mp3")
        except PermissionError:
            await ctx.send("等待目前播放的音樂結束或使用 'stop' 指令。")
            return

        # 使用 youtube_dl 搜尋歌曲
        try:
            ydl_opts = {
                'format': 'bestaudio/best',
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                }],
            }
            with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(f"ytsearch:{song_name}", download=False)
                url = info['entries'][0]['webpage_url']
                await ctx.send(f"正在播放：{info['entries'][0]['title']}")
        except Exception as e:
            await ctx.send("搜尋歌曲時發生錯誤。")
            print(e)
            return

        # 下載歌曲
        try:
            ydl.download([url])
            await ctx.send("歌曲下載完成。")
        except Exception as e:
            await ctx.send("下載歌曲時發生錯誤。")
            print(e)
            return

        # 播放歌曲
        voice = discord.utils.get(self.bot.voice_clients, guild=ctx.guild)
        if voice is None:
            voice_channel = discord.utils.get(ctx.guild.voice_channels, name='General')
            await voice_channel.connect(timeout=600.0)
            voice = discord.utils.get(self.bot.voice_clients, guild=ctx.guild)

        for file in os.listdir("./"):
            if file.endswith(".mp3"):
                os.rename(file, "song.mp3")

        voice.play(discord.FFmpegPCMAudio(source="song.mp3"))

    @commands.command()
    async def leave(self, ctx):
        voice = discord.utils.get(self.bot.voice_clients, guild=ctx.guild)
        try:
            await voice.disconnect()
        except:
            await ctx.send("機器人未連接到語音頻道。")

    @commands.command()
    async def pause(self, ctx):
        voice = discord.utils.get(self.bot.voice_clients, guild=ctx.guild)
        try:
            if voice.is_playing():
                voice.pause()
            else:
                await ctx.send("目前沒有播放中的音樂。")
        except:
            await ctx.send("機器人未連接到語音頻道。")

    @commands.command()
    async def resume(self, ctx):
        voice = discord.utils.get(self.bot.voice_clients, guild=ctx.guild)
        try:
            if voice.is_paused():
                voice.resume()
            else:
                await ctx.send("音樂未暫停。")
        except:
            await ctx.send("機器人未連接到語音頻道。")

    @commands.command()
    async def stop(self, ctx):
        voice = discord.utils.get(self.bot.voice_clients, guild=ctx.guild)
        try:
            voice.stop()
        except:
            await ctx.send("機器人未連接到語音頻道。")

async def setup(bot):
    await bot.add_cog(Music(bot))
