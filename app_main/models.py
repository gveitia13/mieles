from crum import get_current_user
from django.conf import settings
from django.db import models
from django.utils.safestring import mark_safe


# Create your models here.
class Category(models.Model):
    name = models.CharField('Nombre', max_length=100)

    def __str__(self): return self.name

    class Meta:
        verbose_name = 'Categoría'


class Language(models.Model):
    name = models.CharField('Nombre', max_length=100)

    class Meta:
        verbose_name = 'Lenguaje'

    def __str__(self): return self.name


class Code(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    language = models.ForeignKey(Language, on_delete=models.CASCADE)
    title = models.CharField('Título', max_length=100)
    code = models.TextField('Código')
    description = models.TextField('Descripción', null=True, blank=True)

    def get_description(self):
        desc = self.description if len(self.description) < 80 else self.description[:80] + ' ...'
        return desc

    class Meta:
        ordering = ('language', 'category', 'title')
        verbose_name = 'Código'

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        user = get_current_user()
        if not self.user_id:
            self.user_id = user.pk
        return super().save()

    def __str__(self):
        return self.title

    def get_all_img(self):
        html = ''
        imgs = self.imagecode_set.all()
        if imgs.exists():
            for img in imgs:
                html += f'<a href="{img.image.url}" target="_blank"><img class="img-fluid mb-2" ' \
                        f'style="border: 2px solid gray" src="{img.image.url}"></a>'
        return mark_safe(html)

    get_all_img.short_description = 'Vista previa'
    get_description.short_description = 'Descripción'


class ImageCode(models.Model):
    code = models.ForeignKey(Code, on_delete=models.CASCADE)
    image = models.ImageField('Imagen', upload_to='code/image/')

    class Meta:
        verbose_name = 'Imagen de Código'
        verbose_name_plural = 'Imágenes de Código'

    def get_img(self):
        return mark_safe(
            f'<a href="{self.image.url}" target="_blank"><img src="{self.image.url}" '
            f'style="border: 2px solid gray" height="60"></a>')

    get_img.short_description = 'Vista previa'

    def __str__(self): return self.image.name
