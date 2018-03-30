# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from forms import *
def write(request):
    if request.method == 'POST':
        form = Form(request.POST)
        if form.is_valid():
            form.save()
            print 'saved!'
    else:
        form=Form()

    return render(request , 'write.html' , {'form' : form})


def list(request):
    articleList = Article.objects.all()
    print 'articleList' ,articleList
    return render (request , 'list.html' , {'articleList':articleList})

# Create your views here.


def view(request , num = '1'):
    article=Article.objects.get(id=num)
    return render(request , 'view.html' , {'article':article})