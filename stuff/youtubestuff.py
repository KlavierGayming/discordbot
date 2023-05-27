import asyncio
import discord
import yt_dlp as youtube_dl
from yt_dlp import YoutubeDL
from typing import List
ytdl_format_options = {
    'format': 'bestaudio/best',
    'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0',  # bind to ipv4 since ipv6 addresses cause issues sometimes
    'chunk_size': 2_000_000,
    'max_simultaneous_chunk_downloads': 8
}

ffmpeg_options = {
    'options': '-vn',
    "before_options": "-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5"
}
ytdl = youtube_dl.YoutubeDL(ytdl_format_options)


class YTDLSource(discord.PCMVolumeTransformer):
    def __init__(self, source, *, data, volume=1):
        super().__init__(source, volume)

        self.data = data

        self.title = data.get('title')
        self.url = data.get('url')
        self.yturl = data.get("webpage_url")


    @classmethod
    async def play(cls, url, *, loop=None, stream=False):
        loop = loop or asyncio.get_event_loop()
        try:
            data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=not stream))
        except:
            data = await loop.run_in_executor(None, lambda: ytdl.extract_info(f"ytsearch:{url}", download=not stream))
        else:
            data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=not stream))
        if 'entries' in data:
            # take first item from a playlist
            data = data['entries'][0]

        filename = data['url'] if stream else ytdl.prepare_filename(data)
        return cls(discord.FFmpegPCMAudio(filename, **ffmpeg_options), data=data)
    
    @classmethod
    async def getmetadata(cls, searchquery) -> List:
        with YoutubeDL(ytdl_format_options) as ydl:
            try:
                video = ydl.extract_info(searchquery, download=False)['entries'][0]
            except:
                video = ydl.extract_info(f"ytsearch:{searchquery}", download=False)['entries'][0]
            else:
                video = ydl.extract_info(f"ytsearch:{searchquery}", download=False)['entries'][0]
            
            if searchquery.startswith("https://www.youtube.com/watch?v="):
                video["webpage_url"] = searchquery
        return video
    @classmethod
    async def geturl(cls, searchquery) -> List:
        with YoutubeDL(ytdl_format_options) as ydl:
            try:
                video = ydl.extract_info(searchquery, download=False)
            except:
                video = ydl.extract_info(f"ytsearch:{searchquery}", download=False)['entries'][0]
            else:
                video = ydl.extract_info(f"ytsearch:{searchquery}", download=False)['entries'][0]
            
            if searchquery.startswith("https://www.youtube.com/watch?v="):
                video["webpage_url"] = searchquery
        return video["webpage_url"]