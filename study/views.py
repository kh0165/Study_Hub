from django.shortcuts import render, redirect, get_object_or_404
from django.db import models
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required

from .models import (
    Subject,
    Note,
    Course,
    Task,
    NoteCategory,
    Resource,
    Assignment
)
from django.http import HttpResponse
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4

def subject_list(request):

    if not request.user.is_authenticated:
        return redirect('login')

    subjects = Subject.objects.filter(
        user=request.user
    ).order_by('-created_at')

    return render(
        request,
        'study/subject_list.html',
        {
            'subjects': subjects
        }
    )


def create_subject(request):

    if not request.user.is_authenticated:
        return redirect('login')

    if request.method == 'POST':

        name = request.POST.get('name')
        description = request.POST.get('description')

        if name:
            Subject.objects.create(
                user=request.user,
                name=name,
                description=description
            )

        return redirect('subject_list')

    return render(
        request,
        'study/create_subject.html'
    )


def subject_detail(request, subject_id):

    if not request.user.is_authenticated:
        return redirect('login')

    subject = get_object_or_404(
        Subject,
        id=subject_id,
        user=request.user
    )

    courses = subject.courses.all().order_by('-created_at')

    resources = subject.resources.all().order_by('-created_at')

    notes = subject.notes.all().order_by('-created_at')

    assignments = subject.assignments.all().order_by('-created_at')

    # Calculate Progress
    total_assignments = assignments.count()

    if total_assignments > 0:

        progress_points = 0

        for assignment in assignments:

            if assignment.status == 'completed':
                progress_points += 100

            elif assignment.status == 'in_progress':
                progress_points += 50

        progress = int(progress_points / total_assignments)

    else:
        progress = 0

    return render(
        request,
        'study/subject_detail.html',
        {
            'subject': subject,
            'courses': courses,
            'resources': resources,
            'notes': notes,
            'assignments': assignments,
            'progress': progress,
        }
    )

def create_note(request, subject_id):

    if not request.user.is_authenticated:
        return redirect('login')

    subject = get_object_or_404(
        Subject,
        id=subject_id,
        user=request.user
    )

    categories = NoteCategory.objects.filter(
        user=request.user
    )

    if request.method == 'POST':

        title = request.POST.get('title', '').strip()
        content = request.POST.get('content', '').strip()
        category_id = request.POST.get('category')

        if title and content:

            category = None

            if category_id:
                category = get_object_or_404(
                    NoteCategory,
                    id=category_id,
                    user=request.user
                )

            Note.objects.create(
                user=request.user,
                subject=subject,
                category=category,
                title=title,
                content=content
            )

            return redirect(
                'subject_detail',
                subject_id=subject.id
            )

    return render(
        request,
        'study/create_note.html',
        {
            'subject': subject,
            'categories': categories,
        }
    )

def create_note_category(request):

    if not request.user.is_authenticated:
        return redirect('login')

    if request.method == 'POST':

        name = request.POST.get('name', '').strip()

        if name:
            NoteCategory.objects.create(
                user=request.user,
                name=name
            )

            return redirect('note_categories')

    return render(
        request,
        'study/create_note_category.html'
    )

def note_categories(request):

    if not request.user.is_authenticated:
        return redirect('login')

    categories = NoteCategory.objects.filter(
        user=request.user
    ).order_by('name')

    return render(
        request,
        'study/note_categories.html',
        {
            'categories': categories
        }
    )


def note_detail(request, note_id):

    if not request.user.is_authenticated:
        return redirect('login')

    note = get_object_or_404(
        Note,
        id=note_id,
        user=request.user
    )

    return render(
        request,
        'study/note_detail.html',
        {
            'note': note
        }
    )

