from django.contrib import admin
from blog.models import Post, BlogComment

# Register your models here.
# here we make the blogcomment as tupple
admin.site.register((BlogComment))


# for inject tinymce editor in admin panel for post
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    class Media:
        js = ('tinyinject.js',)
