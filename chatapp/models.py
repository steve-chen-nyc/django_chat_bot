from django.db import models

# Create your models here.
class Client(models.Model):
    name = models.CharField(max_length=100)
    date_created = models.DateTimeField('date published')

    def __str__(self):
        return self.name

class Project(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=100)
    date_created = models.DateTimeField('date published')

    def __str__(self):
        return self.name
