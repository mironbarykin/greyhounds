import discord
import datetime
import uuid
from discord.ext import commands

import services


class Client(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix='/', intents=discord.Intents().all())

    async def setup_hook(self) -> None:
        self.add_view(services.cars.CarsTakingReportView())


class Time:
    def __init__(self):
        self.datetime = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=3)))

    def str(self):
        return self.datetime.strftime('%H:%M:%S')


class Report:
    def __init__(self, author: discord.User):
        self.id = str(uuid.uuid4())
        self.author = author

    def generate_embed(self, fields: list):
        """
        Generated embed for this report with specified fields. Fields[0] is heading.
        :param fields: list[tuple(emoji, name, value)]
        :return: discord.Embed
        """
        embed = discord.Embed(color=discord.Color.purple(), description=self.id)
        embed.add_field(name=f'{fields[0][0]} **{fields[0][1]}** ', value='\n'.join([f'{fields[i][0]} {fields[i][1]} {fields[i][2]}' for i in range(1, len(fields))]))
        embed.set_footer(text=Time().str())
        return embed
