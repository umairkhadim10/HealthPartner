from django.db import models
from django.contrib.auth.models import AbstractUser


# customer model
class User(AbstractUser):
    birth_date = models.DateField(null=True, blank=True)


# model for item submissions in one day
class ItemSubmission(models.Model):
    create_date = models.DateField(null=False)

    class Meta:
        ordering = ['-create_date']


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
    item_submissions = models.ForeignKey(ItemSubmission, on_delete=models.CASCADE)


# tweets table
class Tweets(models.Model):
    user_name = models.CharField(max_length=40,)
    description = models.CharField(max_length=200,)

    # def get_all_tweets(self):
    #     return self.


