from djongo import models


class Mobile(models.Model):
    _id = models.CharField(max_length=255, primary_key=True)  # ID là string
    name = models.CharField(max_length=255)
    brand = models.CharField(max_length=255)
    price = models.FloatField()  # Giá là float
    image_url = models.CharField(max_length=500)  # URL ảnh là string
    
    class Meta:
        db_table = "mobiles"  # Đặt tên collection trên MongoDB
