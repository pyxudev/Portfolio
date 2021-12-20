from __future__ import absolute_import
from celery import shared_task

from datetime import timedelta

from django.conf import settings
from django.utils import timezone
from django.core.mail import send_mail

from api_v1.scraping.models import Project
from api_v1.scraping.models import Execution


def ban_nologin_user():
	from accounts.models import Profile
	from datetime import datetime, timedelta

	last_month = datetime.today() - timedelta(days=30)
	print('last_month:', last_month)

	profiles = Profile.objects.filter(last_login__lte = last_month)

	for profile in profiles:
		profile.is_verified = False

	return

if  __name__ == "__main__":
	ban_nologin_user();
