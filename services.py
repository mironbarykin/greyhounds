import datetime
import discord
import uuid
from discord.ext import commands

DEFAULT_BUTTON_STYLE = discord.ButtonStyle.blurple


class Client(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix='/', intents=discord.Intents().all())

    async def setup_hook(self) -> None:
        self.add_view(ReportView())


class ReportView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label='Вернуть', style=DEFAULT_BUTTON_STYLE, custom_id='0')
    async def get_back(self, interaction, button):
        await interaction.response.edit_message(content=f'{interaction.message.content} - {get_current_time()}', view=None)


class Report:
    def __init__(self, author, vehicle, comment=None):
        self.report_id = str(uuid.uuid4())
        self.fields = [f':bust_in_silhouette: **Автор** {author.mention}', f':red_car: **Автомобиль** {vehicle.name}']
        if comment is not None:
            self.fields.append(f':bookmark: **Примечание** {comment}')

    def generate_embed(self):
        embed = discord.Embed(color=discord.Color.purple())
        embed.add_field(name='Отчет о пользовании автопарком.', value="\n".join(self.fields), inline=True)
        embed.set_footer(text=f'ID: {self.report_id}')
        return embed


def get_current_time():
    """
    Function for getting formatted current Europe/Moscow (UTC+3) time.
    :return: str
    """
    return datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=3))).strftime('%H:%M:%S')


if __name__ == '__main__':
    pass
