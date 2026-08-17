from django.urls import path
from . import views


urlpatterns = [

    path(
        '',
        views.analysis_list,
        name='analysis_list'
    ),

    path(
        'new/',
        views.create_analysis,
        name='create_analysis'
    ),

    path(
        'history/',
        views.analysis_history,
        name='analysis_history'
    ),

    path(
        '<int:analysis_id>/',
        views.analysis_detail,
        name='analysis_detail'
    ),

]