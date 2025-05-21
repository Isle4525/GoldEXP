from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Message, Conversation
from .forms import MessageForm

@login_required
def inbox(request):
    conversations = Conversation.objects.filter(participants=request.user)
    return render(request, 'messaging/inbox.html', {'conversations': conversations})

@login_required
def conversation_view(request, conversation_id):
    conversation = get_object_or_404(Conversation, id=conversation_id)
    if request.user not in conversation.participants.all():
        return redirect('inbox')
    
    messages = conversation.messages.all().order_by('created_at')
    
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.sender = request.user
            message.conversation = conversation
            message.save()
            return redirect('conversation', conversation_id=conversation.id)
    else:
        form = MessageForm()
    
    return render(request, 'messaging/conversation.html', {
        'conversation': conversation,
        'messages': messages,
        'form': form
    })

@login_required
def new_conversation(request, user_id):
    recipient = get_object_or_404(User, id=user_id)
    
    # Проверяем, существует ли уже разговор с этим пользователем
    conversation, created = Conversation.objects.get_or_create(
        participants__in=[request.user, recipient],
        defaults={'participants': [request.user, recipient]}
    )
    
    return redirect('messaging:conversation', conversation_id=conversation.id)


@login_required
def send_message(request, conversation_id):
    conversation = get_object_or_404(Conversation, id=conversation_id)
    if request.user not in conversation.participants.all():
        return redirect('messaging:inbox')

    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.sender = request.user
            message.conversation = conversation
            message.save()
            return redirect('messaging:conversation', conversation_id=conversation.id)
    else:
        form = MessageForm()

    return render(request, 'messaging/conversation.html', {
        'conversation': conversation,
        'form': form
    })

@login_required
def delete_conversation(request, conversation_id):
    conversation = get_object_or_404(Conversation, id=conversation_id)
    if request.user not in conversation.participants.all():
        return redirect('messaging:inbox')

    conversation.delete()
    return redirect('messaging:inbox')
