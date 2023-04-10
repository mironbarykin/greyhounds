import discord


class CarsReportView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label='Вернуть', style=discord.ButtonStyle.blurple, custom_id='0')
    async def get_back(self, interaction, button):

        update_car_status(interaction.message.content, 0)

        interaction.message.embeds[0].set_footer(text=f'{interaction.message.embeds[0].footer.text} - {get_current_time()}')

        await interaction.response.edit_message(embed=new_embed, view=None)