def note_list(request):

    if not request.user.is_authenticated:
        return redirect('login')

    notes = Note.objects.filter(
        user=request.user
    ).select_related(
        'subject',
        'category'
    ).order_by('-created_at')

    categories = NoteCategory.objects.filter(
        user=request.user
    ).order_by('name')

    query = request.GET.get('q', '').strip()
    category_id = request.GET.get('category', '').strip()

    if query:
        notes = notes.filter(
            models.Q(title__icontains=query) |
            models.Q(content__icontains=query) |
            models.Q(subject__name__icontains=query) |
            models.Q(category__name__icontains=query)
        )

    if category_id:
        notes = notes.filter(
            category_id=category_id
        )

    # Pagination
    paginator = Paginator(notes, 5)

    page_number = request.GET.get('page')

    page_obj = paginator.get_page(page_number)

    return render(
        request,
        'study/note_list.html',
        {
            'notes': page_obj,
            'categories': categories,
            'page_obj': page_obj,
            'query': query,
            'selected_category': category_id,
        }
    )

def edit_note(request, note_id):

    if not request.user.is_authenticated:
        return redirect('login')

    note = get_object_or_404(
        Note,
        id=note_id,
        user=request.user
    )

    categories = NoteCategory.objects.filter(
        user=request.user
    )

    if request.method == 'POST':

        title = request.POST.get('title', '').strip()
        content = request.POST.get('content', '').strip()
        category_id = request.POST.get('category')

        if title and content:

            category = None

            if category_id:
                category = get_object_or_404(
                    NoteCategory,
                    id=category_id,
                    user=request.user
                )

            note.title = title
            note.content = content
            note.category = category

            note.save()

            return redirect(
                'note_detail',
                note_id=note.id
            )

    return render(
        request,
        'study/edit_note.html',
        {
            'note': note,
            'categories': categories,
        }
    )

def delete_note(request, note_id):

    if not request.user.is_authenticated:
        return redirect('login')

    note = get_object_or_404(
        Note,
        id=note_id,
        user=request.user
    )

    subject_id = note.subject.id

    if request.method == 'POST':

        note.delete()

        return redirect(
            'subject_detail',
            subject_id=subject_id
        )

    return render(
        request,
        'study/delete_note.html',
        {
            'note': note
        }
    )

def create_course(request, subject_id):

    if not request.user.is_authenticated:
        return redirect('login')

    subject = get_object_or_404(
        Subject,
        id=subject_id,
        user=request.user
    )

    if request.method == 'POST':

        title = request.POST.get('title', '').strip()
        platform = request.POST.get('platform', '').strip()
        instructor = request.POST.get('instructor', '').strip()
        progress = request.POST.get('progress', '0')
        status = request.POST.get('status', 'not_started')
        link = request.POST.get('link', '').strip()
        description = request.POST.get('description', '').strip()

        if title:

            Course.objects.create(
                user=request.user,
                subject=subject,
                title=title,
                platform=platform,
                instructor=instructor,
                progress=progress,
                status=status,
                link=link,
                description=description
            )

            return redirect(
                'subject_detail',
                subject_id=subject.id
            )

    return render(
        request,
        'study/create_course.html',
        {
            'subject': subject
        }
    )

def course_detail(request, course_id):

    if not request.user.is_authenticated:
        return redirect('login')

    course = get_object_or_404(
        Course,
        id=course_id,
        user=request.user
    )

    return render(
        request,
        'study/course_detail.html',
        {
            'course': course
        }
    )

def edit_course(request, course_id):

    if not request.user.is_authenticated:
        return redirect('login')

    course = get_object_or_404(
        Course,
        id=course_id,
        user=request.user
    )

    if request.method == 'POST':

        title = request.POST.get('title', '').strip()
        platform = request.POST.get('platform', '').strip()
        instructor = request.POST.get('instructor', '').strip()
        progress = request.POST.get('progress', '0')
        status = request.POST.get('status', 'not_started')
        link = request.POST.get('link', '').strip()
        description = request.POST.get('description', '').strip()

        if title:

            course.title = title
            course.platform = platform
            course.instructor = instructor
            course.progress = int(progress or 0)
            course.status = status
            course.link = link
            course.description = description

            course.save()

            return redirect(
                'course_detail',
                course_id=course.id
            )

    return render(
        request,
        'study/edit_course.html',
        {
            'course': course
        }
    )

def delete_course(request, course_id):

    if not request.user.is_authenticated:
        return redirect('login')

    course = get_object_or_404(
        Course,
        id=course_id,
        user=request.user
    )

    subject_id = course.subject.id

    if request.method == 'POST':

        course.delete()

        return redirect(
            'subject_detail',
            subject_id=subject_id
        )

    return render(
        request,
        'study/delete_course.html',
        {
            'course': course
        }
    )

