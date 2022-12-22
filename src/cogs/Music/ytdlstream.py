
import discord


ffmpeg_options = {
    'options': '-vn'
}


class YTDLStream(discord.PCMVolumeTransformer):
    def __init__(self, source, *, volume=0.5):
        super().__init__(source, volume)

    @classmethod
    def get(cls, url):
        return cls(discord.FFmpegPCMAudio(url, **ffmpeg_options))

