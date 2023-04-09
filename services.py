import datetime
import discord
import uuid
from discord.ext import commands
from database import update_car_status, get_all_cars
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
        update_car_status(interaction.message.content, 0)
        new_embed = interaction.message.embeds[0].set_footer(text=f'{interaction.message.embeds[0].footer.text} - {get_current_time()}')
        await interaction.response.edit_message(embed=new_embed, view=None)


class Report:
    def __init__(self, author, vehicle, comment=None):
        self.report_id = str(uuid.uuid4())
        self.fields = [f':bust_in_silhouette: **Автор** {author.mention}',
                       f':red_car: **Автомобиль** {vehicle.name}']
        if comment is not None:
            self.fields.append(f':bookmark: **Примечание** {comment}')

        update_car_status(vehicle.name, author.id)

    def generate_embed(self):
        """
        Generates embed for report.
        :return: discord.Embed
        """
        embed = discord.Embed(color=discord.Color.purple(), description=self.report_id)
        embed.add_field(name='Отчет о пользовании автопарком.', value="\n".join(self.fields), inline=True)
        embed.set_footer(text=get_current_time())
        return embed


def get_current_time():
    """
    Function for getting formatted current Europe/Moscow (UTC+3) time.
    :return: str
    """
    return datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=3))).strftime('%H:%M:%S')


def generate_statuses_embed():
    embed = discord.Embed(color=discord.Color.purple())
    fields = list()
    for car in get_all_cars():
        author_flag = False
        string = ''
        if car[1] == '0':
            string += ':green_circle: '
        else:
            string += ':red_circle: '
            author_flag = True
        string += car[0]
        if author_flag:
            string += f' - <@!{car[1]}>'
        fields.append(string)

    embed.add_field(name='Статусы автомобилей.', value="\n".join(fields), inline=True)
    embed.set_footer(text=get_current_time())
    return embed


if __name__ == '__main__':
    pass
