from django.conf import settings
from google import genai

from study.models import (
    Subject,
    Note,
    Task,
    Assignment,
    Course,
    Resource,
)


MODEL_NAME = "gemini-3.6-flash"


def build_study_context(user):

    subjects = Subject.objects.filter(
        user=user
    ).order_by("name")

    notes = Note.objects.filter(
        user=user
    ).select_related(
        "subject"
    ).order_by(
        "-created_at"
    )[:10]

    tasks = Task.objects.filter(
        user=user,
        completed=False
    ).select_related(
        "subject"
    ).order_by(
        "due_date",
        "-created_at"
    )[:10]

    assignments = Assignment.objects.filter(
        user=user
    ).select_related(
        "subject"
    ).order_by(
        "due_date",
        "-created_at"
    )[:10]

    courses = Course.objects.filter(
        user=user
    ).select_related(
        "subject"
    ).order_by(
        "-created_at"
    )[:10]

    resources = Resource.objects.filter(
        user=user
    ).select_related(
        "subject"
    ).order_by(
        "-created_at"
    )[:10]

    context = []

    context.append("STUDENT SUBJECTS:")

    for subject in subjects:

        description = (
            subject.description
            if subject.description
            else "No description"
        )

        context.append(
            f"- {subject.name}: {description}"
        )

    context.append("\nRECENT NOTES:")

    for note in notes:

        context.append(
            f"- Subject: {note.subject.name}\n"
            f"  Title: {note.title}\n"
            f"  Content: {note.content[:3000]}"
        )

    context.append("\nPENDING TASKS:")

    for task in tasks:

        subject_name = (
            task.subject.name
            if task.subject
            else "No subject"
        )

        due_date = (
            task.due_date
            if task.due_date
            else "No due date"
        )

        context.append(
            f"- {task.title} | "
            f"Subject: {subject_name} | "
            f"Priority: {task.priority} | "
            f"Due: {due_date}"
        )

    context.append("\nASSIGNMENTS:")

    for assignment in assignments:

        due_date = (
            assignment.due_date
            if assignment.due_date
            else "No due date"
        )

        context.append(
            f"- {assignment.title} | "
            f"Subject: {assignment.subject.name} | "
            f"Status: {assignment.status} | "
            f"Due: {due_date}"
        )

    context.append("\nCOURSES:")

    for course in courses:

        context.append(
            f"- {course.title} | "
            f"Subject: {course.subject.name} | "
            f"Progress: {course.progress}% | "
            f"Status: {course.status}"
        )

    context.append("\nRESOURCES:")

    for resource in resources:

        context.append(
            f"- {resource.title} | "
            f"Subject: {resource.subject.name} | "
            f"Type: {resource.resource_type}"
        )

    return "\n".join(context)


def generate_ai_response(
    user,
    user_message,
    conversation_messages=None
):

    client = genai.Client(
        api_key=settings.GEMINI_API_KEY
    )

    study_context = build_study_context(user)

    history = ""

    if conversation_messages:

        history = "\n\nRECENT CHAT HISTORY:\n"

        for message in conversation_messages[-10:]:

            role = (
                "Student"
                if message.role == "user"
                else "AI Assistant"
            )

            history += (
                f"{role}: {message.content}\n"
            )

    prompt = f"""
You are StudyHub AI Assistant.

You are a personal study assistant inside the StudyHub
web application.

You help the student with:
- Understanding notes
- Studying subjects
- Organizing tasks
- Reviewing assignments
- Tracking courses
- Finding useful study resources
- Creating study plans
- Explaining difficult concepts

IMPORTANT RULES:

1. Be clear and educational.
2. Use the student's StudyHub data when relevant.
3. Never invent information about the student's data.
4. Never reveal information belonging to another user.
5. If the requested information is not available,
   say that clearly.
6. Use simple language.
7. Use bullet points or numbered steps when useful.
8. Do not claim that you changed anything in StudyHub
   unless the application actually performed that action.
9. Focus on helping the student learn.

STUDENT STUDY DATA:

{study_context}

{history}

CURRENT STUDENT MESSAGE:

{user_message}

Answer the student directly.
"""

    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=prompt
    )

    return response.text.strip()