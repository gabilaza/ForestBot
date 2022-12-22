
import config
import discord
from discord.ext import commands
from utils import logs


class Bot(commands.Bot):
    def __init__(self, intents: discord.Intents, **kwargs):
        super().__init__(command_prefix=commands.when_mentioned_or(config.COMMAND_PREFIX), description=config.DESCRIPTION, intents=intents, **kwargs)

    async def setup_hook(self):
        self.remove_command('help')

        try:
            await self.load_extension(config.COGS_PATH)
        except Exception as exc:
            logs.error(f'Could not load cogs due to {exc.__class__.__name__}: {exc}')

    async def on_ready(self):
        logs.info(f'Logged on as {self.user} (ID: {self.user.id})')

    async def on_command_error(self, ctx, exc):
        emb = discord.Embed(title="You can't hack this :clown:",
                            description=str(exc))
        logs.error(exc)
        await ctx.send(embed=emb)


def main():
    logs.logOnTheDisk('discord')
    logs.info('Started main')

    intents = discord.Intents.default()
    intents.members = True
    intents.message_content = True
    bot = Bot(intents=intents)

    if config.TESTING:
        bot.run(config.TOKEN)
    else:
        bot.run(config.TOKEN, log_handler=None)

    logs.info('Finished main')


if __name__ == '__main__':
    main()

