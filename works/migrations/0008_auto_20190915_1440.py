# Generated by Django 2.2.5 on 2019-09-15 14:40

import django.contrib.postgres.fields
import django.contrib.postgres.fields.citext
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('works', '0007_auto_20190915_1437'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contributor',
            name='first_name',
            field=django.contrib.postgres.fields.citext.CICharField(blank=True, db_index=True, default='', max_length=100),
        ),
        migrations.AlterField(
            model_name='contributor',
            name='last_name',
            field=django.contrib.postgres.fields.citext.CICharField(db_index=True, max_length=100),
        ),
        migrations.AlterField(
            model_name='contributor',
            name='middle_name',
            field=django.contrib.postgres.fields.citext.CICharField(blank=True, db_index=True, default='', max_length=100),
        ),
        migrations.AlterField(
            model_name='source',
            name='identifier',
            field=django.contrib.postgres.fields.citext.CICharField(max_length=30, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='work',
            name='title',
            field=django.contrib.postgres.fields.citext.CICharField(max_length=256),
        ),
        migrations.AlterField(
            model_name='work',
            name='title_synonyms',
            field=django.contrib.postgres.fields.ArrayField(base_field=django.contrib.postgres.fields.citext.CICharField(max_length=256), blank=True, default=list, size=None),
        ),
    ]
