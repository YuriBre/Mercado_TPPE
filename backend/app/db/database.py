from databases import Database

DATABASE_URL = "mysql+aiomysql://user:user123@db/mercado"

database = Database(DATABASE_URL)