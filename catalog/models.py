from django.db import models
from .fields import CloudinaryImageField 


class Category(models.Model):
    """Категория товаров"""
    title = models.CharField('Название', max_length=200)
    created_at = models.DateTimeField('Создано', auto_now_add=True)
    
    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ['title']
    
    def __str__(self):
        return self.title


class Product(models.Model):
    """Товар"""
    STATUS_CHOICES = [
        ('new', 'Новая поставка'),
        ('regular', 'Обычный товар'),
    ]
    
    title = models.CharField('Название', max_length=300)
    category = models.ForeignKey(
        Category, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='products',
        verbose_name='Категория'
    )
    description = models.TextField('Описание', blank=True)
    price = models.DecimalField(
        'Цена', 
        max_digits=10, 
        decimal_places=2, 
        null=True, 
        blank=True
    )
    status = models.CharField(
        'Статус',
        max_length=20,
        choices=STATUS_CHOICES,
        default='regular'
    )
    is_active = models.BooleanField('Активен', default=True)
    created_at = models.DateTimeField('Создано', auto_now_add=True)
    updated_at = models.DateTimeField('Обновлено', auto_now=True)
    
    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'
        ordering = ['-created_at']
    
    def __str__(self):
        return self.title


class ProductImage(models.Model):
    """Изображения товара"""
    product = models.ForeignKey(
        Product, 
        on_delete=models.CASCADE, 
        related_name='images',
        verbose_name='Товар'
    )
    # image = models.ImageField('Изображение', upload_to='products/%Y/%m/%d/')
    image = CloudinaryImageField('Изображение', upload_to='products/%Y/%m/%d/')
    order = models.PositiveIntegerField('Порядок', default=0)
    created_at = models.DateTimeField('Создано', auto_now_add=True)
    
    class Meta:
        verbose_name = 'Изображение товара'
        verbose_name_plural = 'Изображения товаров'
        ordering = ['order', 'created_at']
    
    def __str__(self):
        return f"Фото {self.product.title}"
