from django.db import models
from django.contrib.auth.models import AbstractUser


# customer model
class User(AbstractUser):
    birth_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.username


# model for item submissions in one day
class ItemSubmissionDate(models.Model):
    create_date = models.DateField(null=False)

    class Meta:
        ordering = ['-create_date']

    def __str__(self):
        return str(self.create_date)


# model for having in one day
class Items(models.Model):
    FOOD_CHOICES = [
        ('Bread', 'Bread'),
        ('Egg', 'Egg'),
        ('Chicken', 'Chicken'),
        ('Beef', 'Beef'),
        ('Mutton', 'Mutton'),
        ('Milk', 'Milk'),
    ]
    name = models.CharField(max_length=40, choices=FOOD_CHOICES)
    quantity = models.IntegerField()
    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    item_submissions_date = models.ForeignKey(ItemSubmissionDate, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


# tweets table
class Tweets(models.Model):
    user_name = models.CharField(max_length=40,)
    description = models.CharField(max_length=200,)



