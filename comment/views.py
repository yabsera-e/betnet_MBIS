from django.shortcuts import render,get_object_or_404, redirect
from .forms import CommentForm
from .models import Comment
from django.core.files.storage import default_storage
from django.conf import settings
from django.contrib import messages
from django.urls import reverse
import uuid
import os
from django.contrib.auth.decorators import login_required

@login_required
def create(request):
    # form = CommentForm(request.POST)
    # if form.is_valid():
    #     form.instance.user_id = request.user.id
    #     form.save()

    content = request.POST.get('content')

    comment = Comment.objects.create(
        content=content,
        user = request.user
    )
    messages.info(request,'Thank you for your comment!')
        # return redirect("listings")
    
    # messages.info(request,'error ocurred')
    return redirect("listings")