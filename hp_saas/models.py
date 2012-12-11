from django.db import models
from django.contrib import auth

from annoying.fields import AutoOneToOneField
from account.signals import user_signed_up


class HpAccount(models.Model):
    name = models.CharField(max_length=100)
    creation_user = models.ForeignKey('auth.user')

    def __unicode__(self):
        return self.name


class HpLocation(models.Model):
    name = models.CharField(max_length=100)
    hpaccount = models.ForeignKey('HpAccount')
    creation_user = models.ForeignKey('auth.user')

    def __unicode__(self):
        return self.name


class HpProfile(models.Model):
    user = AutoOneToOneField('auth.user')
    company_name = models.CharField(max_length=100)
    next_url = models.CharField(max_length=255, null=True, blank=True)

    def __unicode__(self):
        return u'proile for %s' % self.user


def post_signup(sender, user, form, **kwargs):
    user.first_name = form.cleaned_data['first_name']
    user.last_name = form.cleaned_data['last_name']
    user.save()

    use_name = form.cleaned_data.get('company_name', u'%s %s' % (
        form.cleaned_data['first_name'],
        form.cleaned_data['last_name'].upper()))

    hpaccount = HpAccount.objects.create(name=use_name, creation_user=user)
    HpLocation.objects.create(hpaccount=hpaccount,
        name=use_name, creation_user=user)

    # i wonder why i need this
    user.hpprofile.pk
    user.hpprofile.next_url = form.cleaned_data['next']
    user.hpprofile.save()
user_signed_up.connect(post_signup)
