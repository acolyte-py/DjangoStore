from django.db import models

from ..mainapp.models import Category, Product


class CategoryFeature(models.Model):
    category = models.ForeignKey(
        Category,
        verbose_name='Категория',
        on_delete=models.CASCADE,
    )
    feature_name = models.CharField(
        max_length=100,
        verbose_name='Имя характеристики',
    )
    feature_filter_name = models.CharField(
        max_length=100,
        verbose_name='Имя фильтра для характеристики',
    )
    unit = models.CharField(
        max_length=25,
        verbose_name='Единица измерения',
        null=True,
        blank=True,
    )

    class Meta:
        unique_together = ('category', 'feature_name', 'feature_filter_name')

    def __str__(self):
        return f'{self.category.name} | {self.feature_name}'


class FeatureValidator(models.Model):
    category = models.ForeignKey(
        Category,
        verbose_name='Категория',
        on_delete=models.CASCADE,
    )
    feature_key = models.ForeignKey(
        CategoryFeature,
        verbose_name='Ключ характеристики',
        on_delete=models.CASCADE,
    )
    valid_feature_value = models.CharField(
        max_length=100,
        verbose_name='Валидное значение'
    )

    def __str__(self):
        return f'Категория {self.category.name} | ' \
               f'Характеристика {self.feature_key.feature_name} | ' \
               f'Валдное значение {self.valid_feature_value}'


class ProductFeatures(models.Model):
    product = models.ForeignKey(
        Product,
        verbose_name='Товар',
        on_delete=models.CASCADE,
    )
    feature = models.ForeignKey(
        CategoryFeature,
        verbose_name='Характеристика',
        on_delete=models.CASCADE,
    )
    value = models.CharField(
        max_length=255,
        verbose_name='Значения характеристики',
    )

    def __str__(self):
        return f'Товар - {self.product.title} | ' \
               f'Характеристика - {self.feature.feature_name} | ' \
               f'Значение - {self.value}'
