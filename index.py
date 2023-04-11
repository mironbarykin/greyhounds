import discord
from decouple import config

import services

TARGET_GUILD = discord.Object(id=config('GUILD_ID'))
CARS = services.database.Connection().get('cars')
CAR_CHOICES = [discord.app_commands.Choice(name=f'{CARS[car][0]}', value=f'{car}') for car in range(len(CARS))]
client = services.general.Client()


@client.tree.command(name='car', description='Взять машину.', guild=TARGET_GUILD)
@discord.app_commands.choices(car=CAR_CHOICES)
async def command_car(interaction, car: discord.app_commands.Choice[str], comment: str = None):
    response = services.cars.TakingReport(interaction.user, car.name, comment).response()
    await interaction.response.send_message(**response)


@client.tree.command(name='cars', description='Статус машин.', guild=TARGET_GUILD)
async def command_cars(interaction):
    response = services.cars.StatusReport(interaction.user).response()
    await interaction.response.send_message(**response)


@client.event
async def on_ready():
    await synchronisation()
    print('The bot is ready to serve!')


async def synchronisation():
    await client.tree.sync(guild=TARGET_GUILD)

client.run(config('DISCORD_BOT_TOKEN'))
