from django.shortcuts import render, render_to_response, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext

from django.views.generic.list import ListView
from django.views.generic.detail import DetailView

from main.models import Tweet


# ---- models.py Tweet -----------------------------
class TweetListView(ListView):
    model = Tweet
    template_name = 'tweet_list.html'
    context_object_name = 'tweets'


class TweetDetailView(DetailView):
    model = Tweet
    slug_field = 'time_handle'
    template_name = 'tweet_detail.html'
    context_object_name = 'tweets'
