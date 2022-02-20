from django.contrib.auth import get_user_model
from django.db import models
from ckeditor.fields import RichTextField
from django.utils.text import slugify


class Article(models.Model):
    title = models.CharField(max_length=200)
    summary = models.CharField(max_length=200, blank=True, null=True)
    body = RichTextField()
    photo = models.ImageField(upload_to='images/', blank=True, null=True)
    date = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        related_name="articles"
    )
    slug = models.SlugField(max_length=500, unique=True, null=True, blank=True)

    class Meta:
        ordering = ["-date"]

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):

        if self.slug == None:
            slug = slugify(self.title)

            has_slug = Article.objects.filter(slug=slug).exists()
            count = 1
            while has_slug:
                count += 1
                slug = slugify(self.title) + '-' + str(count)
                has_slug = Article.objects.filter(slug=slug).exists()

            self.slug = slug

        super().save(*args, **kwargs)


class Comment(models.Model):
    article = models.ForeignKey(
        Article,
        on_delete=models.CASCADE,
        related_name="comments"
    )
    name = models.CharField(max_length=100)
    email = models.EmailField()
    body = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=False)

    class Meta:
        ordering = ["created_on"]

    def __str__(self):
        return f"Comment {self.body} by {self.name}"