def task_list(request):

    if not request.user.is_authenticated:
        return redirect('login')

    tasks = Task.objects.filter(
        user=request.user
    ).order_by(
        'completed',
        'due_date'
    )

    paginator = Paginator(tasks, 5)

    page_number = request.GET.get('page')

    page_obj = paginator.get_page(page_number)

    return render(
        request,
        'study/task_list.html',
        {
            'tasks': page_obj,
            'page_obj': page_obj,
        }
    )

def create_task(request):


    if not request.user.is_authenticated:
        return redirect('login')

    subjects = Subject.objects.filter(
        user=request.user
    )

    if request.method == 'POST':

        title = request.POST.get('title', '').strip()
        description = request.POST.get('description', '').strip()
        due_date = request.POST.get('due_date')
        priority = request.POST.get('priority', 'medium')
        subject_id = request.POST.get('subject')

        if title and subject_id:

            subject = get_object_or_404(
                Subject,
                id=subject_id,
                user=request.user
            )

            Task.objects.create(
                user=request.user,
                subject=subject,
                title=title,
                description=description,
                due_date=due_date if due_date else None,
                priority=priority
            )

            return redirect('task_list')

    return render(
        request,
        'study/create_task.html',
        {
            'subjects': subjects
        }
    )


def toggle_task(request, task_id):

    if not request.user.is_authenticated:
        return redirect('login')

    task = get_object_or_404(
        Task,
        id=task_id,
        user=request.user
    )

    task.completed = not task.completed
    task.save()

    return redirect('task_list')

def edit_task(request, task_id):

    if not request.user.is_authenticated:
        return redirect('login')

    task = get_object_or_404(
        Task,
        id=task_id,
        user=request.user
    )

    if request.method == 'POST':

        title = request.POST.get('title', '').strip()
        description = request.POST.get('description', '').strip()
        due_date = request.POST.get('due_date')
        priority = request.POST.get('priority', 'medium')

        if title:
            task.title = title
            task.description = description
            task.due_date = due_date if due_date else None
            task.priority = priority

            task.save()

            return redirect('task_list')

    return render(
        request,
        'study/edit_task.html',
        {
            'task': task
        }
    )

def delete_task(request, task_id):

    if not request.user.is_authenticated:
        return redirect('login')

    task = get_object_or_404(
        Task,
        id=task_id,
        user=request.user
    )

    if request.method == 'POST':
        task.delete()

    return redirect('task_list')


def create_resource(request, subject_id):

    if not request.user.is_authenticated:
        return redirect('login')

    subject = get_object_or_404(
        Subject,
        id=subject_id,
        user=request.user
    )

    if request.method == 'POST':

        title = request.POST.get('title', '').strip()
        description = request.POST.get('description', '').strip()
        link = request.POST.get('link', '').strip()
        resource_type = request.POST.get(
            'resource_type',
            'other'
        )

        if title and link:

            Resource.objects.create(
                user=request.user,
                subject=subject,
                title=title,
                description=description,
                link=link,
                resource_type=resource_type
            )

            return redirect(
                'subject_detail',
                subject_id=subject.id
            )

    return render(
        request,
        'study/create_resource.html',
        {
            'subject': subject,
        }
    )

def resource_detail(request, resource_id):

    if not request.user.is_authenticated:
        return redirect('login')

    resource = get_object_or_404(
        Resource,
        id=resource_id,
        user=request.user
    )

    return render(
        request,
        'study/resource_detail.html',
        {
            'resource': resource
        }
    )

def edit_resource(request, resource_id):

    if not request.user.is_authenticated:
        return redirect('login')

    resource = get_object_or_404(
        Resource,
        id=resource_id,
        user=request.user
    )

    if request.method == 'POST':

        title = request.POST.get('title', '').strip()
        description = request.POST.get('description', '').strip()
        link = request.POST.get('link', '').strip()
        resource_type = request.POST.get(
            'resource_type',
            'other'
        )

        if title and link:

            resource.title = title
            resource.description = description
            resource.link = link
            resource.resource_type = resource_type

            resource.save()

            return redirect(
                'resource_detail',
                resource_id=resource.id
            )

    return render(
        request,
        'study/edit_resource.html',
        {
            'resource': resource
        }
    )

