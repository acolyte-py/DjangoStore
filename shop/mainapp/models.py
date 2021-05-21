from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.utils import timezone

User = get_user_model()


class Category(models.Model):
    name = models.CharField(max_length=255, verbose_name='Имя категории')
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse(
            'category_detail',
            kwargs={
                'slug': self.slug
            }
        )

    def get_fields_for_filter_in_template(self):
        return ProductFeatures.objects.filter(
            category=self,
            use_in_filter=True,
        ).prefetch_related('category').value(
            'feature_key', 'filter_measure', 'feature_name', 'filter_type'
        )


class Product(models.Model):
    category = models.ForeignKey(
        Category,
        verbose_name='Категория',
        on_delete=models.CASCADE,
    )
    title = models.CharField(max_length=255, verbose_name='Наименование')
    slug = models.SlugField(unique=True)
    image = models.ImageField(verbose_name='Изображение')
    description = models.TextField(verbose_name='Описание', null=True)
    price = models.DecimalField(
        max_digits=9,
        decimal_places=2,
        default=0,
        verbose_name='Цена',
    )

    def __str__(self):
        return self.title

    def get_model_name(self):
        return self.__class__.__name__.lower()

    def get_absolute_url(self):
        return reverse(
            'product_detail',
            kwargs={
                'slug': self.slug
            }
        )


class ProductFeatures(models.Model):
    RADIO = 'radio'
    CHECKBOX = 'checkbox'

    FILTER_TYPE_CHOICES = (
        (RADIO, 'Радиокнопка'),
        (CHECKBOX, 'Чекбокс'),
    )
    feature_key = models.CharField(
        max_length=100,
        verbose_name='Ключ характеристики'
    )
    feature_name = models.CharField(
        max_length=255,
        verbose_name='Наименование хаарктеристики'
    )
    category = models.ForeignKey(
        Category,
        verbose_name='Категория',
        on_delete=models.CASCADE,
    )
    postfix_for_value = models.CharField(
        max_length='20',
        null=True,
        blank=True,
        verbose_name='Постфикс для значения',
        help_text='7 часов работы -> 1 час работы -> 2 часа работы'
    )
    use_in_filter = models.BooleanField(
        default=False,
        verbose_name='Использовать фильтрацию товаров в шаблоне',
    )
    filter_type = models.CharField(
        max_length=20,
        verbose_name='Тип фильтра',
        default=CHECKBOX,
        choices=FILTER_TYPE_CHOICES,
    )
    filter_measure = models.CharField(
        max_length=50,
        verbose_name='Единица измерения для фильра',
        help_text='Единица измерения для конкретного фильтра -> "5" часов'
    )

    def __str__(self):
        return f'Категория - "{self.category.name}"' \
               f'| Характеристика - "{self.feature_name}" '


class ProductFeatureValidators(models.Model):
    category = models.ForeignKey(
        Category,
        verbose_name='Категория',
        on_delete=models.CASCADE,
    )
    feature = models.ForeignKey(
        ProductFeatures,
        verbose_name='Характеристика',
        null=True,
        blank=True,
        on_delete=models.CASCADE,
    )
    feature_value = models.CharField(
        max_length=255,
        unique=True,
        null=True,
        blank=True,
        verbose_name='Значения характеристики',
    )

    def __str__(self):
        if not self.feature:
            return f'Валидатор категории "{self.category.name}" - ' \
                   f'характеристика не выбрана '
        return f'Валидатор категории "{self.category.name}" | ' \
               f'Характеристика - "{self.feature.feature_name}" | ' \
               f'Значения - "{self.feature_value}"'


