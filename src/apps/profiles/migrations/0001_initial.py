# Generated by Django 4.1.1 on 2022-10-08 20:46

import dirtyfields.dirtyfields
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False, verbose_name='ID записи')),
                ('created_at', models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='Время создания записи')),
                ('updated_at', models.DateTimeField(auto_now=True, db_index=True, verbose_name='Время изменения записи')),
                ('description', models.TextField(blank=True, max_length=1000)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
            bases=(dirtyfields.dirtyfields.DirtyFieldsMixin, models.Model),
        ),
        migrations.CreateModel(
            name='Follower',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False, verbose_name='ID записи')),
                ('created_at', models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='Время создания записи')),
                ('updated_at', models.DateTimeField(auto_now=True, db_index=True, verbose_name='Время изменения записи')),
                ('follow_to', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='followed', to='profiles.profile')),
                ('follower', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='followers', to='profiles.profile')),
            ],
            bases=(dirtyfields.dirtyfields.DirtyFieldsMixin, models.Model),
        ),
        migrations.AddConstraint(
            model_name='follower',
            constraint=models.CheckConstraint(check=models.Q(('follow_to', models.F('follower')), _negated=True), name='check_follow_to_self'),
        ),
        migrations.AlterUniqueTogether(
            name='follower',
            unique_together={('follower', 'follow_to')},
        ),
    ]
