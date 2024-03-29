# Generated by Django 5.0.1 on 2024-02-16 16:21

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Book',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('category', models.CharField(choices=[('M', 'MATHMATICS'), ('S', 'SCIENCE'), ('P', 'PHYSICS')], max_length=1)),
                ('status', models.CharField(choices=[('RA', 'RECENTLY ADDED'), ('MP', 'MOST PURCHASED'), ('TR', 'TOP RATED')], max_length=2)),
                ('title', models.CharField(max_length=255)),
                ('author', models.CharField(max_length=255)),
                ('price', models.DecimalField(decimal_places=2, max_digits=6)),
                ('cover', models.ImageField(blank=True, upload_to='covers/')),
                ('description', models.TextField(blank=True)),
                ('available', models.BooleanField(default=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
            ],
        ),
    ]
