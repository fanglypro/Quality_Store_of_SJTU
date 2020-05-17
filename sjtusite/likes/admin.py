from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import LikeRecord, LikeCount


# Register your models here.


class LikeCountAdmin(admin.ModelAdmin):
    list_display = ['content_type', 'object_id', 'content_object', 'liked_num']
    # fields = ['name',  'text', 'shop']


class LikeRecordAdmin(admin.ModelAdmin):
    list_display = ['content_type', 'object_id', 'content_object']
    # fields = ['name',  'text', 'shop']


admin.site.register(LikeCount, LikeCountAdmin)
admin.site.register(LikeRecord, LikeRecordAdmin)
