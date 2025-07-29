from tortoise import Tortoise

async def init():
    await Tortoise.init(
        db_url='sqlite://db.sqlite3',
        modules={'models': ['models.drug']}
    )
    await Tortoise.generate_schemas()
    