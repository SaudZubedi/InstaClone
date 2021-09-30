from django.contrib import admin
from .models import *

# Register your models here.

class FollowAdmin(admin.ModelAdmin):
    list_display = ('user', 'following', )
    search_fields = ('user', 'following', )
    readonly_fields = ()
    
    filter_horizontal   = ()
    list_filter         = ()
    fieldsets           = ()

admin.site.register(Post)
admin.site.register(PostLike)
admin.site.register(Comment)
admin.site.register(SavedPost)
admin.site.register(Follow, FollowAdmin)