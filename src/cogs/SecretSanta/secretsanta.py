
import time
import copy
import random
from discord.ext import commands
from utils import logs


class SecretSantaCog(commands.Cog, name='SecretSanta'):
    """
        Secret Santa is a Western Christmas tradition in which members of a group or community are randomly assigned a person to whom they give a gift. The identity of the gift giver is to remain a **secret** and should not be revealed.
        The distribution is done uniformly (each person has the same probability of being assigned to another person).
    """
    def __init__(self, bot):
        self.__bot = bot
        self.__isOpen = False
        self.__participants = dict()
        self.__giftToParticipants = None

    def cog_check(self, ctx):
        return ctx.guild is None

    @commands.group(pass_context=True, name='secretsanta', hidden=True)
    async def __groupCommands(self, ctx):
        if ctx.invoked_subcommand is None:
            helpCog = self.__bot.get_cog('Help')
            if helpCog is not None:
                await helpCog.help(ctx, 'SecretSanta')

    @__groupCommands.command(name='register')
    async def __registerParticipant(self, ctx, *params):
        """
            Register at Secret Santa.
        """
        if self.__isOpen:
            self.__participants[ctx.author.id] = ' '.join(params)
            await ctx.send(f'Registered as {self.__participants[ctx.author.id]}.')
        else:
            await ctx.send('The event is now closed.')

    @__groupCommands.command(name='unregister')
    async def __unregisterParticipant(self, ctx, *params):
        """
            Unregister from Secret Santa.
        """
        if self.__isOpen:
            await ctx.send(f'Bye {self.__participants[ctx.author.id]} :wave:. Maybe next year.')
            self.__participants.pop(ctx.author.id, None)
        else:
            await ctx.send('The event is now closed.')

    @__groupCommands.command(name='account')
    async def __articipantAccount(self, ctx):
        """
            View registrated name.
        """
        if ctx.author.id in self.__participants:
            await ctx.send(f'Registered as {self.__participants[ctx.author.id]}.')
        else:
            await ctx.send('You are not registered.')

    @__groupCommands.command(name='assigned')
    async def __assignedPerson(self, ctx):
        """
            The person assigned to you.
        """
        if ctx.author.id in self.__participants:
            if self.__isOpen:
                await ctx.send('You cannot see the assigned person because the event has not ended.')
            elif self.__giftToParticipants is None:
                await ctx.send('The event is closed. Now Santa is thinking about distribution.')
            else:
                await ctx.send('The person is ...')
                time.sleep(2)
                await ctx.send('||'+self.__giftToParticipants[ctx.author.id]+'||')
        else:
            await ctx.send('You must be registered.')

    @__groupCommands.command(name='event')
    async def __isOpen(self, ctx):
        """
            Check if the event is open.
        """
        if self.__isOpen:
            await ctx.send('The event is open.')
        else:
            await ctx.send('The event is closed.')

    @__groupCommands.command(name='open', hidden=True)
    @commands.is_owner()
    async def __open(self, ctx):
        """
            Open the event.
        """
        if self.__isOpen:
            await ctx.send('It is opened already.')
        else:
            self.__isOpen = True
            await ctx.send('The event has started.')

    @__groupCommands.command(name='close', hidden=True)
    @commands.is_owner()
    async def __close(self, ctx):
        """
            Close the event.
        """
        if self.__isOpen:
            if len(self.__participants) > 1:
                self.__isOpen = False
                await ctx.send('The event has ended.')
            else:
                await ctx.send('The number of participants is small and you cannot close the event.')
        else:
            await ctx.send('The event is already closed.')

    @__groupCommands.command(name='reset', hidden=True)
    @commands.is_owner()
    async def __reset(self, ctx):
        """
            Reset the event.
        """
        self.__isOpen = False
        self.__participants = dict()
        self.__giftToParticipants = None
        await ctx.send('The event has reset.')

    @staticmethod
    def __uniformShuffle(array):
        arr = copy.deepcopy(array)
        n = len(arr)
        for i in range(n):
            j = random.randint(i, n - 1)
            arr[i], arr[j] = arr[j], arr[i]
        return arr

    @__groupCommands.command(name='distribute', hidden=True)
    @commands.is_owner()
    async def __distributeGifts(self, ctx):
        """
            Distribution of gifts.
        """
        if not self.__isOpen:
            if len(self.__participants) > 1:
                participants = list(self.__participants.keys())
                participants.sort()

                giftsTo = self.__uniformShuffle(participants)
                while 0 in [x - y for x, y in zip(participants, giftsTo)]:
                    giftsTo = self.__uniformShuffle(participants)

                logs.info(giftsTo)
                self.__giftToParticipants = dict()
                for participant, giftTo in zip(participants, giftsTo):
                    self.__giftToParticipants[participant] = self.__participants[giftTo]

                logs.critical(self.__participants)
                logs.critical(self.__giftToParticipants)

                await ctx.send('Finished distribution.')

                for participant in self.__participants:
                    participantUser = await self.__bot.fetch_user(participant)
                    await participantUser.send(f'The assigned person is ||{self.__giftToParticipants[participant]}||.')

                await ctx.send('Done sending messages.')
            else:
                await ctx.send('The number of participants is small and you cannot distribute.')
        else:
            await ctx.send('You cannot distribute because the event has not closed.')

