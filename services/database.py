import mysql.connector
from decouple import config


class Connection:
    def __init__(self):
        self.db = mysql.connector.connect(host=config('DB_HOST'), user=config('DB_USERNAME'), passwd=config('DB_PASSWORD'), database=config('DB_DATABASE'))
        self.cursor = self.db.cursor()

    def insert(self, table: str, arguments: dict):
        """
        Inserts value in table with arguments.
        :param table: str
        :param arguments: dict(column: value)
        :return: None
        """
        self.cursor.execute(f"""INSERT INTO {table} ({", ".join([f'{argument}' for argument in arguments])}) VALUES ({", ".join([f"'{arguments[argument]}'" for argument in arguments])})""")
        self.db.commit()

    def update(self, table: str, arguments: dict, conditions: dict):
        """
        Updates argument in table under conditions.
        :param table: str
        :param arguments: dict(column: value)
        :param conditions: dict(column: value)
        :return: None
        """
        self.cursor.execute(f"""UPDATE {table} SET {",".join([f"{argument} = '{arguments[argument]}'" for argument in arguments])} WHERE {" AND ".join([f"{condition} = '{conditions[condition]}'" for condition in conditions])}""")
        self.db.commit()

    def get(self, table: str):
        """
        Get all data from table.
        :param table: str
        :return: tuple
        """
        self.cursor.execute(f"""SELECT * FROM {table}""")
        return self.cursor.fetchall()

    def close(self):
        self.cursor.close()
        self.db.close()


if __name__ == '__main__':
    pass
