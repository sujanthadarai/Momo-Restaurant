from django.db import models

# Create your models here.
class Category(models.Model):
    title=models.CharField(max_length=200) #veg,buf,chicken
    
    def __str__(self):
        return self.title 
    
    
class Momo(models.Model):
    name=models.CharField(max_length=200) #veg steam momo
    category=models.ForeignKey(Category, on_delete=models.CASCADE)
    image=models.ImageField(upload_to="images")
    price=models.DecimalField(max_digits=8,decimal_places=2)
    
    def __str__(self):
        return self.name
    
    
class Contact(models.Model):
    name=models.CharField(max_length=200)
    email=models.EmailField()
    phone=models.CharField(max_length=20)
    message=models.TextField()
    