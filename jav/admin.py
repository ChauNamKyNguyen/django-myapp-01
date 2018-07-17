from django.contrib import admin

# My app
from jav.models import Actress, Movie, UserProfile

# Modify admin page
class ActressAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('name',)}

class MovieAdmin(admin.ModelAdmin):
    list_display = ('title', 'actress', 'url')

# Register your models here.
admin.site.register(Actress, ActressAdmin)
admin.site.register(Movie, MovieAdmin)
admin.site.register(UserProfile)
