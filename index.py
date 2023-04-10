import discord
from decouple import config

import services

TARGET_GUILD = discord.Object(id=config('GUILD_ID'))

client = services.general.Client()


@client.tree.command(name='cars_take', description='Взять машину.', guild=TARGET_GUILD)
@discord.app_commands.choices(car=[discord.app_commands.Choice(name=f'{car[0]}', value='0') for car in services.database.Connection().get('cars')])
async def command_car(interaction, car: discord.app_commands.Choice[str], comment: str = None):
    print(car)
    # TODO; DISCORD IS ALWAYS SENDING ONLY FIRST CAR, NOT WHAT I'AM CHOOSING
    response = services.cars.TakingReport(interaction.user, car.name, comment).response()
    await interaction.response.send_message(**response)


@client.tree.command(name='cars_status', description='Статус машин.', guild=TARGET_GUILD)
async def command_cars(interaction):
    response = services.cars.StatusReport(interaction.user).response()
    await interaction.response.send_message(**response)


@client.tree.command(name='car_add', description='Обновление автопарка.', guild=TARGET_GUILD)
async def command_cars(interaction, name: str):
    pass


@client.event
async def on_ready():
    await synchronisation()
    print('The bot is ready to serve!')


async def synchronisation():
    await client.tree.sync(guild=TARGET_GUILD)

client.run(config('DISCORD_BOT_TOKEN'))
