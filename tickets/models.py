from django.db import models
from django.utils import timezone


# Create your models here.
class Ticket(models.Model):
    
    title = models.CharField(max_length=254, default='')
    summary = models.TextField(blank=False)
    ticket_type = models.CharField(max_length=30)
    upvotes = models.IntegerField(default=0)
    total_paid = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    creator = models.CharField(max_length=150) 
    status = models.CharField(max_length=30, default='Backlog')
    initiation_date = models.DateTimeField( default=timezone.now)
    completion_date = models.DateTimeField(blank=True, null=True)
    
    def __str__(self):
        return "{0} - {1}".format(self.ticket_type, self.title)