from django.db import models

from api.accounts.models import User

# Create your models here.
class Ticket(models.Model):
    name = models.CharField(max_length=128)
    total = models.IntegerField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    related_ticket = models.ForeignKey('self', on_delete=models.DO_NOTHING, default=1)

    def __str__(self):
        return self.user.username + '的' + self.name

    def make_response_data(self):
        ticket = {'pid': self.id, 'name': self.name, 'total': self.total}
        return ticket

    def use(self):
        self.total -= 1
        self.related_ticket.total += 1
        self.save()
        self.related_ticket.save()