def delete_resource(request, resource_id):

    if not request.user.is_authenticated:
        return redirect('login')

    resource = get_object_or_404(
        Resource,
        id=resource_id,
        user=request.user
    )

    subject_id = resource.subject.id

    if request.method == 'POST':

        resource.delete()

        return redirect(
            'subject_detail',
            subject_id=subject_id
        )

    return render(
        request,
        'study/delete_resource.html',
        {
            'resource': resource
        }
    )


def create_assignment(request, subject_id):

    if not request.user.is_authenticated:
        return redirect('login')

    subject = get_object_or_404(
        Subject,
        id=subject_id,
        user=request.user
    )

    if request.method == 'POST':

        title = request.POST.get('title', '').strip()
        description = request.POST.get('description', '').strip()
        due_date = request.POST.get('due_date')
        status = request.POST.get('status', 'pending')

        if title:
            Assignment.objects.create(
                user=request.user,
                subject=subject,
                title=title,
                description=description,
                due_date=due_date if due_date else None,
                status=status
            )

            return redirect(
                'subject_detail',
                subject_id=subject.id
            )

    return render(
        request,
        'study/create_assignment.html',
        {
            'subject': subject
        }
    )

def edit_assignment(request, assignment_id):

    if not request.user.is_authenticated:
        return redirect('login')

    assignment = get_object_or_404(
        Assignment,
        id=assignment_id,
        user=request.user
    )

    if request.method == 'POST':

        title = request.POST.get('title', '').strip()
        description = request.POST.get('description', '').strip()
        due_date = request.POST.get('due_date')
        status = request.POST.get('status', 'pending')

        if title:

            assignment.title = title
            assignment.description = description
            assignment.due_date = due_date if due_date else None
            assignment.status = status

            assignment.save()

            return redirect(
                'subject_detail',
                subject_id=assignment.subject.id
            )

    return render(
        request,
        'study/edit_assignment.html',
        {
            'assignment': assignment
        }
    )

def assignment_list(request):

    if not request.user.is_authenticated:
        return redirect('login')

    assignments = Assignment.objects.filter(
        user=request.user
    ).select_related(
        'subject'
    ).order_by(
        'status',
        'due_date'
    )

    paginator = Paginator(assignments, 5)

    page_number = request.GET.get('page')

    page_obj = paginator.get_page(page_number)

    return render(
        request,
        'study/assignment_list.html',
        {
            'assignments': page_obj,
            'page_obj': page_obj,
        }
    )

def delete_assignment(request, assignment_id):

    if not request.user.is_authenticated:
        return redirect('login')

    assignment = get_object_or_404(
        Assignment,
        id=assignment_id,
        user=request.user
    )

    if request.method == 'POST':
        subject_id = assignment.subject.id
        assignment.delete()

        return redirect(
            'assignment_list'
        )

    return render(
        request,
        'study/delete_assignment.html',
        {
            'assignment': assignment
        }
    )

def assignment_detail(request, assignment_id):

    if not request.user.is_authenticated:
        return redirect('login')

    assignment = get_object_or_404(
        Assignment,
        id=assignment_id,
        user=request.user
    )

    return render(
        request,
        'study/assignment_detail.html',
        {
            'assignment': assignment
        }
    )


