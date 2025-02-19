from django.db import models


class Name(models.Model):
    firstname = models.CharField(max_length=255)
    lastname = models.CharField(max_length=255)

    class Meta:
        db_table = "name"  # MySQL
        
    def __str__(self):
        return f"{self.firstname} {self.lastname}"


class Address(models.Model):
    street = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    state = models.CharField(max_length=255)
    zip_code = models.CharField(max_length=20)

    class Meta:
        db_table = "address"  # MySQL
        
    def __str__(self):
        return f"{self.street}, {self.city}, {self.state}, {self.zip_code}"


class Customer(models.Model):
    username = models.CharField(max_length=255, unique=True)
    password = models.CharField(max_length=255)
    name = models.ForeignKey(
        Name, on_delete=models.CASCADE, db_column='name_id')
    address = models.ForeignKey(
        Address, on_delete=models.CASCADE, db_column='address_id')
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = "customer"  # MySQL

    def __str__(self):
        return self.username
