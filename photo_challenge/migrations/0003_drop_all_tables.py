# Generated by Django 5.0.6 on 2024-06-27 12:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('photo_challenge', '0002_rename_details_photochallenge_description_and_more'),
    ]

    operations = [
        migrations.DeleteModel(
            name='PhotoSubmission',
        ),
        migrations.DeleteModel(
            name='PhotoChallengeComment',
        ),
        migrations.DeleteModel(
            name='PhotoChallengeVote',
        ),
        migrations.DeleteModel(
            name='PhotoChallenge',
        ),
    ]