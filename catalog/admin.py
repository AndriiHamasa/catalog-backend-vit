from django.contrib import admin
from django.utils.html import format_html
from .models import Category, Product, ProductImage


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['title', 'product_count', 'created_at']
    search_fields = ['title']
    
    def product_count(self, obj):
        count = obj.products.count()
        return f"{count} товар(ов)"
    product_count.short_description = 'Количество товаров'


# class ProductImageInline(admin.TabularInline):
#     """Инлайн для изображений товара - добавляем фото прямо в карточке товара"""
#     model = ProductImage
#     extra = 3  # Показываем 3 пустых поля для загрузки
#     fields = ['image', 'order', 'image_preview']
#     readonly_fields = ['image_preview']
    
#     def image_preview(self, obj):
#         if obj.image:
#             return format_html(
#                 '<img src="{}" style="max-height: 100px; max-width: 200px; border-radius: 5px;" />',
#                 obj.image.url
#             )
#         return "Нет изображения"
#     image_preview.short_description = 'Превью'
# class ProductImageInline(admin.TabularInline):
#     """Инлайн для изображений товара"""
#     model = ProductImage
#     extra = 1
#     fields = ['image', 'image_url', 'order', 'image_preview']
#     readonly_fields = ['image_preview']
    
#     def image_preview(self, obj):
#         url = obj.get_image_url()
#         if url:
#             return format_html(
#                 '<img src="{}" style="max-height: 100px; max-width: 200px; border-radius: 5px;" />',
#                 url
#             )
#         return "Нет изображения"
#     image_preview.short_description = 'Превью'
class ProductImageInline(admin.TabularInline):
    """Инлайн для изображений товара"""
    model = ProductImage
    extra = 1
    fields = ['image', 'image_url', 'order', 'image_preview']
    readonly_fields = ['image_preview']
    
    def image_preview(self, obj):
        if obj.image_url:
            return format_html(
                '<img src="{}" style="max-height: 100px; max-width: 200px; border-radius: 5px;" />',
                obj.image_url
            )
        return "Нет изображения"
    image_preview.short_description = 'Превью'


# @admin.register(Product)
# class ProductAdmin(admin.ModelAdmin):
#     list_display = [
#         'title', 
#         'category', 
#         'price', 
#         'status_badge',
#         'is_active', 
#         'images_count',
#         'created_at'
#     ]
#     list_filter = ['category', 'status', 'is_active', 'created_at']
#     search_fields = ['title', 'description']
#     list_editable = ['is_active', 'price']
#     inlines = [ProductImageInline]  # Фотки добавляются прямо тут
    
#     fieldsets = (
#         ('Основная информация', {
#             'fields': ('title', 'category', 'price')
#         }),
#         ('Описание', {
#             'fields': ('description',),
#             'classes': ('wide',)
#         }),
#         ('Статус и активность', {
#             'fields': ('status', 'is_active')
#         }),
#     )
    
#     def status_badge(self, obj):
#         if obj.status == 'new':
#             color = '#28a745'
#             text = '🆕 Новая поставка'
#         else:
#             color = '#6c757d'
#             text = '📦 Обычный'
#         return format_html(
#             '<span style="background: {}; color: white; padding: 3px 10px; border-radius: 3px; font-size: 11px;">{}</span>',
#             color, text
#         )
#     status_badge.short_description = 'Статус'
    
#     def images_count(self, obj):
#         count = obj.images.count()
#         if count == 0:
#             return format_html('<span style="color: red;">❌ 0 фото</span>')
#         return format_html('<span style="color: green;">✅ {} фото</span>', count)
#     images_count.short_description = 'Изображения'
    
#     # Делаем удобную сортировку
#     ordering = ['-created_at']

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = [
        'title', 
        'category', 
        'price', 
        'status_badge',
        'is_active', 
        'images_count',
        'created_at'
    ]
    list_filter = ['category', 'status', 'is_active', 'created_at']
    search_fields = ['title', 'description']
    list_editable = ['is_active', 'price']
    inlines = [ProductImageInline]
    
    fieldsets = (
        ('Основная информация', {
            'fields': ('title', 'category', 'price')
        }),
        ('Описание', {
            'fields': ('description',),
            'classes': ('wide',)
        }),
        ('Статус и активность', {
            'fields': ('status', 'is_active')
        }),
    )
    
    def status_badge(self, obj):
        if obj.status == 'new':
            color = '#28a745'
            text = '🆕 Новая поставка'
        else:
            color = '#6c757d'
            text = '📦 Обычный'
        return format_html(
            '<span style="background: {}; color: white; padding: 3px 10px; border-radius: 3px; font-size: 11px;">{}</span>',
            color, text
        )
    status_badge.short_description = 'Статус'
    
    def images_count(self, obj):
        count = obj.images.count()
        if count == 0:
            return format_html('<span style="color: red;">❌ 0 фото</span>')
        return format_html('<span style="color: green;">✅ {} фото</span>', count)
    images_count.short_description = 'Изображения'
    
    ordering = ['-created_at']

# @admin.register(ProductImage)
# class ProductImageAdmin(admin.ModelAdmin):
#     """На всякий случай оставляем отдельное управление фото"""
#     list_display = ['id', 'product', 'image_preview', 'order', 'created_at']
#     list_filter = ['created_at']
#     search_fields = ['product__title']
#     list_editable = ['order']
    
#     def image_preview(self, obj):
#         if obj.image:
#             return format_html(
#                 '<img src="{}" style="max-height: 50px; max-width: 100px; border-radius: 5px;" />',
#                 obj.image.url
#             )
#         return "Нет изображения"
#     image_preview.short_description = 'Превью'

# @admin.register(ProductImage)
# class ProductImageAdmin(admin.ModelAdmin):
#     list_display = ['id', 'product', 'image_preview', 'has_file', 'has_url', 'order', 'created_at']
#     list_filter = ['created_at']
#     search_fields = ['product__title']
#     list_editable = ['order']
#     fields = ['product', 'image', 'image_url', 'order', 'image_preview']
#     readonly_fields = ['image_preview']
    
#     def image_preview(self, obj):
#         url = obj.get_image_url()
#         if url:
#             return format_html(
#                 '<img src="{}" style="max-height: 100px; max-width: 200px; border-radius: 5px;" />',
#                 url
#             )
#         return "Нет изображения"
#     image_preview.short_description = 'Превью'
    
#     def has_file(self, obj):
#         return '✅' if obj.image else '❌'
#     has_file.short_description = 'Файл'
    
#     def has_url(self, obj):
#         return '✅' if obj.image_url else '❌'
#     has_url.short_description = 'URL'

@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ['id', 'product', 'image_preview', 'order', 'created_at']
    list_filter = ['created_at']
    search_fields = ['product__title']
    list_editable = ['order']
    fields = ['product', 'image_url', 'order', 'image_preview']
    readonly_fields = ['image_preview']
    
    def image_preview(self, obj):
        if obj.image_url:
            return format_html(
                '<img src="{}" style="max-height: 100px; max-width: 200px; border-radius: 5px;" />',
                obj.image_url
            )
        return "Нет изображения"
    image_preview.short_description = 'Превью'

