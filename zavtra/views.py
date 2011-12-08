#-*- coding: utf-8 -*-
from datetime import datetime, timedelta
from itertools import groupby

from django.http import HttpResponseRedirect
from django.contrib.auth import logout as auth_logout

from annoying.decorators import render_to

from corecontent.models import ContentItem

from utils import cached

oneday = timedelta(days=1)

@render_to('home.html')
def home(request):
    now = datetime.now().date()
    wstart = now - oneday*(now.weekday() - 2)
    wend = wstart + 7*oneday
    """ Cache by wstart, wend? """
    def get_content():
        qs = ContentItem.batched.batch_select('authors').select_related('rubric').filter(
	    enabled=True, pub_date__range = (wstart, wend), rubric__on_main=True
	)
	newsletter = {}
	for item in list(qs):
	    newsletter.setdefault(item.rubric_id, {'rubric': None, 'items': []})
	    if newsletter[item.rubric_id]['rubric'] is None:
		newsletter[item.rubric_id]['rubric'] = item.rubric
	    newsletter[item.rubric_id]['items'].append(item)
	return sorted(newsletter.values(), key=lambda p: p['rubric'].position)
    newsletter = cached(
	get_content,
	'newsletter'
    )
    blogs = cached(
	lambda: ContentItem.batched.batch_select('authors').filter(enabled=True, rubric=None)[0:6],
	'blogs',
	duration = (wend - now).seconds
    )
    return {
	'newsletter': newsletter,
	'blogs': blogs
    }

@render_to('login.html')
def login(request):
    return {}

@render_to('archive.html')
def archive(request):
    issues = sorted(Issue.objects.order_by('date'), key=lambda issue: issue.date.year, reverse=True)
    return {
        'in_archive': True,
        'issues': [(k, list(g)) for k, g in groupby(issues, lambda w: w.date.year)]
    }

def logout(request):
    auth_logout(request)
    return HttpResponseRedirect('/')

def logged_in(request):
    raise Exception, "OLOLO!"
