# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, get_object_or_404,redirect
from .models import Board,Topic,Post
from .forms import NewTopicForm, PostForm
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.utils import timezone
from django.views.generic import UpdateView
from django.utils.decorators import method_decorator 
from django.views.generic import ListView



# Create your views here.
#for the home view
"""def home(request):
	boards = Board.objects.all()
	return render(request,'home.html',{'boards':boards})"""

class BoardListView(ListView):
    model = Board
    context_object_name =  'boards'
    template_name = 'home.html'

def board_topics(request,pk):
    board = get_object_or_404(Board,pk=pk)
    topics = board.topics.order_by('-last_updated').annotate(replies=Count('posts')-1)
    return render(request,'topics.html', {'board':board,'topics':topics})

@login_required(login_url='/login/')
def new_topic(request, pk):
    board = get_object_or_404(Board, pk=pk)
    user = User.objects.first()  # TODO: get the currently logged in user
    if request.method == 'POST':
        form = NewTopicForm(request.POST)
        if form.is_valid():
            topic = form.save(commit=False)
            topic.board = board
            topic.starter = user
            topic.save()
            post = Post.objects.create(
                message=form.cleaned_data.get('message'),
                topic=topic,
                created_by=user
            )
            return redirect('topic_posts', pk=pk,topic_pk = topic.pk)  # TODO: redirect to the created topic page
    else:
        form = NewTopicForm()
    return render(request, 'new_topic.html', {'board': board, 'form': form})

def topic_posts(request, pk, topic_pk):
    topic = get_object_or_404(Topic, board__pk=pk, pk=topic_pk)
    topic.views += 1
    topic.save()
    return render(request, 'topic_posts.html', {'topic': topic})

@login_required
def reply_topic(request, pk, topic_pk):
    topic = get_object_or_404(Topic, board__pk=pk, pk=topic_pk)
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.topic = topic
            post.created_by = request.user
            post.save()
            return redirect('topic_posts', pk=pk, topic_pk=topic_pk)
    else:
        form = PostForm()
    return render(request, 'reply_topic.html', {'topic': topic, 'form': form})

@method_decorator(login_required,name='dispatch')
class PostUpdateView(UpdateView):
    model = Post
    fields = ('message',)
    template_name = 'edit_post.html'
    pk_url_kwarg = 'post_pk'
    context_objec_name ='post'

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(created_by=self.request.user)

    def form_valid(self,form):
        post = form.save(commit=False)
        post.updated_by = self.request.user
        post.updated_at =  timezone.now()
        post.save()
        return redirect('topic_posts',pk=post.topic.board.pk,topic_pk=post.topic.pk)