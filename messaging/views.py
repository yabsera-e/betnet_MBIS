from django.shortcuts import render, get_object_or_404, redirect
from.models import Conversation, Message
from users.models import CustomUser
from listing.models import Listing
from .forms import MessageForm
from django.contrib.auth.decorators import login_required

@login_required
def conversation_list(request):
    conversations = Conversation.objects.filter(participants=request.user)
    return render(request, 'messaging/conversation_list.html', {'conversations': conversations})

# def start_conversation(request, user_id):
#     other_user = get_object_or_404(CustomUser, pk=user_id)
#     conversation = Conversation.objects.create()
#     conversation.participants.add(request.user, other_user)
#     return redirect('conversation_detail', pk=conversation.pk)

@login_required
def start_conversation(request, listing_id, user_id):
    other_user = get_object_or_404(CustomUser, pk=user_id)
    conversation = Conversation.objects.filter(participants=request.user).filter(participants=other_user).filter(listing_id=listing_id).distinct().first()
    listing = get_object_or_404(Listing, id=listing_id)
    if conversation:
        # conversation.listing = listing
        # conversation.save()
        return redirect('conversation_detail', pk=conversation.pk)
    else:
        conversation = Conversation.objects.create(listing=listing)
        conversation.participants.add(request.user, other_user)
        return redirect('conversation_detail', pk=conversation.pk)

@login_required
def conversation_detail(request, pk):
    conversation = get_object_or_404(Conversation, pk=pk, participants=request.user)
    messages = Message.objects.filter(conversation=conversation).order_by('created_at')
    form = MessageForm()
    return render(request, 'messaging/conversation_detail.html', {'conversation': conversation, 'messages': messages, 'form':form})

@login_required
def send_message(request, pk):
    form = MessageForm(request.POST)
    if form.is_valid():
        conversation = get_object_or_404(Conversation, pk=pk)
        message = Message.objects.create(author=request.user, conversation=conversation, content=request.POST.get('content'))
    return redirect('conversation_detail', pk=conversation.pk)