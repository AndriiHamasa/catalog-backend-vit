from django.db import models
import cloudinary
import cloudinary.uploader
from django.conf import settings


class CloudinaryImageField(models.ImageField):
    """
    Кастомное поле для загрузки изображений на Cloudinary
    """
    
    def save_form_data(self, instance, data):
        """Переопределяем сохранение - загружаем на Cloudinary"""
        if data and hasattr(data, 'read'):
            # Только на продакшене загружаем на Cloudinary
            if settings.RAILWAY_ENVIRONMENT:
                # Загружаем на Cloudinary
                upload_result = cloudinary.uploader.upload(
                    data,
                    folder="products",
                    resource_type="image"
                )
                # Сохраняем URL вместо файла
                setattr(instance, self.name, upload_result['secure_url'])
            else:
                # Локально сохраняем как обычно
                super().save_form_data(instance, data)
        elif data is False:
            # Удаление изображения
            setattr(instance, self.name, None)
