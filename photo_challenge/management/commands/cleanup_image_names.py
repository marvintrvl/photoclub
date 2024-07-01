# In a new file: photo_challenge/management/commands/cleanup_image_names.py

from django.core.management.base import BaseCommand
from photo_challenge.models import PhotoChallengeSubmission
import os

class Command(BaseCommand):
    help = 'Cleans up image names with multiple _resized suffixes'

    def handle(self, *args, **options):
        submissions = PhotoChallengeSubmission.objects.all()
        for submission in submissions:
            for field in ['image1', 'image2', 'image3']:
                image = getattr(submission, field)
                if image:
                    old_name = image.name
                    name, ext = os.path.splitext(old_name)
                    name = name.rsplit('_resized', 1)[0]
                    new_name = f"{name}_resized{ext}"
                    if old_name != new_name:
                        os.rename(image.path, os.path.join(os.path.dirname(image.path), new_name))
                        image.name = new_name
                        submission.save()
                        self.stdout.write(self.style.SUCCESS(f'Renamed {old_name} to {new_name}'))