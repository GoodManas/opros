import pymysql

conn = pymysql.connect(
    host="localhost",
    user="root",
    password="root",
    db="salon"
)

print("connection ok")

cursor = conn.cursor()

def chek():
    cursor.execute("select from users")
    users_data = cursor.fetchall()
    return users_data