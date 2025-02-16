from djongo import models


class Clothes(models.Model):
    _id = models.CharField(max_length=255, primary_key=True)  # ID là string
    name = models.CharField(max_length=255)
    size = models.CharField(max_length=50)
    price = models.FloatField()  # Giá là float
    image_url = models.CharField(max_length=500)  # URL ảnh là string

    class Meta:
        db_table = "clothes"  # Đặt tên collection trên MongoDB
