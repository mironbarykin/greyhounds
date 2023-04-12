import mysql.connector
from decouple import config


class Connection:
    def __init__(self, closed: bool = True):
        """
        Opens the database connection and creates cursor, If close flag is active, connection will be closed after usage.
        :param closed: bool
        """
        self.db = mysql.connector.connect(host=config('TEST_DB_HOST'), user=config('TEST_DB_USERNAME'), passwd=config('TEST_DB_PASSWORD'), database=config('TEST_DB_DATABASE'))
        self.cursor = self.db.cursor()
        self.closed = closed

    def insert(self, table: str, arguments: dict):
        """
        Inserts value in table with arguments.
        :param table: str
        :param arguments: dict(column: value)
        :return: None
        """
        self.cursor.execute(f"""INSERT INTO {table} ({", ".join([f'{argument}' for argument in arguments])}) VALUES ({", ".join([f"'{arguments[argument]}'" for argument in arguments])})""")
        self.db.commit()

        if self.closed:
            self.close()

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

        if self.closed:
            self.close()

    def get(self, table: str):
        """
        Get all data from table.
        :param table: str
        :return: tuple
        """
        self.cursor.execute(f"""SELECT * FROM {table}""")

        response = self.cursor.fetchall()
        if self.closed:
            self.close()

        return response

    def close(self):
        self.cursor.close()
        self.db.close()


if __name__ == '__main__':
    pass
