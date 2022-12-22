
import sys
import inspect
from utils import logs


## Cogs imports

from .Help import HelpCog
from .Channel import ChannelCog
from .Music import MusicCog
from .SecretSanta import SecretSantaCog

########


async def setup(bot):
    # Get all classes that are imported on this python file
    cogs = inspect.getmembers(sys.modules[__name__], inspect.isclass)
    logs.debug(cogs)

    for cogName, cogObject in cogs:
        logs.info(f'Loading {cogName} from {cogObject}')
        await bot.add_cog(cogObject(bot))

