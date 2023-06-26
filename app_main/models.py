from ckeditor.fields import RichTextField
from django.db import models


# Create your models here.
class Category(models.Model):
    name = models.CharField('Nombre', max_length=100)

    def __str__(self): return self.name

    class Meta:
        verbose_name = 'Categoría'


class Language(models.Model):
    name = models.CharField('Nombre', max_length=100)

    def __str__(self): return self.name


class Code(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    language = models.ForeignKey(Language, on_delete=models.CASCADE)
    title = models.CharField('Título', max_length=100)
    code = RichTextField('Código')
    description = models.TextField('Descripción', null=True, blank=True)

    class Meta:
        ordering = ('language', 'category', 'title')
        verbose_name = 'Código'

    def __str__(self): return self.title


class ImageCode(models.Model):
    code = models.ForeignKey(Code, on_delete=models.CASCADE)
    image = models.ImageField('Imagen', upload_to='code/image/')

    class Meta:
        verbose_name = 'Imagen de Código'
        verbose_name_plural = 'Imágenes de Código'

    def __str__(self): return self.image.name
