import mysql.connector as con
import time
from config import Config
mydb=con.connect(host=Config.DB_HOST,user=Config.DB_USER,password=Config.DB_PASSWORD,port=Config.DB_PORT)
mycursor=mydb.cursor()

