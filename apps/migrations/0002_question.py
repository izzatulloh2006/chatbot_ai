# Generated by Django 5.2.4 on 2025-07-06 14:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apps', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_id', models.BigIntegerField()),
                ('username', models.CharField(blank=True, max_length=150, null=True)),
                ('question', models.TextField()),
                ('answer', models.TextField()),
                ('language', models.CharField(default='uz', max_length=10)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
