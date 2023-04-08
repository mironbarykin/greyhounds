import discord
import os

GUILD_ID = 921654208082632725

CAR_ACTIONS = [
    discord.app_commands.Choice(name='взять', value='1'),
    discord.app_commands.Choice(name='вернуть', value='2'),
    discord.app_commands.Choice(name='проверить', value='3')
]
CAR_CHOICES = [
    discord.app_commands.Choice(name='Машина Первая', value='1'),
    discord.app_commands.Choice(name='Машина Вторая', value='2'),
    discord.app_commands.Choice(name='Машина Третья', value='3')
]

bot = discord.Client(intents=discord.Intents.all())
commands = discord.app_commands.CommandTree(bot)


class OrderButtons(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label='Сдать машину')
    async def test(self, interaction: discord.Interaction, button: discord.ui.Button):
        interaction.response.edit_message(content='This report is closed.')


@commands.command(name="button", description="Just a test ;)", guild=discord.Object(id=GUILD_ID))
async def command_test(interaction):
    await interaction.response.send_message(content='This report is closed.')


@commands.command(name="car", description="Взаимодействия с автопарком.", guild=discord.Object(id=GUILD_ID))
@discord.app_commands.choices(action=CAR_ACTIONS)
@discord.app_commands.choices(car=CAR_CHOICES)
async def command_car(interaction, action: discord.app_commands.Choice[str], car: discord.app_commands.Choice[str]):

    response_embed = discord.Embed(color=discord.Color.purple())
    embed_fields = [f":bust_in_silhouette: **Автор** {interaction.user.mention}",
                    f":red_car: **Автомобиль** {car.value}"]
    response_embed.add_field(name='Отчет о взятии автомобиля.', value="\n".join(embed_fields), inline=True)

    await interaction.response.send_message(content=interaction.user.mention, embed=response_embed, view=OrderButtons())


@bot.event
async def on_ready():
    await commands.sync(guild=discord.Object(id=GUILD_ID))
    print("Ready!")

bot.run(os.getenv('DISCORD_BOT_TOKEN'))
