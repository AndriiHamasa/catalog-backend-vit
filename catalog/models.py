from django.db import models
from django.core.files.uploadedfile import InMemoryUploadedFile, TemporaryUploadedFile


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


# class ProductImage(models.Model):
#     """Изображения товара"""
#     product = models.ForeignKey(
#         Product, 
#         on_delete=models.CASCADE, 
#         related_name='images',
#         verbose_name='Товар'
#     )
#     # image = models.ImageField('Изображение', upload_to='products/%Y/%m/%d/')
#     image = CloudinaryImageField('Изображение', upload_to='products/%Y/%m/%d/')
#     order = models.PositiveIntegerField('Порядок', default=0)
#     created_at = models.DateTimeField('Создано', auto_now_add=True)
    
#     class Meta:
#         verbose_name = 'Изображение товара'
#         verbose_name_plural = 'Изображения товаров'
#         ordering = ['order', 'created_at']
    
#     def __str__(self):
#         return f"Фото {self.product.title}"

# class ProductImage(models.Model):
#     """Изображения товара"""
#     product = models.ForeignKey(
#         Product, 
#         on_delete=models.CASCADE, 
#         related_name='images',
#         verbose_name='Товар'
#     )
    
#     # Два способа загрузки: файл ИЛИ URL
#     image = models.ImageField(
#         'Загрузить файл', 
#         upload_to='products/%Y/%m/%d/',
#         blank=True,
#         null=True,
#         help_text='Загрузите изображение с компьютера'
#     )
#     image_url = models.URLField(
#         'Или вставьте URL',
#         max_length=500,
#         blank=True,
#         null=True,
#         help_text='Вставьте прямую ссылку на изображение (например, с Cloudinary)'
#     )
    
#     order = models.PositiveIntegerField('Порядок', default=0)
#     created_at = models.DateTimeField('Создано', auto_now_add=True)
    
#     class Meta:
#         verbose_name = 'Изображение товара'
#         verbose_name_plural = 'Изображения товаров'
#         ordering = ['order', 'created_at']
    
#     def __str__(self):
#         return f"Фото {self.product.title}"
    
#     def get_image_url(self):
#         """Возвращает URL изображения (из файла или из URL поля)"""
#         if self.image_url:
#             return self.image_url
#         elif self.image:
#             return self.image.url
#         return None
    
#     def clean(self):
#         """Валидация: должно быть заполнено хотя бы одно поле"""
#         from django.core.exceptions import ValidationError
#         if not self.image and not self.image_url:
#             raise ValidationError('Загрузите файл или укажите URL изображения')
        
    # def save(self, *args, **kwargs):
    #     """Переопределяем сохранение для загрузки на Cloudinary"""
    #     if self.image and not self.image_url:
    #         # Если загружен файл - загружаем на Cloudinary
    #         import cloudinary.uploader
    #         from django.conf import settings
            
    #         if settings.RAILWAY_ENVIRONMENT:
    #             try:
    #                 # Загружаем на Cloudinary
    #                 upload_result = cloudinary.uploader.upload(
    #                     self.image,
    #                     folder="products",
    #                     resource_type="image"
    #                 )
    #                 # Сохраняем URL в image_url
    #                 self.image_url = upload_result['secure_url']
    #                 # Очищаем поле image
    #                 self.image = None
    #             except Exception as e:
    #                 print(f"❌ Ошибка загрузки на Cloudinary: {e}")
        
    #     super().save(*args, **kwargs)

    # def save(self, *args, **kwargs):
    #     """Переопределяем сохранение для загрузки на Cloudinary"""
    #     if self.image and not self.image_url:
    #         # Если загружен файл - загружаем на Cloudinary
    #         from django.conf import settings
            
    #         if settings.RAILWAY_ENVIRONMENT:
    #             try:
    #                 import cloudinary.uploader
                    
    #                 # Читаем файл
    #                 self.image.seek(0)  # Важно! Возвращаем указатель в начало
                    
    #                 # Загружаем на Cloudinary
    #                 upload_result = cloudinary.uploader.upload(
    #                     self.image.file,  # ← Используем .file вместо самого объекта
    #                     folder="products",
    #                     resource_type="image"
    #                 )
                    
    #                 # Сохраняем URL в image_url
    #                 self.image_url = upload_result['secure_url']
                    
    #                 # Очищаем поле image (чтобы не сохранять файл локально)
    #                 self.image = None
                    
    #             except Exception as e:
    #                 # Логируем ошибку
    #                 import logging
    #                 logger = logging.getLogger(__name__)
    #                 logger.error(f"❌ Ошибка загрузки на Cloudinary: {e}")
    #                 # Не прерываем сохранение - пусть хотя бы файл сохранится
        
    #     super().save(*args, **kwargs)

