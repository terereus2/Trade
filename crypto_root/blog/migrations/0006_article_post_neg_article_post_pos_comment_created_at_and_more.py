# Generated by Django 4.1.5 on 2023-02-08 11:07

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('blog', '0005_comment_delete_modelregisteruser'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='post_neg',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='article',
            name='post_pos',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='comment',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.CreateModel(
            name='UserVote',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('vote_type', models.CharField(max_length=10)),
                ('article', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='blog.article')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
