from tortoise import Model, fields

class Drug(Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=30)
    price = fields.IntField()
    date = fields.CharField(max_length=45)
    author = fields.CharField(max_length=100)

    class Meta:
        table = "drugs"

    def __str__(self):
        return self.name