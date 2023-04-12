import discord
from services.database import Connection
from services.general import Time, Report


class CarsTakingReportView(discord.ui.View):
    """
    A class representing the view of car's taking report.
    """
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label='Вернуть', style=discord.ButtonStyle.blurple, custom_id='0')
    async def callback(self, interaction, button):
        Connection().update(table='cars', arguments={'status': '0'}, conditions={'name': interaction.message.content})

        embed = interaction.message.embeds[0]
        embed.set_footer(text=f'{embed.footer.text} - {Time().str()}')

        await interaction.response.edit_message(embed=embed, view=None)


class UpdatableStatusReportView(discord.ui.View):
    """
    A class representing the view of updatable status view. 
    """
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label='Обновить', style=discord.ButtonStyle.blurple, custom_id='1')
    async def callback(self, interaction, button):
        await interaction.response.edit_message(**StatusReport(author=interaction.user).response())


class TakingReport(Report):
    """
    A class representing the car's taking report.
    """
    def __init__(self, author, car, comment):
        super().__init__(author=author)

        self.car = car

        self.fields = [(':receipt:', 'Отчет о пользовании автопарком!', ' '),
                       (':bust_in_silhouette:', '**Автор**', author.mention),
                       (':red_car:', '**Автомобиль**', self.car)]

        if comment is not None:
            self.fields.append((':pencil2:', '**Комментарий**', comment))

        Connection().update('cars', {'status': author.id, 'timestamp': Time().timestamp()}, {'name': self.car})

    def embed(self):
        return self.generate_embed(fields=self.fields)

    def response(self):
        return {'content': self.car, 'embed': self.embed(), 'view': CarsTakingReportView()}


class StatusReport(Report):
    """
    A class representing the status report.
    """
    def __init__(self, author):
        super().__init__(author=author)
        self.fields = [(':card_box:', 'Статус автомобилей.', '')]
        for car in Connection().get('cars'):
            field = ['', '', '']
            field[1] = car[0]
            if car[1] == '0':
                field[0] = ':green_circle:'
            else:
                field[0] = ':red_circle:'
                field[2] = f'<@{car[1]}>'
            self.fields.append(field)

    def embed(self):
        return self.generate_embed(fields=self.fields)

    def response(self):
        return {'content': ' ', 'embed': self.embed()}


if __name__ == '__main__':
    pass
