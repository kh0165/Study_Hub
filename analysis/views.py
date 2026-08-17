from django.shortcuts import render, redirect, get_object_or_404
from django.conf import settings
from django.contrib.auth.decorators import login_required

from .models import Analysis
from study.models import Note

from google import genai


@login_required
def analysis_list(request):

    analyses = Analysis.objects.filter(
        user=request.user
    ).order_by('-created_at')

    return render(
        request,
        'analysis/analysis_list.html',
        {
            'analyses': analyses
        }
    )


@login_required
def analysis_history(request):

    analyses = Analysis.objects.filter(
        user=request.user
    ).order_by('-created_at')

    return render(
        request,
        'analysis/history.html',
        {
            'analyses': analyses
        }
    )


@login_required
def create_analysis(request):

    notes = Note.objects.filter(
        user=request.user
    ).select_related(
        'subject'
    ).order_by(
        '-created_at'
    )

    if request.method == 'POST':

        note_id = request.POST.get('note_id')
        analysis_type = request.POST.get('analysis_type')

        note = get_object_or_404(
            Note,
            id=note_id,
            user=request.user
        )

        if analysis_type not in ['summarize', 'explain']:

            return render(
                request,
                'analysis/create_analysis.html',
                {
                    'notes': notes,
                    'error': 'Please select a valid analysis type.'
                }
            )

        analysis = Analysis.objects.create(
            user=request.user,
            title=note.title,
            analysis_type=analysis_type,
            input_data=note.content,
            status='pending'
        )

        try:

            # Gemini client
            client = genai.Client(
                api_key=settings.GEMINI_API_KEY
            )

            if analysis_type == 'summarize':

                prompt = f"""
You are an AI study assistant inside Study Hub.

Summarize the following student note in a clear and concise way.

Requirements:
- Keep the important ideas.
- Remove unnecessary repetition.
- Use simple language.
- Organize the summary using bullet points when useful.
- Do not add information that is not present in the note.

Student Note:

{note.content}
"""

            else:

                prompt = f"""
You are an AI study assistant inside Study Hub.

Explain the following student note in a simple and educational way.

Requirements:
- Explain the main concepts clearly.
- Break difficult ideas into simple points.
- Give examples when useful.
- Keep the explanation related to the original note.
- Do not add unrelated information.

Student Note:

{note.content}
"""

            # Send request to Gemini
            response = client.models.generate_content(
    model="gemini-3.6-flash",
    contents=prompt
)

            result = response.text

            analysis.result = result
            analysis.status = 'completed'
            analysis.save()

        except Exception as e:

            analysis.result = f"AI analysis failed: {str(e)}"
            analysis.status = 'failed'
            analysis.save()

        return redirect(
            'analysis_detail',
            analysis_id=analysis.id
        )

    return render(
        request,
        'analysis/create_analysis.html',
        {
            'notes': notes
        }
    )


@login_required
def analysis_detail(request, analysis_id):

    analysis = get_object_or_404(
        Analysis,
        id=analysis_id,
        user=request.user
    )

    return render(
        request,
        'analysis/analysis_detail.html',
        {
            'analysis': analysis
        }
    )