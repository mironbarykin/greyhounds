import discord
import services
import database
from decouple import config

GUILD_ID = 921654208082632725

CAR_CHOICES = [
    discord.app_commands.Choice(name='G63 AMG 6x6 (DL406RLP)', value='1'),
    discord.app_commands.Choice(name='BMW X6M F86 (TS168VLL)', value='2'),
    discord.app_commands.Choice(name='Infiniti FX50S (II976CBX)', value='3'),
    discord.app_commands.Choice(name='BMW x5 e70 (LH749IYP)', value='4'),
    discord.app_commands.Choice(name='Audi RS6 2002 (BO657QTM)', value='5'),
    discord.app_commands.Choice(name='Alfa Romeo Giulia (PN955NEC)', value='6'),
    discord.app_commands.Choice(name='Lamborghini Sian (VZ745SMF)', value='7'),
]

client = services.Client()


@client.tree.command(name='status', description='Информация о статусе бота.', guild=discord.Object(id=GUILD_ID))
async def command_test(interaction):
    await interaction.response.send_message(content='Бот поднят, все в порядке.')


@client.tree.command(name='car', description='Использование автопарка.', guild=discord.Object(id=GUILD_ID))
@discord.app_commands.choices(car=CAR_CHOICES)
async def command_car(interaction, car: discord.app_commands.Choice[str], comment: str = None):

    report = services.Report(author=interaction.user, vehicle=car, comment=comment)

    await interaction.response.send_message(content=f'{car.name}', embed=report.generate_embed(), view=services.ReportView())


@client.tree.command(name='cars', description='Статус автопарка.', guild=discord.Object(id=GUILD_ID))
async def command_cars(interaction):

    await interaction.response.send_message(content='', embed=services.generate_statuses_embed())


@client.tree.command(name='car_add', description='Обновление автопарка.', guild=discord.Object(id=GUILD_ID))
async def command_cars(interaction, name: str):
    try:
        database.add_new_car(name)
        await interaction.response.send_message(content=f'Автомобиль {name}, **успешно** добавлен в ваш автопарк.')
    except Exception as error:
        await interaction.response.send_message(content=f'Новый автомобиль **не удалось** добавить в ваш автопарк. '
                                                        f'\n {error}')


@client.event
async def on_ready():
    await client.tree.sync(guild=discord.Object(id=GUILD_ID))
    print('The bot is ready to serve!')

client.run(config('DISCORD_BOT_TOKEN'))
