from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import (
    get_object_or_404,
    redirect,
    render
)

from .models import Conversation, Message
from .services import generate_ai_response


@login_required
def chat(request):

    user = request.user

    conversations = Conversation.objects.filter(
        user=user
    ).order_by('-updated_at')

    conversation_id = request.GET.get('conversation')

    conversation = None

    if conversation_id:

        conversation = get_object_or_404(
            Conversation,
            id=conversation_id,
            user=user
        )

    elif conversations.exists():

        conversation = conversations.first()

    messages = (
        conversation.messages.all()
        if conversation
        else []
    )

    context = {
        'conversations': conversations,
        'conversation': conversation,
        'messages': messages,
    }

    return render(
        request,
        'chatbot/chat.html',
        context
    )


@login_required
def new_conversation(request):

    conversation = Conversation.objects.create(
        user=request.user,
        title='New Chat'
    )

    return redirect(
        f'/chatbot/?conversation={conversation.id}'
    )


@login_required
def send_message(request):

    if request.method != 'POST':

        return JsonResponse(
            {
                'success': False,
                'error': 'Only POST requests are allowed.'
            },
            status=405
        )

    conversation_id = request.POST.get('conversation_id')

    user_message = request.POST.get(
        'message',
        ''
    ).strip()

    if not user_message:

        return JsonResponse(
            {
                'success': False,
                'error': 'Message cannot be empty.'
            },
            status=400
        )

    conversation = get_object_or_404(
        Conversation,
        id=conversation_id,
        user=request.user
    )

    Message.objects.create(
        conversation=conversation,
        role='user',
        content=user_message
    )

    previous_messages = list(
        conversation.messages.all()
    )[:-1]

    try:

        ai_response = generate_ai_response(
            user=request.user,
            user_message=user_message,
            conversation_messages=previous_messages
        )

    except Exception as e:

        return JsonResponse(
            {
                'success': False,
                'error': str(e)
            },
            status=500
        )

    Message.objects.create(
        conversation=conversation,
        role='assistant',
        content=ai_response
    )

    if conversation.title == 'New Chat':

        conversation.title = user_message[:50]

    conversation.save()

    return JsonResponse(
        {
            'success': True,
            'response': ai_response,
            'conversation_id': conversation.id,
        }
    )