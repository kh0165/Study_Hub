from django.contrib import admin
from .models import Analysis


@admin.register(Analysis)
class AnalysisAdmin(admin.ModelAdmin):

    list_display = (
        'title',
        'user',
        'analysis_type',
        'status',
        'created_at',
    )

    list_filter = (
        'analysis_type',
        'status',
    )

    search_fields = (
        'title',
        'user__username',
    )