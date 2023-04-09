import mysql.connector
from decouple import config

db = mysql.connector.connect(
    host='bpitxcssf60tabkyp3gu-mysql.services.clever-cloud.com',
    user=config('DB_USERNAME'),
    passwd=config('DB_PASSWORD'),
    database='bpitxcssf60tabkyp3gu'
)

cursor = db.cursor()

# The initial table creating.
# cursor.execute("CREATE TABLE IF NOT EXISTS cars (name VARCHAR(50), status INT)")


def add_new_car(name):
    """
    Adds new car with its name to the database with status 0.
    :param name: str 'car_name (plate)'
    :return: None
    """
    cursor.execute(f"""INSERT INTO cars (name, status) VALUES ('{name}', '{0}')""")
    db.commit()


def update_car_status(car, status):
    """
    Updates the car status in the database to the ID of current owner, or 0 if free to use.
    :param car: str 'car_name (plate)'
    :param status: int
    :return:
    """
    cursor.execute(f"""UPDATE cars SET status = '{status}' WHERE name = '{car}'""")
    db.commit()


def get_all_cars():
    """
    Returns all cars with statuses.
    :return: list
    """
    cursor.execute("""SELECT * FROM cars""")
    return cursor.fetchall()
