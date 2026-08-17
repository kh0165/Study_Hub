from django.contrib import admin

from .models import Subject, Note, Course, Task, NoteCategory

@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):

    list_display = (
        'name',
        'user',
        'created_at',
    )

    search_fields = (
        'name',
        'user__username',
    )

    list_filter = (
        'created_at',
    )


@admin.register(Note)
class NoteAdmin(admin.ModelAdmin):

    list_display = (
        'title',
        'subject',
        'user',
        'created_at',
    )

    search_fields = (
        'title',
        'content',
        'user__username',
    )

    list_filter = (
        'subject',
        'created_at',
    )
    
@admin.register(NoteCategory)
class NoteCategoryAdmin(admin.ModelAdmin):

    list_display = (
        'name',
        'user',
        'created_at',
    )

    search_fields = (
        'name',
    )

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):

    list_display = (
        'title',
        'subject',
        'user',
        'created_at',
    )

    search_fields = (
        'title',
        'description',
        'user__username',
    )

    list_filter = (
        'subject',
        'created_at',
    )


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):

    list_display = (
        'title',
        'user',
        'priority',
        'due_date',
        'completed',
        'created_at',
    )

    list_filter = (
        'priority',
        'completed',
        'due_date',
    )

    search_fields = (
        'title',
        'description',
        'user__username',
    )