from django.urls import path

from . import views


urlpatterns = [

    path(
        '',
        views.subject_list,
        name='subject_list'
    ),

    path(
        'new/',
        views.create_subject,
        name='create_subject'
    ),

    path(
        '<int:subject_id>/',
        views.subject_detail,
        name='subject_detail'
    ),
    # path(
    #     'tasks/',
    #     views.task_list,
    #     name='task_list'
    # ),
    path(
        '<int:subject_id>/notes/new/',
        views.create_note,
        name='create_note'
    ),
    path(
        'notes/<int:note_id>/',
        views.note_detail,
        name='note_detail'
    ),
    path(
        'notes/<int:note_id>/edit/',
        views.edit_note,
        name='edit_note'
    ),
    path(
        'notes/<int:note_id>/delete/',
        views.delete_note,
        name='delete_note'
    ),
    path(
        '<int:subject_id>/courses/new/',
        views.create_course,
        name='create_course'
    ),
    path(
        'courses/<int:course_id>/',
        views.course_detail,
        name='course_detail'
    ),
    path(
        'courses/<int:course_id>/edit/',
        views.edit_course,
        name='edit_course'
    ),
    path(
        'courses/<int:course_id>/delete/',
        views.delete_course,
        name='delete_course'
    ),
    # path(
    #     'notes/',
    #     views.note_list,
    #     name='note_list'
    # ),
    # path(
    #     'subjects/<int:subject_id>/resources/add/',
    #     views.create_resource,
    #     name='create_resource'
    # ),
    path(
        '<int:subject_id>/assignments/new/',
        views.create_assignment,
        name='create_assignment'
    ),
     path(
        'assignments/<int:assignment_id>/',
        views.assignment_detail,
        name='assignment_detail'
    ),
    path(
        'assignments/<int:assignment_id>/edit/',
        views.edit_assignment,
        name='edit_assignment'
    ),
    path(
        'assignments/',
        views.assignment_list,
        name='assignment_list'
    ),
    path(
        'assignments/<int:assignment_id>/delete/',
        views.delete_assignment,
        name='delete_assignment'
    ),
    path(
        'export-pdf/',
        views.export_pdf,
        name='export_pdf'
    ),
]