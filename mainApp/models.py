from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.urls import reverse
from django.utils.text import slugify

# Create your models here.
class Degree(models.Model): 
    name = models.CharField(max_length=100)
    description = models.TextField(max_length=1500)
    numYears = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(4)])

    def __str__(self):
        return self.name

class Student(models.Model):
    name = models.CharField(max_length=100)
    surname = models.CharField(max_length=100)
    picture = models.ImageField(upload_to='mainApp/Students/images', null=True)
    age = models.IntegerField(validators=[MinValueValidator(16), MaxValueValidator(55)])
    slug = models.SlugField(default='', null=False, db_index=True, unique=True)
    finished_degree = models.BooleanField(default=False)
    degree = models.ForeignKey(Degree, on_delete=models.CASCADE, related_name='fkstudents')

    def get_absolute_url(self):
        return reverse("book-detail", args=[self.slug])

    def save(self, *args, **kwargs):
        self.slug = slugify(f"{self.name} {self.surname}")
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} {self.surname} -- {self.degree.name}"