from django.contrib import admin
from .models import LikeRecord, LikeCount


class LikeCountAdmin(admin.ModelAdmin):
    list_display = ['content_type', 'object_id', 'content_object', 'liked_num']


class LikeRecordAdmin(admin.ModelAdmin):
    list_display = ['content_type', 'object_id', 'content_object']


admin.site.register(LikeCount, LikeCountAdmin)
admin.site.register(LikeRecord, LikeRecordAdmin)
