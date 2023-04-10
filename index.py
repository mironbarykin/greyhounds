import discord
import service
import database
from decouple import config

TARGET_GUILD = discord.Object(id=config('GUILD_ID'))

client = service.Client()


@client.tree.command(name='car', description='Использование автопарка.', guild=TARGET_GUILD)
@discord.app_commands.choices(car=service.generate_car_choices())
async def command_car(interaction, car: discord.app_commands.Choice[str], comment: str = None):

    report = service.Report(author=interaction.user, vehicle=car, comment=comment)

    await interaction.response.send_message(content=f'{car.name}', embed=report.generate_embed(), view=service.ReportView())


@client.tree.command(name='cars', description='Статус автопарка.', guild=TARGET_GUILD)
async def command_cars(interaction):

    await interaction.response.send_message(content='', embed=service.generate_statuses_embed())


@client.tree.command(name='car_add', description='Обновление автопарка.', guild=TARGET_GUILD)
async def command_cars(interaction, name: str):
    try:
        database.add_new_car(name)
        await interaction.response.send_message(content=f'Автомобиль {name} **успешно** добавлен в ваш автопарк.')
    except Exception as error:
        await interaction.response.send_message(content=f'Новый автомобиль **не удалось** добавить в ваш автопарк. \n {error}')


@client.event
async def on_ready():
    await synchronisation()
    print('The bot is ready to serve!')


async def synchronisation():
    await client.tree.sync(guild=TARGET_GUILD)

client.run(config('DISCORD_BOT_TOKEN'))
