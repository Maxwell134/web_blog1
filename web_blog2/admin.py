from django.contrib import admin

from .views import Post, Contact, Comments

# Register your models here.

admin.site.register(Post)
admin.site.register(Comments)
admin.site.register(Contact)