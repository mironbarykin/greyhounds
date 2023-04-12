import os
import discord

import services

TARGET_GUILD = discord.Object(id=os.getenv('TEST_GUILD_ID'))
CARS = services.database.Connection().get('cars')
CAR_CHOICES = [discord.app_commands.Choice(name=f'{CARS[car][0]}', value=f'{car}')
               for car in range(len(CARS))]
client = services.general.Client()


@client.tree.command(name='car', description='Взять машину.', guild=TARGET_GUILD)
@discord.app_commands.choices(car=CAR_CHOICES)
async def command_car(interaction, car: discord.app_commands.Choice[str], comment: str = None):
    """
    View layer of discord command /car.
    :interaction: discord.Interaction
    :car: str
    :comment: str, default=None
    """
    response = services.cars.TakingReport(interaction.user, car.name, comment).response()
    await interaction.response.send_message(**response)


@client.tree.command(name='cars', description='Статус машин.', guild=TARGET_GUILD)
async def command_cars(interaction, is_updatable: bool = False, is_static: bool = False):
    """
    View layer of discord command /cars.
    :interaction: discord.Interaction
    :is_updatable: bool, default=False
    :is_static: bool, default=False
    """
    response = services.cars.StatusReport(interaction.user).response()
    if is_updatable:
        response['view'] = services.cars.UpdatableStatusReportView()
    if not is_static:
        response['delete_after'] = 10
    await interaction.response.send_message(**response)


@client.event
async def on_ready():
    """
    Function which starting when bot is ready,
    synchronises the commands and send a message.
    """
    await synchronisation()
    print('The bot is ready to serve!')


async def synchronisation():
    """
    Synchronises the commands.
    """
    await client.tree.sync(guild=TARGET_GUILD)

client.run(os.getenv('TEST_DISCORD_BOT_TOKEN'))
