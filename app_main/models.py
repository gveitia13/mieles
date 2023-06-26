from ckeditor.fields import RichTextField
from django.db import models


# Create your models here.
class Category(models.Model):
    name = models.CharField('Nombre', max_length=100)

    def __str__(self): return self.name


class Language(models.Model):
    name = models.CharField('Nombre', max_length=100)


class Code(models.Model):
    title = models.CharField('Título', max_length=100)
    code = RichTextField('Código')


class ImageCode(models.Model):
    code = models.ForeignKey(Code, on_delete=models.CASCADE)
    image = models.ImageField('Imagen', upload_to='code/image/')
