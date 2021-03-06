"""Models for minipoll"""
from datetime import datetime

from django.db import models
from django.db.models import Count
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _

from batch_select.models import BatchManager

from minipoll.managers import DRAFT, PUBLISHED, ARCHIVED

STATUS_CHOICES = ((DRAFT, _('draft')),
                  (PUBLISHED, _('published')),
                  (ARCHIVED, _('archived')),
                  )

class Poll(models.Model):
    """A simple poll"""
    title = models.CharField(_('title'), max_length=250)
    description = models.TextField(_('description'), blank=True)
    #open_response = models.BooleanField(_('open response'))

    slug = models.SlugField(_('slug'))
    creator = models.ForeignKey(User, verbose_name=_('creator'))
    status = models.IntegerField(_('status'), choices=STATUS_CHOICES, default=DRAFT)
    creation_date = models.DateTimeField(_('creation date'), auto_now_add=True)
    modification_date = models.DateTimeField(_('modification date'), auto_now=True)
    publication_date = models.DateTimeField(_('publication date'), default=datetime.now)

    objects = models.Manager()
    batched = BatchManager()

    class Meta:
        ordering = ('-creation_date',)
        verbose_name = _('Poll')
        verbose_name_plural = _('Polls')

    def __unicode__(self):
        return self.title

    @models.permalink
    def get_absolute_url(self):
        return ('minipoll_poll_detail', (self.slug,))

    def votes(self):
	self.vote_set.count()
    votes.short_description = _('votes')

    @staticmethod
    def calculate(poll):
	choices_all = []
	total_votes = float(poll.total_votes)
	for choice in poll.choices.annotate(votes_count=Count('vote')).all():
	    if choice.votes_count == 0:
		percent = 0.0
	    else:
		percent = (float(choice.votes_count) / total_votes) * 100.0
	    setattr(choice, 'c_percent', percent)
	    choices_all.append(choice)
	setattr(poll, 'c_choices', choices_all)
	return poll


class Choice(models.Model):
    """A choice for a poll"""
    poll = models.ForeignKey(Poll, verbose_name=_('poll'), related_name='choices')
    
    title = models.CharField(_('title'), max_length=250)
    description = models.TextField(_('description'), blank=True)
    creation_date = models.DateTimeField(_('creation date'), auto_now_add=True)

    is_active = models.BooleanField(_('is active'), default=True,
                                    help_text=_('If you want to disable this choice.'))
    display_priority = models.IntegerField(_('display priority'), default=100,
                                           help_text=_('Used to ordonnate the choices.'))

    objects = models.Manager()

    class Meta:
        ordering = ('-display_priority', 'creation_date',)
        verbose_name = _('Choice')
        verbose_name_plural = _('Choices')

    def __unicode__(self):
        return self.title

    def votes(self):
	return self.vote_set.count()

    votes.short_description = _('votes')

    def percent(self):
        poll_votes = self.poll.votes()
        if not poll_votes:
            return 0.0
        return float(self.votes()) / float(poll_votes) * 100.0

class Vote(models.Model):
    """A vote for a poll"""
    poll = models.ForeignKey(Poll, verbose_name=_('poll'))
    choice = models.ForeignKey(Choice, verbose_name=_('choice'))
    #comment = models.CharField(_('comment'), max_length=250,
    #                           blank=True)

    voter = models.ForeignKey(User, verbose_name=_('voter'),
                              blank=True, null=True)
    ip_address = models.IPAddressField(_('ip address'))
    creation_date = models.DateTimeField(_('creation date'), auto_now_add=True)

    class Meta:
        ordering = ('-creation_date',)
        verbose_name = _('Vote')
        verbose_name_plural = _('Votes')

    def __unicode__(self):
        return '%s %s' % (self.choice.__unicode__(), self.creation_date)
