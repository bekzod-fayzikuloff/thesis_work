# Generated by Django 4.1.1 on 2022-10-27 21:48

import dirtyfields.dirtyfields
from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import functools
import src.common.validators


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False, verbose_name='ID записи')),
                ('created_at', models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='Время создания записи')),
                ('updated_at', models.DateTimeField(auto_now=True, db_index=True, verbose_name='Время изменения записи')),
                ('description', models.TextField(max_length=1000)),
                ('is_active', models.BooleanField(default=True)),
            ],
            options={
                'verbose_name': 'Пост',
                'verbose_name_plural': 'Посты',
            },
            bases=(dirtyfields.dirtyfields.DirtyFieldsMixin, models.Model),
        ),
        migrations.CreateModel(
            name='PostMedia',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False, verbose_name='ID записи')),
                ('created_at', models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='Время создания записи')),
                ('updated_at', models.DateTimeField(auto_now=True, db_index=True, verbose_name='Время изменения записи')),
                ('file', models.FileField(upload_to='posts/media/%Y/%m/%d/', validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['jpg', 'png', 'gif', 'bmp', 'ico', 'mp4', 'webm', 'avi']), functools.partial(src.common.validators.validate_file_size, *(), **{'max_size': 10485760})])),
            ],
            options={
                'verbose_name': 'Медия поста',
                'verbose_name_plural': 'Медия постов',
            },
            bases=(dirtyfields.dirtyfields.DirtyFieldsMixin, models.Model),
        ),
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
                'verbose_name': 'Профиль',
                'verbose_name_plural': 'Профили',
            },
            bases=(dirtyfields.dirtyfields.DirtyFieldsMixin, models.Model),
        ),
        migrations.CreateModel(
            name='PostsGroup',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('creator', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='posts_groups', related_query_name='posts_group', to='profiles.profile')),
                ('posts', models.ManyToManyField(blank=True, related_name='groups', to='profiles.post')),
            ],
            options={
                'verbose_name': 'Коллекция постов',
                'verbose_name_plural': 'Коллекции постов',
            },
        ),
        migrations.AddField(
            model_name='post',
            name='creator',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='posts', related_query_name='posts', to='profiles.profile'),
        ),
        migrations.AddField(
            model_name='post',
            name='medias',
            field=models.ManyToManyField(related_name='posts', related_query_name='posts', to='profiles.postmedia'),
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
            options={
                'verbose_name': 'Подписчик',
                'verbose_name_plural': 'Подписчики',
            },
            bases=(dirtyfields.dirtyfields.DirtyFieldsMixin, models.Model),
        ),
        migrations.AddConstraint(
            model_name='follower',
            constraint=models.CheckConstraint(check=models.Q(('follow_to', models.F('follower')), _negated=True), name='check_follow_to_self', violation_error_message='Users cannot follow to themselves.'),
        ),
        migrations.AlterUniqueTogether(
            name='follower',
            unique_together={('follower', 'follow_to')},
        ),
    ]
