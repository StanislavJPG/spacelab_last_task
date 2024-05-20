from tortoise import fields
from tortoise.models import Model


class ExchangeRate(Model):
    """
    model for SQL DB
    """
    id = fields.IntField(pk=True)
    mins = fields.IntField()
    price = fields.CharField(max_length=255)
    close_time = fields.BigIntField()

    class Meta:
        table = 'exchange_rate'

    def __str__(self):
        return self.price
