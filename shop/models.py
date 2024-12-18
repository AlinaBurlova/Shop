from django.db import models
from django.urls import reverse
from slugify import slugify


class Category(models.Model):
    name = models.CharField(max_length=200, verbose_name="Категория")
    slug = models.SlugField(max_length=200, unique=True)
    description = models.TextField(blank=True, verbose_name='Описание категории')
    image_1 = models.ImageField(upload_to='categories/image_1',
                              blank=True, verbose_name='Изображение №1')
    image_2 = models.ImageField(upload_to='categories/image_2',
                                blank=True, verbose_name='Изображение №2')

    class Meta:
        ordering = ['name']
        indexes = [
            models.Index(fields=['name']),
        ]
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('shop:category_detail', kwargs={'slug': self.slug})


class Product(models.Model):
    category = models.ForeignKey(Category,
                                 related_name='products',
                                 on_delete=models.CASCADE)
    author = models.CharField(max_length=75, verbose_name='Автор')
    name = models.CharField(max_length=200,
                            verbose_name='Название книги')
    description = models.TextField(blank=True, verbose_name='Описание книги')
    slug = models.SlugField(max_length=200)
    image = models.ImageField(upload_to='products/%Y/%m/%d',
                              blank=True, verbose_name='Фото')
    price = models.DecimalField(max_digits=10,
                                decimal_places=2)
    available = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']
        indexes = [
            models.Index(fields=['id', 'slug']),
            models.Index(fields=['name']),
            models.Index(fields=['-created']),
        ]
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        # slug = slugify(self.name)
        # counter = 1
        # while Product.objects.filter(slug=slug):
        #     slug = f"{slug}-{counter}"
        #     counter+=1
        #     self.slug = slug
        # super().save(*args, **kwargs)

        super().save(*args, **kwargs)
        slug_name = slugify(self.name)
        slug = f"{slug_name}-{self.pk}"
        self.slug = slug
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('shop:product_detail', kwargs={'slug': self.slug})
