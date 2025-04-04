# Generated by Django 4.0 on 2024-10-28 00:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('portfolio', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='blogitem',
            options={'ordering': ['order']},
        ),
        migrations.AlterModelOptions(
            name='chip',
            options={'ordering': ['order']},
        ),
        migrations.AlterModelOptions(
            name='collegeitem',
            options={'ordering': ['order']},
        ),
        migrations.AlterModelOptions(
            name='projectitem',
            options={'ordering': ['order']},
        ),
        migrations.AddField(
            model_name='blogitem',
            name='order',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='chip',
            name='order',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='collegeitem',
            name='order',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='projectitem',
            name='order',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='blogitem',
            name='redirect',
            field=models.URLField(),
        ),
    ]
