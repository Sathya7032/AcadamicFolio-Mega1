from django.contrib import admin
from .models import *
# Register your models here.

class UserAdmin(admin.ModelAdmin):
    list_display = ['username', 'email']

admin.site.register(User,UserAdmin)    
admin.site.register(Task)
admin.site.register(TutorialName)
admin.site.register(Blogs)
admin.site.register(TutorialPost)
admin.site.register(Meme)
admin.site.register(Contact)