class ProductImage(models.Model):
    """Изображения товара"""
    product = models.ForeignKey(
        Product, 
        on_delete=models.CASCADE, 
        related_name='images',
        verbose_name='Товар'
    )
    
    # Только URL изображения (пользователь сам загружает на Cloudinary)
    # image_url = models.URLField(
    #     'URL изображения',
    #     max_length=500,
    #     help_text='Вставьте прямую ссылку на изображение с Cloudinary'
    # )
    # Временное поле для загрузки файла
    image = models.ImageField(
        'Загрузить файл', 
        upload_to='products/temp/',  # Временная папка
        blank=True,
        null=True,
        help_text='Загрузите изображение (будет автоматически загружено на Cloudinary)'
    )
    
    # Финальное хранилище - URL
    image_url = models.URLField(
        'Или вставьте URL',
        max_length=500,
        blank=True,
        help_text='Вставьте прямую ссылку на изображение'
    )
    
    order = models.PositiveIntegerField('Порядок', default=0)
    created_at = models.DateTimeField('Создано', auto_now_add=True)
    
    class Meta:
        verbose_name = 'Изображение товара'
        verbose_name_plural = 'Изображения товаров'
        ordering = ['order', 'created_at']
    
    def __str__(self):
        return f"Фото {self.product.title}"
    
    def get_image_url(self):
        """Возвращает URL изображения"""
        if self.image_url:
            return self.image_url
        elif self.image:
            return self.image.url
        return None
    
    def clean(self):
        """Валидация"""
        from django.core.exceptions import ValidationError
        if not self.image and not self.image_url:
            raise ValidationError('Загрузите файл или укажите URL изображения')
    
    # def save(self, *args, **kwargs):
    #     """Обработка загрузки на Cloudinary"""
    #     from django.conf import settings
        
    #     # Только на Railway загружаем на Cloudinary
    #     if self.image and not self.image_url and hasattr(settings, 'RAILWAY_ENVIRONMENT') and settings.RAILWAY_ENVIRONMENT:
    #         try:
    #             import cloudinary.uploader
                
    #             # Правильное чтение файла
    #             if isinstance(self.image, (InMemoryUploadedFile, TemporaryUploadedFile)):
    #                 # Файл загружен через форму
    #                 self.image.seek(0)
    #                 file_to_upload = self.image
    #             else:
    #                 # Файл уже на диске
    #                 file_to_upload = self.image.path
                
    #             # Загружаем на Cloudinary
    #             upload_result = cloudinary.uploader.upload(
    #                 file_to_upload,
    #                 folder="products",
    #                 resource_type="image",
    #                 timeout=60
    #             )
                
    #             # Сохраняем URL
    #             self.image_url = upload_result['secure_url']
                
    #             # Очищаем временный файл
    #             self.image.delete(save=False)
    #             self.image = None
                
    #         except Exception as e:
    #             # Логируем ошибку но НЕ прерываем сохранение
    #             print(f"⚠️ Cloudinary upload failed: {e}")
    #             # Файл останется на Railway (временно), но это не критично
        
    #     super().save(*args, **kwargs)