@login_required
def export_pdf(request):

    response = HttpResponse(content_type='application/pdf')

    response['Content-Disposition'] = (
        'attachment; filename="study_hub_report.pdf"'
    )

    pdf = canvas.Canvas(response, pagesize=A4)

    width, height = A4

    # =========================
    # Get user's data
    # =========================

    subjects = Subject.objects.filter(
        user=request.user
    )

    courses = Course.objects.filter(
        user=request.user
    )

    notes = Note.objects.filter(
        user=request.user
    )

    tasks = Task.objects.filter(
        user=request.user
    )

    assignments = Assignment.objects.filter(
        user=request.user
    )

    completed_tasks = tasks.filter(
        completed=True
    ).count()

    pending_tasks = tasks.filter(
        completed=False
    ).count()

    # =========================
    # PDF Header
    # =========================

    pdf.setFont("Helvetica-Bold", 22)

    pdf.drawString(
        50,
        height - 60,
        "Study Hub Report"
    )

    pdf.setFont("Helvetica", 12)

    pdf.drawString(
        50,
        height - 90,
        f"User: {request.user.email}"
    )

    pdf.drawString(
        50,
        height - 115,
        "Study Statistics"
    )

    # =========================
    # Statistics
    # =========================

    y = height - 160

    pdf.setFont("Helvetica", 13)

    statistics = [
        f"Total Subjects: {subjects.count()}",
        f"Total Courses: {courses.count()}",
        f"Total Notes: {notes.count()}",
        f"Total Tasks: {tasks.count()}",
        f"Completed Tasks: {completed_tasks}",
        f"Pending Tasks: {pending_tasks}",
        f"Total Assignments: {assignments.count()}",
    ]

    for statistic in statistics:

        pdf.drawString(
            70,
            y,
            statistic
        )

        y -= 30

    # =========================
    # Tasks Section
    # =========================

    y -= 30

    pdf.setFont("Helvetica-Bold", 16)

    pdf.drawString(
        50,
        y,
        "Tasks"
    )

    y -= 30

    pdf.setFont("Helvetica", 11)

    for task in tasks:

        if y < 80:
            pdf.showPage()
            y = height - 60

            pdf.setFont("Helvetica-Bold", 16)
            pdf.drawString(50, y, "Tasks - Continued")

            y -= 30
            pdf.setFont("Helvetica", 11)

        status = "Completed" if task.completed else "Pending"

        due_date = (
            task.due_date.strftime("%Y-%m-%d")
            if task.due_date
            else "No due date"
        )

        pdf.drawString(
            70,
            y,
            f"Task: {task.title}"
        )

        y -= 20

        pdf.drawString(
            90,
            y,
            f"Status: {status} | Priority: {task.priority}"
        )

        y -= 20

        pdf.drawString(
            90,
            y,
            f"Due Date: {due_date}"
        )

        y -= 30

    # =========================
    # Assignments Section
    # =========================

    y -= 20

    pdf.setFont("Helvetica-Bold", 16)

    pdf.drawString(
        50,
        y,
        "Assignments"
    )

    y -= 30

    pdf.setFont("Helvetica", 11)

    for assignment in assignments:

        if y < 100:
            pdf.showPage()
            y = height - 60

            pdf.setFont("Helvetica-Bold", 16)
            pdf.drawString(
                50,
                y,
                "Assignments - Continued"
            )

            y -= 30
            pdf.setFont("Helvetica", 11)

        due_date = (
            assignment.due_date.strftime("%Y-%m-%d")
            if assignment.due_date
            else "No due date"
        )

        pdf.drawString(
            70,
            y,
            f"Assignment: {assignment.title}"
        )

        y -= 20

        pdf.drawString(
            90,
            y,
            f"Status: {assignment.status}"
        )

        y -= 20

        pdf.drawString(
            90,
            y,
            f"Due Date: {due_date}"
        )

        y -= 30

    # =========================
    # Notes Section
    # =========================

    y -= 20

    pdf.setFont("Helvetica-Bold", 16)

    pdf.drawString(
        50,
        y,
        "Notes"
    )

    y -= 30

    pdf.setFont("Helvetica", 11)

    for note in notes:

        if y < 100:
            pdf.showPage()
            y = height - 60

            pdf.setFont("Helvetica-Bold", 16)
            pdf.drawString(
                50,
                y,
                "Notes - Continued"
            )

            y -= 30
            pdf.setFont("Helvetica", 11)

        pdf.drawString(
            70,
            y,
            f"Note: {note.title}"
        )

        y -= 20

        subject_name = (
            note.subject.name
            if note.subject
            else "No subject"
        )

        pdf.drawString(
            90,
            y,
            f"Subject: {subject_name}"
        )

        y -= 30

    # =========================
    # Finish PDF
    # =========================

    pdf.showPage()

    pdf.save()

    return response