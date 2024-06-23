# editing/admin.py
from django.contrib import admin
from .models import EditingChallenge, EditingSubmission

admin.site.register(EditingChallenge)
admin.site.register(EditingSubmission)
