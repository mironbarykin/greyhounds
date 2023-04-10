import discord
from database import update_car_status, get_all_cars


def generate_car_choices():
    """
    Generates a list of discord.app_commands.Choice objects for all cars currently in the database.
    :return: list[discord.app_commands.Choice]
    """
    choices = list()
    for car in get_all_cars():
        choices.append(discord.app_commands.Choice(name=car[0], value=''))
    return choices


if __name__ == '__main__':
    pass
