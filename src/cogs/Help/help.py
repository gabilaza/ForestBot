
import config
import discord
from discord.ext import commands
from utils import logs


class HelpCog(commands.Cog, name='Help'):
    def __init__(self, bot):
        self.__bot = bot

    @commands.command(aliases=['h'])
    async def help(self, ctx, *params):
        isOwner = await self.__bot.is_owner(ctx.author)
        if not params:
            emb = discord.Embed(title='Commands and modules',
                                description=f'Use `{config.COMMAND_PREFIX}h <module>` to gain more information about that module :smiley:\n')

            cogsDesc = ''
            for cogName in self.__bot.cogs:
                if cogName == 'Help':
                    continue

                cog = self.__bot.get_cog(cogName)
                if cog.cog_check(ctx):
                    cogsDesc += f'`{cogName}`\n'

            if cogsDesc:
                emb.add_field(name='Modules', value=cogsDesc, inline=False)

            commands_desc = ''
            for command in self.__bot.walk_commands():
                if not command.cog_name and (not command.hidden or isOwner):
                    commands_desc += f'{command.name} - {command.help}\n'

            if commands_desc:
                emb.add_field(name='Not belonging to a module', value=commands_desc, inline=False)

            emb.add_field(name='About', value='Maintained by {}.\n'.format(config.MAINTAINER))
            emb.set_footer(text=f'Version: {config.VERSION}')
        elif len(params) == 1:
            cogName = params[0]
            cog = self.__bot.get_cog(cogName)
            if cog:
                if cog.cog_check(ctx):
                    cogDoc = cog.description
                    emb = discord.Embed(title=f'{cogName} - commands', description=(cogDoc if cogDoc else '')+f'\n**Usage: {config.COMMAND_PREFIX}{cogName.lower()} command**')

                    for command in cog.walk_commands():
                        if not command.hidden or isOwner:
                            emb.add_field(name=f'{command.name}', value=command.help, inline=False)
                else:
                    emb = discord.Embed(title="What's that?!",
                                        description=f"This module is not available on this channel.") # TODO: specific
            else:
                emb = discord.Embed(title="What's that?!",
                                    description=f"I've never heard from a module called `{cogName}` before :scream:")
        elif len(params) > 1:
            emb = discord.Embed(title="That's too much.",
                                description="Please request only one module at once :sweat_smile:")
        else:
            emb = discord.Embed(title="It's a magical place.",
                                description="I don't know how you got here. But I didn't see this coming at all.")

        await ctx.send(embed=emb)

