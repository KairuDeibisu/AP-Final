

from Note.database.database import Database

from sqlalchemy import select


db = Database()

user_table = db.user_table


insert_stmt = user_table.insert().values(
    content="Hello, World"
)

print(type(insert_stmt))
