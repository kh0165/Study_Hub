from django.shortcuts import render, redirect
from study.models import Subject, Note, Course, Task, Resource , Assignment

def dashboard(request):

    if not request.user.is_authenticated:
        return redirect('login')

    user = request.user

    total_subjects = Subject.objects.filter(
        user=user
    ).count()

    total_notes = Note.objects.filter(
        user=user
    ).count()

    total_courses = Course.objects.filter(
        user=user
    ).count()

    total_resources = Resource.objects.filter(
        user=user
    ).count()

    total_tasks = Task.objects.filter(
        user=user
    ).count()

    completed_tasks = Task.objects.filter(
        user=user,
        completed=True
    ).count()

    pending_tasks = total_tasks - completed_tasks

    total_assignments = Assignment.objects.filter(
        user=user
    ).count()

    completed_assignments = Assignment.objects.filter(
        user=user,
        status='completed'
    ).count()

    pending_assignments = Assignment.objects.filter(
        user=user,
        status='pending'
    ).count()

    in_progress_assignments = Assignment.objects.filter(
        user=user,
        status='in_progress'
    ).count()

    recent_notes = Note.objects.filter(
        user=user
    ).select_related(
        'subject'
    ).order_by(
        '-created_at'
    )[:5]

    recent_resources = Resource.objects.filter(
        user=user
    ).select_related(
        'subject'
    ).order_by(
        '-created_at'
    )[:5]

    recent_tasks = Task.objects.filter(
        user=user
    ).order_by(
        '-created_at'
    )[:5]

    recent_courses = Course.objects.filter(
        user=user
    ).select_related(
        'subject'
    ).order_by(
        '-created_at'
    )[:5]
    return render(
        request,
        'dashboard/dashboard.html',
        {
            'total_subjects': total_subjects,
            'total_notes': total_notes,
            'total_courses': total_courses,
            'total_resources': total_resources,
            'total_tasks': total_tasks,
            'completed_tasks': completed_tasks,
            'pending_tasks': pending_tasks,
            'total_assignments': total_assignments,
            'completed_assignments': completed_assignments,
            'pending_assignments': pending_assignments,
            'in_progress_assignments': in_progress_assignments,
            'recent_notes': recent_notes,
            'recent_resources': recent_resources,
            'recent_tasks': recent_tasks,
            'recent_courses': recent_courses,
        }
    )