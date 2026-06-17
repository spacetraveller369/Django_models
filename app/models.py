from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

class Movie(models.Model):
    title = models.CharField(max_length=200, verbose_name="Название фильма")
    description = models.TextField(verbose_name="Описание фильма")
    release_date = models.DateField(verbose_name="Дата создания")
    country = models.CharField(max_length=100, verbose_name="Страна")
    poster = models.ImageField(upload_to='posters/', verbose_name="Постер")
    
    rating = models.IntegerField(
        verbose_name="Рейтинг",
        validators=[
            MinValueValidator(1, message="Рейтинг не может быть меньше 1"),
            MaxValueValidator(5, message="Рейтинг не может быть больше 5")
        ]
    )

    def __str__(self):
        return self.title
