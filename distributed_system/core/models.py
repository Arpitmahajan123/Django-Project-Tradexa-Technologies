from django.db import models
from django.core.exceptions import ValidationError
import re

class User(models.Model):
    """User model stored in users.db"""
    name = models.CharField(max_length=100)
    email = models.EmailField()
    
    class Meta:
        db_table = 'users'
        app_label = 'core'
    
    def clean(self):
        """Application-level validation"""
        errors = {}
        
        if not self.name or not self.name.strip():
            errors['name'] = f"User {self.id}: Name cannot be empty"
        
        if not self.email or '@' not in self.email:
            errors['email'] = f"User {self.id}: Invalid email format"
        
        if errors:
            raise ValidationError(errors)
    
    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"User(id={self.id}, name='{self.name}', email='{self.email}')"

class Product(models.Model):
    """Product model stored in products.db"""
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    
    class Meta:
        db_table = 'products'
        app_label = 'core'
    
    def clean(self):
        """Application-level validation"""
        errors = {}
        
        if not self.name or not self.name.strip():
            errors['name'] = f"Product {self.id}: Name cannot be empty"
        
        if self.price is not None and self.price < 0:
            errors['price'] = f"Product {self.id}: Price cannot be negative"
        
        if errors:
            raise ValidationError(errors)
    
    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"Product(id={self.id}, name='{self.name}', price=${self.price})"

class Order(models.Model):
    """Order model stored in orders.db"""
    user_id = models.IntegerField()
    product_id = models.IntegerField()
    quantity = models.IntegerField()
    
    class Meta:
        db_table = 'orders'
        app_label = 'core'
    
    def clean(self):
        """Application-level validation"""
        errors = {}
        
        if self.user_id is not None and self.user_id <= 0:
            errors['user_id'] = f"Order {self.id}: Invalid user_id"
        
        if self.product_id is not None and self.product_id <= 0:
            errors['product_id'] = f"Order {self.id}: Invalid product_id"
        
        if self.quantity is not None and self.quantity <= 0:
            errors['quantity'] = f"Order {self.id}: Quantity must be positive"
        
        if errors:
            raise ValidationError(errors)
    
    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"Order(id={self.id}, user_id={self.user_id}, product_id={self.product_id}, quantity={self.quantity})"