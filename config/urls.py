from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from study import views as study_views


urlpatterns = [

    path(
        'admin/',
        admin.site.urls
    ),

    path(
        '',
        include('accounts.urls')
    ),

    path(
        'dashboard/',
        include('dashboard.urls')
    ),

    path(
        'analysis/',
        include('analysis.urls')
    ),
    path(
    'chatbot/',
    include('chatbot.urls')
),
    path(
        'subjects/',
        include('study.urls')
    ),

    # =========================
    # Password Reset
    # =========================

    path(
        'password-reset/',
        auth_views.PasswordResetView.as_view(
            template_name='accounts/password_reset.html'
        ),
        name='password_reset'
    ),

    path(
        'password-reset/done/',
        auth_views.PasswordResetDoneView.as_view(
            template_name='accounts/password_reset_done.html'
        ),
        name='password_reset_done'
    ),

    path(
        'password-reset-confirm/<uidb64>/<token>/',
        auth_views.PasswordResetConfirmView.as_view(
            template_name='accounts/password_reset_confirm.html'
        ),
        name='password_reset_confirm'
    ),

    path(
        'password-reset-complete/',
        auth_views.PasswordResetCompleteView.as_view(
            template_name='accounts/password_reset_complete.html'
        ),
        name='password_reset_complete'
    ),

    # =========================
    # Tasks
    # =========================

    path(
        'tasks/',
        study_views.task_list,
        name='task_list'
    ),

    path(
        'tasks/new/',
        study_views.create_task,
        name='create_task'
    ),

    path(
        'tasks/<int:task_id>/toggle/',
        study_views.toggle_task,
        name='toggle_task'
    ),

    path(
        'tasks/<int:task_id>/edit/',
        study_views.edit_task,
        name='edit_task'
    ),

    path(
        'tasks/<int:task_id>/delete/',
        study_views.delete_task,
        name='delete_task'
    ),

    # =========================
    # Notes
    # =========================

    path(
        'notes/categories/',
        study_views.note_categories,
        name='note_categories'
    ),

    path(
        'notes/categories/new/',
        study_views.create_note_category,
        name='create_note_category'
    ),

    path(
        'notes/',
        study_views.note_list,
        name='note_list'
    ),

    # =========================
    # Resources
    # =========================

    path(
        'subjects/<int:subject_id>/resources/add/',
        study_views.create_resource,
        name='create_resource'
    ),

    path(
        'resources/<int:resource_id>/',
        study_views.resource_detail,
        name='resource_detail'
    ),

    path(
        'resources/<int:resource_id>/edit/',
        study_views.edit_resource,
        name='edit_resource'
    ),

    path(
        'resources/<int:resource_id>/delete/',
        study_views.delete_resource,
        name='delete_resource'
    ),

    # =========================
    # PDF
    # =========================

    path(
        'export-pdf/',
        study_views.export_pdf,
        name='export_pdf'
    ),


]


if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )