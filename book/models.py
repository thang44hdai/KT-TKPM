from django.db import models

# Create your models here.


class Book(models.Model):
    _id = models.CharField(max_length=255, primary_key=True)
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    price = models.FloatField()
    image = models.CharField(max_length=500)
    description = models.TextField()
    published_date = models.DateField()

    class Meta:
        db_table = "book"  # Chỉ định tên collection trong MongoDB
