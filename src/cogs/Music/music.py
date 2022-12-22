
import asyncio
from discord.ext import commands
from .playlist import Track, Playlist
from .ytdlinfo import YTDLInfo
from .ytdlstream import YTDLStream
from utils import logs


class MusicCog(commands.Cog, name='Music'):
    """
        Listen to music on a voice channel.
    """
    def __init__(self, bot):
        self.__bot = bot
        self.__playlists = {}

    def cog_check(self, ctx):
        return ctx.guild is not None

    def __getPlaylist(self, ctx):
        if ctx.guild.id not in self.__playlists:
            self.__playlists[ctx.guild.id] = Playlist()
        return self.__playlists[ctx.guild.id]

    @commands.group(pass_context=True, name='music', hidden=True)
    async def __groupCommands(self, ctx):
        if ctx.invoked_subcommand is None:
            helpCog = self.__bot.get_cog('Help')
            if helpCog is not None:
                await helpCog.help(ctx, 'Music')

    @__groupCommands.command(name='repeat')
    async def __playlistRepeat(self, ctx):
        """
            The repeat of the playlist.
        """
        playlist = self.__getPlaylist(ctx)

        repeatType = playlist.getRepeat().value+1
        if len(Playlist.RepeatType) <= repeatType:
            repeatType = 0
        repeatType = Playlist.RepeatType(repeatType)
        playlist.setRepeat(repeatType)

        message = str(repeatType).split('.')[-1]
        await ctx.send(f'Repeat: {message}')

    @__groupCommands.command(name='add')
    async def __playlistAddTrack(self, ctx, *, url: str):
        """
            Add a track to the playlist.
        """
        playlist = self.__getPlaylist(ctx)
        trackInfo = await YTDLInfo.get(url, loop=self.__bot.loop)
        track = Track(trackInfo.url, trackInfo.title, trackInfo.channelName, trackInfo.duration)
        playlist.addTrack(track)

        await ctx.send(f'{track} added to the playlist')

    @__groupCommands.command(name='remove')
    async def __playlistRemoveTrack(self, ctx, *, indexTrack: int):
        """
            Remove a track to the playlist.
        """
        playlist = self.__getPlaylist(ctx)
        playlist.removeTrack(indexTrack)

        await ctx.send('Track removed if existed.')

    @__groupCommands.command(name='show')
    async def __playlistShow(self, ctx):
        """
            Display the playlist.
        """
        playlist = self.__getPlaylist(ctx)

        await ctx.send(str(playlist))

    @__groupCommands.command(name='reset')
    async def __playlistReset(self, ctx):
        """
            Reset playlist.
        """
        playlist = self.__getPlaylist(ctx)
        playlist.reset()

        await ctx.send('Playlist reset.')

    async def __playlistPlaying(self, ctx, playlist, it=None):
        track = None
        try:
            track = next(it)
        except StopIteration:
            return

        player = YTDLStream.get(track.url)
        ctx.voice_client.play(player, after=lambda e: asyncio.run_coroutine_threadsafe(self.__playlistPlaying(ctx, playlist, it), self.__bot.loop))

        await ctx.send(f'Playing: {track}')

    @__groupCommands.command(name='play')
    async def __playlistPlay(self, ctx):
        """
            Listening to the playlist.
        """
        playlist = self.__getPlaylist(ctx)
        asyncio.run_coroutine_threadsafe(self.__playlistPlaying(ctx, playlist, iter(playlist)), self.__bot.loop)

    @__groupCommands.command(name='next')
    async def __playlistNextTrack(self, ctx):
        """
            Next track.
        """
        ctx.voice_client.stop()

    @__playlistPlay.before_invoke
    async def __ensureVoice(self, ctx):
        if ctx.voice_client is None:
            if ctx.author.voice:
                await ctx.author.voice.channel.connect()
            else:
                await ctx.send("You are not connected to a voice channel.")
        elif ctx.voice_client.is_playing():
            ctx.voice_client.stop()

