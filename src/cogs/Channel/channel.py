

import discord
from discord.ext import commands
from utils import logs

class ChannelCog(commands.Cog, name='Channel'):
    """
        Connecting and disconnecting from the voice channel.
    """
    def __init__(self, bot):
        self.__bot = bot

    def cog_check(self, ctx):
        return ctx.guild is not None

    @commands.group(pass_context=True, name='channel', hidden=True)
    async def __groupCommands(self, ctx):
        if ctx.invoked_subcommand is None:
            helpCog = self.__bot.get_cog('Help')
            if helpCog is not None:
                await helpCog.help(ctx, 'Channel')

    @__groupCommands.command(name='join')
    async def __joinChannel(self, ctx, *, channel: discord.VoiceChannel):
        """
            Connecting to a voice channel.
        """
        if ctx.voice_client is None:
            await channel.connect()
        else:
            await ctx.voice_client.move_to(channel)

    @__groupCommands.command(name='leave')
    async def __leaveChannel(self, ctx):
        """
            Disconnecting from a voice channel.
        """
        await ctx.voice_client.disconnect()

