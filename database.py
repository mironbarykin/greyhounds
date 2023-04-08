import mysql.connector
import os

db = mysql.connector.connect(
    host='bpitxcssf60tabkyp3gu-mysql.services.clever-cloud.com',
    user=os.getenv('DB_USERNAME'),
    passwd=os.getenv('DB_PASSWORD'),
    database='bpitxcssf60tabkyp3gu'
)

cursor = db.cursor()
