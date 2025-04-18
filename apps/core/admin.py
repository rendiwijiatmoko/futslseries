from django.contrib import admin
from .models import VideoHighlight, Partner, SuccessStory
from apps.teams.models import Team

@admin.register(VideoHighlight)
class HighlightAdmin(admin.ModelAdmin):
    list_display = ('title', 'is_active')
    list_editable = ('is_active',)
    def save_model(self, request, obj, form, change):
        if obj.is_active:
            VideoHighlight.objects.exclude(pk=obj.pk).update(is_active=False)
        super().save_model(request, obj, form, change)


@admin.register(Partner)
class PartnerAdmin(admin.ModelAdmin):
    list_display = ('name', 'order')


@admin.register(SuccessStory)
class SuccessStoryAdmin(admin.ModelAdmin):
    list_display = ('title', 'created')



