# Generated by Django 4.2.16 on 2024-11-20 16:17

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("correction", "0002_alter_answer_score"),
    ]

    operations = [
        migrations.AddField(
            model_name="answer",
            name="extract_value",
            field=models.CharField(blank=True, max_length=1000, null=True),
        ),
    ]
