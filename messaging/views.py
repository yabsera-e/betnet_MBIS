from django.shortcuts import render, get_object_or_404, redirect
from .models import Conversation, Message
from users.models import CustomUser
from listing.models import Listing
from .forms import MessageForm
from django.contrib.auth.decorators import login_required

@login_required
def conversation_list(request):
    conversations = Conversation.objects.filter(participants=request.user)
    return render(request, 'messaging/conversation_list.html', {'conversations': conversations})

@login_required
def start_conversation(request, listing_id, user_id):
    other_user = get_object_or_404(CustomUser, pk=user_id)
    listing = get_object_or_404(Listing, id=listing_id)

    conversation = Conversation.objects.filter(
        participants=request.user
    ).filter(
        participants=other_user
    ).filter(
        listing=listing
    ).distinct().first()

    if conversation:
        if not conversation.is_paid:
            return redirect('messaging_payment', conversation_id=conversation.id)
        return redirect('conversation_detail', pk=conversation.pk)
    else:
        conversation = Conversation.objects.create(listing=listing)
        conversation.participants.add(request.user, other_user)
        return redirect('messaging_payment', conversation_id=conversation.id)

@login_required
def messaging_payment(request, conversation_id):
    conversation = get_object_or_404(Conversation, pk=conversation_id)

    if request.method == "POST":
        conversation.is_paid = True
        conversation.save()
        return redirect('conversation_detail', pk=conversation.id)

    return render(request, 'payment/messaging_payment.html', {'conversation': conversation})

@login_required
def conversation_detail(request, pk):
    conversation = get_object_or_404(Conversation, pk=pk, participants=request.user)

    # Ensure payment is done before showing chat
    if not conversation.is_paid:
        return redirect('messaging_payment', conversation_id=conversation.id)

    messages_qs = Message.objects.filter(conversation=conversation).order_by('created_at')
    form = MessageForm()
    return render(request, 'messaging/conversation_detail.html', {
        'conversation': conversation,
        'messages': messages_qs,
        'form': form
    })

@login_required
def send_message(request, pk):
    form = MessageForm(request.POST)
    if form.is_valid():
        conversation = get_object_or_404(Conversation, pk=pk, participants=request.user)
        # Only allow sending message if paid
        if conversation.is_paid:
            Message.objects.create(
                author=request.user,
                conversation=conversation,
                content=request.POST.get('content')
            )
    return redirect('conversation_detail', pk=pk)
