# Generated by Django 3.0.6 on 2020-10-08 03:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tool', '0006_auto_20200528_0459'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='domaininfo',
            name='broken_links_count',
        ),
        migrations.RemoveField(
            model_name='domaininfo',
            name='robots_txt_info',
        ),
        migrations.RemoveField(
            model_name='domaininfo',
            name='sitemap_info',
        ),
        migrations.AddField(
            model_name='domaininfo',
            name='connection_time',
            field=models.FloatField(null=True),
        ),
    ]
