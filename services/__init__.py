import discord
import datetime
import uuid
from discord.ext import commands
from cars import CarsReportView
import cars

# fields =>[(EMOJI, HEADING, RESUL)]


class Client(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix='/', intents=discord.Intents().all())

    async def setup_hook(self) -> None:
        self.add_view(CarsReportView())


class Time:
    def __init__(self):
        self.datetime = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=3)))

    def __str__(self):
        return self.datetime.strftime('%H:%M:%S')


class Report:
    def __init__(self, author: discord.User):
        self.id = str(uuid.uuid4())
        self.author = author

    def embed(self, fields: list):
        """
        Returns embed for this report.
        :param fields: list[tuple(emoji, name, value)]
        :return: discord.Embed
        """
        embed = discord.Embed(color=discord.Color.purple(), description=self.id)
        embed.add_field(name=f'{fields[0][0]} **{fields[0][1]}** ', value='\n'.join([f'{fields[i][0]} **{fields[0][1]}** {fields[0][2]}' for i in range(len(fields) - 1)]))
        embed.set_footer(text=str(Time))
        return embed
