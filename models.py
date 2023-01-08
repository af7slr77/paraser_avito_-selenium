import sqlite3

db = sqlite3.connect("db.db")
cursor = db.cursor()
cursor.execute("""CREATE TABLE IF NOT EXISTS products (
        url UNIQUE=True,
        title,
        price,
        description,
        city 
)""")
db.commit()


def write_to_db(url, title, price, description, city):

    try:
        cursor.execute("""INSERT INTO products VALUES(?,?,?,?,?)""", (url, title, price, description, city))
        db.commit()
        print('data recorded!')
    except Exception as ex:
        print(ex)