class CartProduct(models.Model):
    user = models.ForeignKey(
        'Customer',
        verbose_name='Покупатель',
        on_delete=models.CASCADE,
    )
    cart = models.ForeignKey(
        'Cart',
        verbose_name='Корзина',
        on_delete=models.CASCADE,
        related_name='related_products',
    )
    product = models.ForeignKey(
        Product,
        verbose_name='Товар',
        on_delete=models.CASCADE,
    )
    qty = models.PositiveIntegerField(default=1)
    final_price = models.DecimalField(
        max_digits=9,
        decimal_places=2,
        default=0,
        verbose_name='Общая цена',
    )

    def __str__(self):
        return 'Продукт: {} (for cart)'.format(self.product.title)

    def save(self, *args, **kwargs):
        self.final_price = self.qty * self.product.price
        super().save(*args, **kwargs)


class Cart(models.Model):
    owner = models.ForeignKey(
        'Customer',
        null=True,
        verbose_name='Владелец',
        on_delete=models.CASCADE,
    )
    products = models.ManyToManyField(
        CartProduct,
        blank=True,
        related_name='related_cart',
    )
    total_products = models.PositiveIntegerField(default=0)
    final_price = models.DecimalField(
        max_digits=9,
        decimal_places=2,
        default=0,
        verbose_name='Общая цена'
    )
    in_order = models.BooleanField(default=False)
    for_anonymous_user = models.BooleanField(default=False)

    def __str__(self):
        return str(self.id)


class Customer(models.Model):
    user = models.ForeignKey(
        User,
        verbose_name='Покупатель',
        on_delete=models.CASCADE,
    )
    phone = models.CharField(
        max_length=16,
        verbose_name='Телефон',
        null=True,
        blank=True,
    )
    address = models.CharField(
        max_length=255,
        verbose_name='Адрес',
        null=True,
        blank=True,
    )
    orders = models.ManyToManyField(
        'Order',
        verbose_name='Заказы покупателя',
        related_name='related_customer'
    )

    def __str__(self):
        return 'Покупатель: {} {}'.format(
            self.user.first_name,
            self.user.last_name
        )


class Order(models.Model):
    STATUS_NEW = 'new'
    STATUS_IN_PROGRESS = 'in_progress'
    STATUS_READY = 'is_ready'
    STATUS_COMPLETED = 'completed'

    BUYING_TYPE_SELF = 'self'
    BUYING_TYPE_DELIVERY = 'delivery'

    STATUS_CHOICES = (
        (STATUS_NEW, 'Новый заказ'),
        (STATUS_IN_PROGRESS, 'Заказ в обработке'),
        (STATUS_READY, 'Заказ готов'),
        (STATUS_COMPLETED, 'Заказ выполнен'),
    )

    BUYING_TYPE_CHOICES = (
        (BUYING_TYPE_SELF, 'Самовывоз'),
        (BUYING_TYPE_DELIVERY, 'Доставка'),
    )

    customer = models.ForeignKey(
        Customer,
        verbose_name='Покупатель',
        related_name='related_orders',
        on_delete=models.CASCADE,
    )
    first_name = models.CharField(max_length=20, verbose_name='Имя')
    last_name = models.CharField(max_length=30, verbose_name='Фамилия')
    phone = models.CharField(max_length=11, verbose_name='Номер телефон')
    cart = models.ForeignKey(
        Cart,
        verbose_name='Корзина',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    address = models.CharField(
        max_length=1024,
        verbose_name='Адрес',
        null=True,
        blank=True,
    )
    status = models.CharField(
        max_length=100,
        verbose_name='Статус заказа',
        choices=STATUS_CHOICES,
        default=STATUS_NEW,
    )
    buying_type = models.CharField(
        max_length=100,
        verbose_name='Тип заказа',
        choices=BUYING_TYPE_CHOICES,
        default=BUYING_TYPE_SELF,
    )
    comment = models.TextField(
        verbose_name='Комментарий к заказу',
        null=True,
        blank=True
    )
    created_at = models.DateTimeField(
        verbose_name='Дата создание заказа',
        auto_now=True,
    )
    order_data = models.DateField(
        verbose_name='Дата получения заказа',
        default=timezone.now()
    )

    def __str__(self):
        return str(self.id)
