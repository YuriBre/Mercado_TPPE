from databases import Database

DATABASE_URL = "mysql+aiomysql://user:user123@db:3306/mercado"
database = Database(DATABASE_URL)
